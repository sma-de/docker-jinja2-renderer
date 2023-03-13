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
        '-f', '--force',
        help='Files in the destination directory will be overwritten, if they already exist',
        action='store_true'
    )

    parser.add_argument(
        '-r',
        help='Scan for files recursively',
        action='store_true'
    )

    parser.add_argument(
        '-i', '--include-templates-dir',
        help='Directories where to load jinja template from',
        action='append',
        dest="template_include_dirs",
    )

    args = parser.parse_args()

    logger.info(f"Working on files in '{args.path}'...")

    files = pathlib.Path(args.path).glob("**/*.j2" if args.r else "*.j2")

    incdirs = []

    if args.template_include_dirs:
        for d in args.template_include_dirs:
            if not os.path.isabs(d):
                d = os.path.join(os.getcwd(), d)

            incdirs.append(d)

        logger.info(
          f"Files inside following dirs will be avaible as"\
           " imports/includes inside jinja template:"
        )

        logger.info("  {}".format(','.join(incdirs)))

    for f in files:

        is_incfile = False

        for inc in incdirs:
            if f.is_relative_to(inc):
                logger.warning(f"Skipping include dir file '{f}'")
                is_incfile = True
                break

        if is_incfile:
            continue

        if f.is_symlink():
            logger.warning(f"Skipping symlink '{f}'")
            continue

        logger.info(f"Processing '{f}'...")

        variables = {
            'file': str(f)
        }

        content = pathlib.Path(f, encoding='UTF-8').read_text()

        if incdirs:
            template = jinja2.Environment(
               loader=jinja2.FileSystemLoader(incdirs)
            ).from_string(content)
        else:
            template = jinja2.Template(content)

        rendered = template.render(variables)

        output_file_name = os.path.splitext(f)[0]

        logger.info(f"Wiring to '{output_file_name}'...")

        my_file = pathlib.Path(output_file_name, encoding='UTF-8')
        if my_file.is_file() and not args.force:
            logger.error(f"Can't write to existing file '{f}'.")
        else:
            my_file.write_text(rendered)
