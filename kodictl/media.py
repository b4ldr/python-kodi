"""Media type definitions"""


class BaseMedia:
    """A base media class"""
    media = 'base'
    id_str = '{}id'.format(media)

    def __init__(self, raw):
        # TODO: use __getitem__
        self.label = raw['label']
        self.id = raw['{}id'.format(self.media)]
        self._raw = raw

    def __str__(self):
        return '{}: {}'.format(self.media, self.label)


class Movie(BaseMedia):
    """Class for songs"""
    media = 'movie'


class Song(BaseMedia):
    """Class for songs"""
    media = 'song'


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
        return [item for item in self.collection if title in item['label']]


class Movies(BaseCollection):
    """Class to hold a collection of movies"""
    mediaclass = Movie


class Songs(BaseCollection):
    """Class to hold a collection of songs"""
    mediaclass = Song
