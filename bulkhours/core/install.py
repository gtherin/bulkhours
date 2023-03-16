import argparse
import datetime
import os
import sys
import time
import json


def get_argparser(line, cell):
    argparser = argparse.ArgumentParser(description="Evaluation params")
    argparser.add_argument("-u", "--user", default=os.environ["STUDENT"] if "STUDENT" in os.environ else None)
    argparser.add_argument("-i", "--id", default=None)
    argparser.add_argument("-o", "--options", default="")
    argparser.add_argument("-l", "--label", type=str, default=None)
    argparser.add_argument("-t", "--type", default="code")
    argparser.add_argument("-x", "--xoptions", default=None)

    try:
        opts = line.split()

        if "-l" in opts:
            lindex_start = opts.index("-l") + 1
            lindex_end = len(opts)
            for i, o in enumerate(opts[lindex_start + 1 :]):
                if len(o) == 2 and o[0] == "-":
                    lindex_end = lindex_start + i + 1
                    break

            label = " ".join(opts[lindex_start:lindex_end])
            args = argparser.parse_args(opts[:lindex_start] + ["LABEL"] + opts[lindex_end:])
            args.label = label  # Set label
        else:
            args = argparser.parse_args(opts)

        # args.xoptions = {
        #    a.split(":")[0]: cell if a.split(":")[1] == "CELL" else a.split(":")[1] for a in args.options.split(";")
        # }

    except SystemExit as e:
        argparser.print_help()
        return None

    return args


def get_install_parser(argv):
    parser = argparse.ArgumentParser(
        description="Installation script evaluation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-u", "--user", default=None)
    parser.add_argument("-x", "--pass-code", help="Pass code", default=None)
    parser.add_argument("-X", "--pass-phrase", help="Pass code", default=None)
    parser.add_argument("-e", "--env-id", help=f"Environnment id")
    parser.add_argument("-i", "--id", default=None)
    parser.add_argument("-p", "--packages", default="")

    return parser.parse_args(argv)


def main(argv=sys.argv[1:]):
    args = get_install_parser(argv)

    # Set up a colab flag
    is_colab = os.path.exists("/content")

    if args.pass_phrase != "POLPETTE":
        print("RUN install bulkhours: aborted 💥, package is no more available")
        return

    # Log datetime
    start_time = time.time()
    stime = datetime.datetime.now() + datetime.timedelta(seconds=3600) if is_colab else datetime.datetime.now()
    print("RUN install bulkhours [%s]" % stime.strftime("%H:%M:%S"))

    # Set up the package directory
    bulk_dir = "/content" if is_colab else "/home/guydegnol/projects"
    env_id = "mock" if is_colab else "colab"

    # Install main package
    print("RUN git clone https://github.com/guydegnol/bulkhours.git [%s, %.0fs]" % (env_id, time.time() - start_time))
    if is_colab:
        os.system(
            f"cd {bulk_dir} && rm -rf bulkhours 2> /dev/null && git clone https://github.com/guydegnol/bulkhours.git --depth 1 > /dev/null 2>&1"
        )

    # Update pip
    print("RUN pip install --upgrade pip [%s, %.0fs]" % (env_id, time.time() - start_time))
    if is_colab:
        os.system(f"pip install --upgrade pip > /dev/null 2>&1")

    # Install packages
    for package in args.packages.split(","):
        print("RUN pip install %s [%s, %.0fs]" % (package, env_id, time.time() - start_time))
        os.system(f"pip install {package} > /dev/null 2>&1")

    # Dump env variables
    data = {
        "login": args.user,
        "pass_code": args.pass_code,
        "env": args.env_id,
        "nid": args.id,
        "course_version": args.pass_phrase,
    }
    print(
        "LOG login=%s, id=%s, env=%s [%s, %.0fs]" % (args.user, args.id, args.env_id, env_id, time.time() - start_time)
    )
    with open(f"{bulk_dir}/bulkhours/.safe", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
