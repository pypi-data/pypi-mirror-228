from __future__ import annotations

import argparse
import os.path
import sys
from collections.abc import Sequence
from typing import Any

import jinja2

from .commands.diff import Differ
from .commands.write import Writer
from .config import TemplateConfig
from .config import YamlParser
from .files import DryRunFileWriter
from .files import FileSystem
from .logging import StdErrColorLogger
from .logging import StdErrLogger
from .printers import PagerPrinter
from .printers import StdOutPrinter
from .rendering import Jinja2Renderer


def _get_logger() -> StdErrColorLogger | StdErrLogger:
    use_color = os.getenv('NO_COLOR') in (None, '', '0')
    if use_color:
        return StdErrColorLogger()
    else:
        return StdErrLogger()


def _load_template_config(path: str) -> TemplateConfig:
    parser = YamlParser()

    with open(os.path.expanduser(path)) as f:
        content = f.read()

    return parser.parse_template_config(content)


def _load_context(path: str) -> dict[str, Any]:
    parser = YamlParser()

    with open(os.path.expanduser(path)) as f:
        content = f.read()

    return parser.parse_context(content)


def _get_renderer(
        template_config: TemplateConfig, context: dict[str, Any],
) -> Jinja2Renderer:
    loader = jinja2.FileSystemLoader([template_config.root_dir])
    return Jinja2Renderer(loader=loader, context=context)


def write(
        *,
        template_config_path: str, context_file_path: str,
        dry_run: bool, force: bool,
) -> int:
    template_config = _load_template_config(template_config_path)
    context = _load_context(context_file_path)

    renderer = _get_renderer(template_config, context)

    logger = _get_logger()

    file_system: FileSystem | DryRunFileWriter
    if dry_run:
        logger.info('dry-run: no files will be written')
        file_system = DryRunFileWriter()
    else:
        file_system = FileSystem()

    writer = Writer(renderer, file_system, logger)
    writer.write(template_config, skip_if_exists=not force)

    return 0


def diff(
        *,
        template_config_path: str, context_file_path: str,
        pager: str | None,
) -> int:
    template_config = _load_template_config(template_config_path)
    context = _load_context(context_file_path)

    reader = FileSystem()
    renderer = _get_renderer(template_config, context)

    printer: StdOutPrinter | PagerPrinter
    if pager:
        printer = PagerPrinter(pager)
    else:
        printer = StdOutPrinter()

    differ = Differ(reader, renderer, printer)
    differ.print_diff(template_config)

    return 0


def main(argv: Sequence[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]

    parser = argparse.ArgumentParser(prog='write-config-files')
    subparsers = parser.add_subparsers(dest='command')

    def _add_cmd(name: str, *, help: str) -> argparse.ArgumentParser:
        parser = subparsers.add_parser(name, help=help)
        parser.add_argument(
            '-t', '--templates',
            default='templates.yaml',
            help='path to config file (default: %(default)s)',
        )
        parser.add_argument(
            '-c', '--context',
            default='context.yaml',
            help='path to context file (default: %(default)s)',
        )
        return parser

    write_parser = _add_cmd('write', help='write the config files')
    write_parser.add_argument(
        '-f', '--force',
        action='store_true',
        help='overwrite existing files',
    )
    write_parser.add_argument(
        '-d', '--dry-run',
        action='store_true',
        help='render templates but do not write files',
    )

    diff_parser = _add_cmd('diff', help='show which files have changed')
    diff_parser.add_argument(
        '-p', '--pager',
        help='the pager to use to display each diff (default: no pager)',
    )

    args = parser.parse_args(argv)

    if args.command == 'write':
        return write(
            template_config_path=args.templates,
            context_file_path=args.context,
            dry_run=args.dry_run,
            force=args.force,
        )
    elif args.command == 'diff':
        return diff(
            template_config_path=args.templates,
            context_file_path=args.context,
            pager=args.pager,
        )
    else:
        raise NotImplementedError(f'unrecognised command: {args.command!r}')
