# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4; encoding:utf-8 -*-
#
# Copyright 2022 Kenneth Loafman <kenneth@loafman.com>
#
# This file is part of duplicity.
#
# Duplicity is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# Duplicity is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with duplicity; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

"""
Main for parse command line, check for consistency, and set config
"""
import argparse
import copy
import sys
import inspect

from duplicity import backend
from duplicity import cli_util
from duplicity import config
from duplicity import gpg
from duplicity import log
from duplicity import path
from duplicity import util
from duplicity.cli_data import *
from duplicity.cli_util import *


class DuplicityHelpFormatter(argparse.ArgumentDefaultsHelpFormatter,
                             argparse.RawDescriptionHelpFormatter):
    """
    A working class to combine ArgumentDefaults, RawDescription.
    Use with make_wide() to insure we catch argparse API changes.
    """


def make_wide(formatter, w=120, h=46):
    """
    Return a wider HelpFormatter, if possible.
    See: https://stackoverflow.com/a/5464440
    Beware: "Only the name of this class is considered a public API."
    """
    try:
        kwargs = {'width': w, 'max_help_position': h}
        formatter(None, **kwargs)
        return lambda prog: formatter(prog, **kwargs)
    except TypeError:
        warnings.warn("argparse help formatter failed, falling back.")
        return formatter


def harvest_namespace(args):
    """
    Copy all arguments and their values to the config module.  Don't copy
    attributes that are 'hidden' (start with an underscore) or whose name is
    the empty string (used for arguments that don't directly store a value
    by using dest="")
    """
    for f in [x for x in dir(args) if x and not x.startswith("_")]:
        v = getattr(args, f)
        setattr(config, f, v)


def parse_implied_command(arglist):
    """
    Add implied commands if
    - no or wrong command was given
    - number of positional arguments is 2
    - the order of positional arguments implies backup (2nd is url) or restore (first is url)
    Check if there is a valid action command or throw command line error
    """
    parser = argparse.ArgumentParser(
        prog='duplicity',
        add_help=False,
        argument_default=None)

    # add dummy -h and --help
    parser.add_argument("-h", "--help", action="store_true")

    # add all known options
    for opt in all_options:
        var = opt2var(opt)
        names = [opt] + OptionAliases.__dict__.get(var, [])
        # arparse store and friends define nargs, so we keep em
        # strip actually config retrieving action classes _and_ type functions checking validity
        selected_args_only = {
            k: (
                v
                if not (inspect.isclass(v) and issubclass(v, argparse.Action))
                else DoNothingAction
            )
            for k, v in OptionKwargs.__dict__[var].items()
            if k not in {'type'}
        }
        # needed as store action does not tolerate nargs=0, we do not want to interpret just now anyway
        parser.add_argument(*names, **selected_args_only)

    # strip known arguments should leave us with pos_args only and unknown options paramters unfortunately
    args, remainder = parser.parse_known_args(arglist)

    # let's test the action command and try to assume,
    # eventually err out if no valid action could be determined/was given
    if len(remainder) > 0 and remainder[0] not in all_commands:
        if len(remainder) == 2 and is_path(remainder[0]) and is_url(remainder[1]):
            log.Notice(_("No valid action command found. Will imply 'backup' because "
                         "a path source was given and target is a url location."))
            arglist.insert(0, 'backup')
            # config.inc_explicit = False
        elif len(remainder) == 2 and is_url(remainder[0]) and is_path(remainder[1]):
            log.Notice(_("No valid action command found. Will imply 'restore' because "
                         "url source was given and target is a local path."))
            arglist.insert(0, 'restore')
        else:
            remainder_string = ', '.join(f"'{c}'" for c in remainder)
            all_long_commands = set()
            for var, aliases in CommandAliases.__dict__.items():
                if var.startswith("__") or len(var) <= 2:
                    continue
                all_long_commands.add(var2cmd(var))
            all_long_commands_string = ', '.join(f"'{c}'" for c in sorted(all_long_commands))
            msg = _("Invalid or missing action command and cannot be implied from the "
                    f"given arguments. {remainder_string}\n"
                    f"Valid action commands are: {all_long_commands_string}")
            command_line_error(msg)


def pre_parse_cmdline_options(arglist):
    """
    Parse the commands and options that need to be handled first.
    Everthing else is passed on to the main parser.
    """
    # set up parent parser
    parser = argparse.ArgumentParser(
        prog='duplicity',
        add_help=False,
        argument_default=None)

    # add parent_only options to the parser
    for opt in sorted(parent_only_options):
        var = opt2var(opt)
        names = [opt] + OptionAliases.__dict__.get(var, [])
        parser.add_argument(*names, **OptionKwargs.__dict__[var])

    # process parent args now
    args, remainder = parser.parse_known_args(arglist)

    # harvest args to config
    harvest_namespace(args)

    return args, remainder


def parse_cmdline_options(arglist):
    """
    Parse remaining argument list once all is defined.
    """
    # fixup implied commands
    parse_implied_command(arglist)

    # preprocess config type args
    args, remain = pre_parse_cmdline_options(arglist)

    # set up parent parser
    parser = argparse.ArgumentParser(
        prog='duplicity',
        argument_default=None,
        formatter_class=make_wide(DuplicityHelpFormatter))

    # add all options to the parser
    for opt in sorted(all_options):
        var = opt2var(opt)
        names = [opt] + OptionAliases.__dict__.get(var, [])
        parser.add_argument(*names, **OptionKwargs.__dict__[var])

    # add changed options to the parser
    for opt in sorted(changed_options):
        parser.add_argument(opt,
                            nargs=0,
                            action=ChangedOptionAction,
                            help=argparse.SUPPRESS)

    # add deprecated options to the parser
    for opt in sorted(deprecated_options):
        parser.add_argument(opt,
                            nargs=0,
                            action=DeprecationAction,
                            help=argparse.SUPPRESS)

    # set up command subparsers
    subparsers = parser.add_subparsers(
        title=_("Valid action commands"),
        required=False)

    # add sub_parser for each command
    subparser_dict = dict()
    for var, meta in sorted(DuplicityCommands.__dict__.items()):
        if var.startswith("__"):
            continue
        cmd = var2cmd(var)
        subparser_dict[cmd] = subparsers.add_parser(
            cmd,
            aliases=CommandAliases.__dict__[var],
            help=f"# duplicity {var} [options] {u' '.join(meta)}",
            formatter_class=make_wide(DuplicityHelpFormatter),
            epilog=help_url_formats,
        )
        subparser_dict[cmd].add_argument(
            dest="action",
            action="store_const",
            const=cmd)
        for arg in meta:
            func = getattr(cli_util, f"check_{arg}")
            subparser_dict[cmd].add_argument(arg, type=func)

        # add valid options for each command
        for opt in sorted(CommandOptions.__dict__[var]):
            var = opt2var(opt)
            names = [opt] + OptionAliases.__dict__.get(var, [])
            subparser_dict[cmd].add_argument(*names, **OptionKwargs.__dict__[var])

    # parse the options
    args = parser.parse_args(remain)

    # if no command, print general help
    if not hasattr(args, "action"):
        parser.print_usage()
        sys.exit(2)

    # harvest args to config
    harvest_namespace(args)

    return args


def process_command_line(cmdline_list):
    """
    Process command line, set config
    """
    # build initial gpg_profile
    config.gpg_profile = gpg.GPGProfile()

    # parse command line
    args = parse_cmdline_options(cmdline_list)

    # if we get a different gpg-binary from the commandline then redo gpg_profile
    if config.gpg_binary is not None:
        src = copy.deepcopy(config.gpg_profile)
        config.gpg_profile = gpg.GPGProfile(
            passphrase=src.passphrase,
            sign_key=src.sign_key,
            recipients=src.recipients,
            hidden_recipients=src.hidden_recipients)
    else:
        config.gpg_binary = util.which('gpg')
    gpg_version = ".".join(map(str, config.gpg_profile.gpg_version))
    log.Info(_(f"GPG binary is {config.gpg_binary}, version {gpg_version}"))

    # shorten incremental to inc
    config.action = "inc" if config.action == "incremental" else config.action

    # import all backends and determine which one we use
    backend.import_backends()
    remote_url = config.source_url or config.target_url
    if remote_url:
        config.backend = backend.get_backend(remote_url)
    else:
        config.backend = None

    # determine full clean local path
    local_path = config.source_path or config.target_dir
    if local_path:
        config.local_path = path.Path(path.Path(local_path).get_canonical())
    else:
        config.local_path = None

    # generate backup name and set up archive dir
    if config.backup_name is None:
        config.backup_name = generate_default_backup_name(remote_url)
    set_archive_dir(expand_archive_dir(config.archive_dir,
                                       config.backup_name))

    # count is only used by the remove-* commands
    config.keep_chains = config.count

    # selection only applies to certain commands
    if config.action in ["backup", 'full', 'inc', 'verify']:
        set_selection()

    # print derived info
    log.Info(_(f"Using archive dir: {config.archive_dir_path.uc_name}"))
    log.Info(_(f"Using backup name: {config.backup_name}"))

    return config.action


if __name__ == "__main__":
    import types
    log.setup()
    action = process_command_line(sys.argv[1:])
    for a, v in sorted(config.__dict__.items()):
        if a.startswith("_") or isinstance(config.__dict__[a], types.ModuleType):
            continue
        print(f"{a} = {v} ({type(config.__dict__[a])})")
