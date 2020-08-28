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
        self._username = username
        self._password = password
        self._movies = None
        self._songs = None
        self.session = Session()
        self.log = getLogger(__name__)
        self._subtitles = None
        self._pause = None
        self._volume = None

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
        return self._username

    @username.setter
    def username(self, username):
        """username setter"""
        self._username = username
        self.session.auth = (self.username, self.password)

    @property
    def password(self):
        """password getter"""
        return self._password

    @password.setter
    def password(self, password):
        """password setter"""
        self._password = password
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
    def pause(self):
        return self._pause

    @pause.setter
    def pause(self, value):
        if not isinstance(value, bool):
            raise ValueError('argument must be boolean')
        if value != self._pause:
            self._pause = value
            method = 'Player.PlayPause'
            params = {'playerid': 1, 'play': not self._pause}
            self._post(method, params)

    @property
    def volume(self):
        # TODO: maybe get the current volume
        return self._volume

    @volume.setter
    def volume(self, value):
        if not isinstance(value, int):
            raise ValueError('argument must be int')
        if value != self._volume:
            self._volume = value
            method = 'Application.SetVolume'
            params = {'volume': self._volume}
            self._post(method, params)

    @property
    def active_window(self):
        # TODO: maybe get the current volume
        return self._active_window

    @active_window.setter
    def active_window(self, value):
        # TODO: add valid gui's
        if not isinstance(value, str):
            raise ValueError('argument must be string')
        if value != self._active_window:
            self._active_window = value
            method = 'GUI.ActiveWindow'
            params = {'window': 'videos', 'parameters': [self._active_window]}
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
        if self._movies is None:
            method = 'VideoLibrary.GetMovies'
            params = {'properties': []}
            results = self._post(method, params)
            self._movies = Movies(results.get('movies', {}))
        return self._movies

    @property
    def songs(self):
        """List all songs"""
        if self._songs is None:
            method = 'AudioLibrary.GetSongs'
            params = {'properties': ['artist', 'duration', 'album', 'track']}
            result = self._post(method, params)
            self._songs = Songs(result.get('songs', {}))
        return self._songs

    def add_to_playlist(self, media):
        """add a media item to the playlist"""
        method = 'Playlist.Add'
        params = {'playlistid': 1, 'item': {media.id_str: media.id}}
        self._post(method, params)

    def play(self):
        """play the playlist"""
        method = 'player.open'
        params = {'item': {'playlistid': 1}}
        self._post(method, params)

    def stop(self):
        """stop any playing movie"""
        method = 'Player.Stop'
        params = {'playerid': 1}
        self._post(method, params)

    def library(self, action, showdialogs=True):
        """Clean the library"""
        actions = ['clean', 'scan']
        if action not in actions:
            raise ValueError('action must be one of {}'.format(', '.join(actions)))
        method = 'VideoLibrary.{}'.format(action.capitalize())
        params = {'showdialogs': showdialogs}
        self._post(method, params)
