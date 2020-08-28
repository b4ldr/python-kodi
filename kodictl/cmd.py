#!/usr/bin/env python3
import logging

from argparse import ArgumentParser

from kodictl import KodiCtl


def get_args():
    """Parse arguments"""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('-H', '--host', default='192.168.1.15')
    parser.add_argument('-p', '--port', default='8080')
    parser.add_argument('-v', '--verbose', action='count')
    parser.add_argument('-M', '--list-movies', action='store_true')
    parser.add_argument('-S', '--list-songs', action='store_true')
    parser.add_argument('-V', '--volume', type=int)
    parser.add_argument('--enable-subtitles', action='store_true')
    parser.add_argument('--disable-subtitles', action='store_true')
    parser.add_argument('--pause', action='store_true')
    parser.add_argument('--unpause', action='store_true')
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
    if args.list_movies:
        for movie in kctl.movies:
            print(movie)
    if args.list_songs:
        for song in kctl.songs:
            print(song)
    if args.enable_subtitles:
        kctl.subtitles = True
    if args.disable_subtitles:
        kctl.subtitles = False
    if args.volume:
        kctl.volume = args.volume
    if args.pause:
        kctl.pause = True
    if args.unpause:
        kctl.pause = False


if __name__ == '__main__':
    raise SystemExit(main())
