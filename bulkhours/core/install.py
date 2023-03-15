import argparse
import datetime
import os
import sys
import time
import json


def get_arg_parser(argv):
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
    args = get_arg_parser(argv)

    # Set up a colab flag
    is_colab = os.path.exists("/content")

    if args.pass_phrase != "ARANCINI":
        print("RUN install bulkhours: aborted 💥")
        return

    # Log datetime
    stime = datetime.datetime.now() + datetime.timedelta(seconds=3600) if is_colab else datetime.datetime.now()
    print("RUN install bulkhours [%s]" % stime.strftime("%H:%M:%S"))

    # Set up the package directory
    bulk_dir = "/content" if is_colab else "/home/guydegnol/projects"
    env_id = "mock" if is_colab else "colab"

    # Install main package
    start_time = time.time()
    print("RUN git clone https://github.com/guydegnol/bulkhours.git [%s, %.0fs]" % (env_id, time.time() - start_time))
    if is_colab:
        os.system(
            f"cd {bulk_dir} && rm -rf bulkhours 2> /dev/null && git clone https://github.com/guydegnol/bulkhours.git --depth 1 > /dev/null 2>&1"
        )

    # Update pip
    start_time = time.time()
    print("RUN pip install --upgrade pip [%s, %.0fs]" % (env_id, time.time() - start_time))
    if is_colab:
        os.system(f"pip install --upgrade pip > /dev/null 2>&1")

    # Install packages
    for package in args.packages.split(","):
        start_time = time.time()
        print("RUN pip install %s [%s, %.0fs]" % (package, env_id, time.time() - start_time))
        os.system(f"pip install {package} > /dev/null 2>&1")

    data = {"login": args.user, "pass_code": args.pass_code, "env": args.env_id, "course_version": args.pass_phrase}
    with open(f"{bulk_dir}/bulkhours/.safe", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
