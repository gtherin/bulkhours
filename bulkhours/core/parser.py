import argparse
import datetime
import os
import sys
import time
import json


def get_opts(opt_key, opts):
    if opt_key not in opts:
        return opts

    lindex_start = opts.index(opt_key) + 1
    lindex_end = len(opts)
    for i, o in enumerate(opts[lindex_start + 1 :]):
        if len(o) == 2 and o[0] == "-":
            lindex_end = lindex_start + i + 1
            break

    label = " ".join(opts[lindex_start:lindex_end])
    return opts[:lindex_start] + [label] + opts[lindex_end:]


def get_argparser(line, cell):
    parser = argparse.ArgumentParser(description="Evaluation params")
    parser.add_argument("-u", "--user", default=os.environ["STUDENT"] if "STUDENT" in os.environ else None)
    parser.add_argument("-i", "--id", default=None)
    parser.add_argument("-o", "--options", default="")
    parser.add_argument("-l", "--label", type=str, default="")
    parser.add_argument("-t", "--type", default="code")
    parser.add_argument("-x", "--xoptions", default=None)
    parser.add_argument("-w", "--widgets", default=None)
    parser.add_argument("-p", "--puppet", default="")
    parser.add_argument("-d", "--default", default="")

    try:
        opts = line.split()
        opts = get_opts("-l", opts)
        opts = get_opts("-d", opts)
        opts = get_opts("-o", opts)

        args = parser.parse_args(opts)

    except SystemExit as e:
        parser.print_help()
        return None

    if args.widgets is None:
        if args.type == "code_project":
            args.widgets = "w|tsc"
        elif args.type in ["table", "checkboxes"]:
            args.widgets = "lw|sc"
        elif args.type in ["code", "markdown", "formula"]:
            args.widgets = "sc"
        else:
            args.widgets = "lwsc"

    return args

    # from .widgets import check_widget
    # return check_widget(args)
