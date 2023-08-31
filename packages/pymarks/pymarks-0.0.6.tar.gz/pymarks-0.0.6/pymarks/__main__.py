from __future__ import annotations

import argparse
import functools
import logging
import sys
from typing import TYPE_CHECKING
from typing import Callable

from pyselector import Menu

from pymarks import actions
from pymarks import constants
from pymarks import database
from pymarks import logger
from pymarks import utils
from pymarks.constants import MENUS
from pymarks.constants import ExitCode
from pymarks.keys import Keybinds

if TYPE_CHECKING:
    from pyselector.interfaces import MenuInterface


log = logging.getLogger(__name__)


def load_menu(name: str) -> tuple[MenuInterface, Callable]:
    menu = Menu.get(name)
    prompt = functools.partial(
        menu.prompt,
        lines=15,
        prompt=f'{constants.APP_NAME}> ',
        width='75%',
        height='50%',
        markup=False,
        mesg=f'Welcome to {constants.APP_NAME}',
    )
    # Register keybinds
    for key in Keybinds:
        menu.keybind.add(*key)
    return menu, prompt


def setup_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=constants.APP_HELP,
        add_help=False,
    )
    parser.add_argument('search', nargs='*')
    parser.add_argument('-m', '--menu', choices=MENUS, default='rofi')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--test', action='store_true')
    parser.add_argument('-V', '--version', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-h', '--help', action='store_true')
    return parser


def parse_args_and_exit(args: argparse.Namespace) -> None:
    if args.version:
        print(constants.APP_NAME, constants.APP_VERSION)
        sys.exit(0)
    if args.help:
        print(constants.APP_HELP)
        sys.exit(0)
    logger.verbose(args.verbose)
    log.debug('args: %s', vars(args))


def main() -> ExitCode:
    utils.setup_project()
    parser = setup_args()
    args = parser.parse_args()
    parse_args_and_exit(args)

    with database.open_database(constants.DB_DEFAULT_FILE) as cursor:
        menu, prompt = load_menu(args.menu)
        records = (
            database.get_bookmarks_by_query(cursor, args.search)
            if args.search
            else database.get_bookmarks_all(cursor)
        )
        items = list(records)
        if not items:
            database.insert_initial_record(cursor)
            items = list(database.get_bookmarks_all(cursor))
        if args.json:
            database.dump_to_json(items)
            return ExitCode(0)
        bookmark = actions.show_bookmarks(cursor, menu, prompt, items)
        database.update_bookmark_last_use(cursor, bookmark.id)
    utils.copy_to_clipboard(bookmark.url)
    return ExitCode(0)


if __name__ == '__main__':
    sys.exit(main())
