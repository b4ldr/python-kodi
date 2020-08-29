"""Media type definitions"""


class BaseMedia:
    """A base media class"""
    media = 'base'

    def __init__(self, raw):
        # TODO: use __getitem__
        self.id_str = '{}id'.format(self.media)
        self.label = raw.get('label')
        self.id = raw.get(self.id_str)
        self._raw = raw

    def __str__(self):
        return '{} ({}): {}'.format(self.media, self.id, self.label)


class Movie(BaseMedia):
    """Class for songs"""
    media = 'movie'


class Song(BaseMedia):
    """Class for songs"""
    media = 'song'


class TVShow(BaseMedia):
    """Class for songs"""
    media = 'tvshow'


class Addon(BaseMedia):
    """Class for songs"""
    media = 'addon'

    def __str__(self):
        return '{}: {}'.format(self.media, self.id)


class BaseCollection:
    """class to hold a colelction of medias"""
    mediaclass = BaseMedia

    def __init__(self, raw):
        self._raw = raw
        self.collection = []
        self._parse()

    def __iter__(self):
        for item in self.collection:
            yield item

    def _parse(self):
        for entry in self._raw:
            self.collection.append(self.mediaclass(entry))

    def search(self, title):
        return [item for item in self.collection if title.lower() in item.label.lower()]


class Movies(BaseCollection):
    """Class to hold a collection of movies"""
    mediaclass = Movie


class Songs(BaseCollection):
    """Class to hold a collection of songs"""
    mediaclass = Song


class TVShows(BaseCollection):
    """Class to hold a collection of Addons"""
    mediaclass = TVShow


class Addons(BaseCollection):
    """Class to hold a collection of Addons"""
    mediaclass = Addon
