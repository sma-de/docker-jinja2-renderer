#!/usr/bin/env python

import argparse
import logging
import os
import pathlib

import jinja2

if __name__ == '__main__':

    logging.basicConfig(
        datefmt='%Y-%m-%d %H:%M:%S',
        format='%(asctime)s [%(levelname)s] %(message)s'
    )
    logger = logging.getLogger("jinja-renderer")
    logger.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(description='Jina2 template renderer')
    parser.add_argument(
        'path',
        help='Path to a folder containing the templates to process.'
    )
    parser.add_argument(
        '-f',
        help='Files in the destination directory will be overwritten, if they already exist',
        action='store_true'
    )
    parser.add_argument(
        '-r',
        help='Scan for files recursively',
        action='store_true'
    )
    args = parser.parse_args()

    logger.info(f"Working on files in '{args.path}'...")

    files = pathlib.Path(args.path).glob("**/*.j2" if args.r else "*.j2")

    for file_name in files:
        if os.path.islink(file_name):
            logger.warning(f"Skipping symlink '{file_name}'")
            continue

        logger.info(f"Processing '{file_name}'...")

        variables = {
            'file': file_name
        }

        content = pathlib.Path(file_name, encoding='UTF-8').read_text()

        template = jinja2.Template(content)
        rendered = template.render(variables)

        output_file_name = os.path.splitext(file_name)[0]

        logger.info(f"Wiring to '{output_file_name}'...")

        my_file = pathlib.Path(output_file_name, encoding='UTF-8')
        if my_file.is_file() and not args.f:
            logger.error(f"Can't write to existing file '{file_name}'.")
        else:
            my_file.write_text(rendered)
