#!/usr/bin/env python3

from logging import getLogger

from requests import Session

from kodictl.media import Movies, Songs


class KodiCtl:
    """Kodi control class"""

    def __init__(self, hostname, port, username=None, password=None, tls=False):
        self.hostname = hostname
        self.port = port
        self.tls = tls
        self.__username = username
        self.__password = password
        self.__movies = None
        self.__songs = None
        self.session = Session()
        self.log = getLogger(__name__)
        self._subtitles = 'Unknown'

    @property
    def uri(self):
        """return the uri"""
        return '{}://{}:{}'.format(self.proto, self.hostname, self.port)

    @property
    def proto(self):
        """return the protocol"""
        return 'https' if self.tls else 'http'

    @property
    def username(self):
        """username getter"""
        return self.__username

    @username.setter
    def username(self, username):
        """username setter"""
        self.__username = username
        self.session.auth = (self.username, self.password)

    @property
    def password(self):
        """password getter"""
        return self.__password

    @password.setter
    def password(self, password):
        """password setter"""
        self.__password = password
        self.session.auth = (self.username, self.password)

    def _post(self, method, params=None, api_id=1):
        """Perform a kodi jsonrpc call"""
        payload = {'jsonrpc': '2.0', 'method': method, 'id': api_id}
        jsonrpc = '{}/{}'.format(self.uri, 'jsonrpc')
        if params:
            payload['params'] = params
        try:
            response = self.session.post(jsonrpc, json=payload)
            self.log.debug(response.text)
            return response.json()['result']
        # TODO: add better error handeling
        except Exception as e:
            pass
        return {}

    @property
    def subtitles(self):
        return self._subtitles

    @subtitles.setter
    def subtitles(self, value):
        if not isinstance(value, bool):
            raise ValueError('argument must be boolean')
        if value != self._subtitles:
            self._subtitles = value
            method = 'Player.SetSubtitle'
            _value = 'on' if value else 'off'
            params = {'playerid': 1, 'subtitle': _value}
            self._post(method, params)

    @property
    def playing(self):
        """ check if kodi is currently playing, required for some functions"""
        method = 'Player.GetActivePlayers'
        # TODO: this seems like it could be improved?
        return bool(self._post(method))

    @property
    def movies(self):
        """List all movies in kodi"""
        if self.__movies is None:
            method = 'VideoLibrary.GetMovies'
            params = {'properties': []}
            results = self._post(method, params)
            self.__movies = Movies(results.get('movies', {}))
        return self.__movies

    @property
    def songs(self):
        """List all songs"""
        if self.__songs is None:
            method = 'AudioLibrary.GetSongs'
            params = {'properties': ['artist', 'duration', 'album', 'track']}
            result = self._post(method, params)
            self.__songs = Songs(result.get('songs', {}))
        return self.__songs
