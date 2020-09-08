#!/usr/bin/env python3
"""script to test lib functionality"""
import logging

from argparse import ArgumentParser

from kodictl import KodiCtl


def get_args():
    """Parse arguments"""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('-H', '--host', default='192.168.1.15')
    parser.add_argument('-P', '--port', default='8080')
    parser.add_argument('-v', '--verbose', action='count')
    parser.add_argument('-p', '--play', action='store_true')
    parser.add_argument('-s', '--stop', action='store_true')
    parser.add_argument('-M', '--list-movies', action='store_true')
    parser.add_argument('-S', '--list-songs', action='store_true')
    parser.add_argument('-T', '--list-tvshows', action='store_true')
    parser.add_argument('-A', '--list-addons', action='store_true')
    parser.add_argument('--clean', action='store_true')
    parser.add_argument('--scan', action='store_true')
    parser.add_argument('--volume', action='store_true')
    parser.add_argument('-V', '--set-volume', type=int)
    parser.add_argument('-R', '--random', action='store_true')
    parser.add_argument('--enable-subtitles', action='store_true')
    parser.add_argument('--disable-subtitles', action='store_true')
    parser.add_argument('--pause', action='store_true')
    parser.add_argument('--unpause', action='store_true')
    parser.add_argument('--mute', action='store_true')
    parser.add_argument('--unmute', action='store_true')
    parser.add_argument('--movie-search')
    parser.add_argument('--music-search')
    parser.add_argument('--tv-search')
    parser.add_argument('--skip', type=int)
    return parser.parse_args()


def get_log_level(args_level):
    """Configure logging"""
    return {
        None: logging.ERROR,
        1: logging.WARN,
        2: logging.INFO,
        3: logging.DEBUG}.get(args_level, logging.DEBUG)


def main():
    """main entry"""
    args = get_args()
    logging.basicConfig(level=get_log_level(args.verbose))
    kctl = KodiCtl(args.host, args.port)
    if args.clean:
        kctl.library('clean')
    if args.scan:
        kctl.library('scan')
    if args.list_movies:
        for item in kctl.movies:
            print(item)
    if args.list_songs:
        for item in kctl.songs:
            print(item)
    if args.list_tvshows:
        for item in kctl.tvshows:
            print(item)
    if args.list_addons:
        for item in kctl.addons:
            print(item)
    if args.enable_subtitles:
        kctl.subtitles = True
    if args.disable_subtitles:
        kctl.subtitles = False
    if args.set_volume:
        kctl.set_volume = args.volume
    if args.pause:
        kctl.pause = True
    if args.unpause:
        kctl.pause = False
    if args.mute:
        print(kctl.muted)
        kctl.muted = True
    if args.unmute:
        print(kctl.muted)
        kctl.muted = False
    if args.play:
        kctl.play()
    if args.stop:
        kctl.stop()
    if args.volume:
        print(kctl.volume)
    if args.movie_search:
        for item in kctl.movies.search(args.movie_search):
            print(item)
        kctl.add_to_playlist(item)
    if args.tv_search:
        for item in kctl.tvshows.search(args.tv_search):
            print(item)
    if args.skip:
        kctl.skip(args.skip)


if __name__ == '__main__':
    raise SystemExit(main())
