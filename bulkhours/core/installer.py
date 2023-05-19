import argparse
import os
import sys
import time
import json

DEFAULT_TOKEN = "NO_TOKEN"


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


def get_install_parser(argv):
    parser = argparse.ArgumentParser(
        description="Installation script evaluation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-u", "--user", default=None)
    parser.add_argument("-e", "--env-id", help=f"Environnment id")
    parser.add_argument("-i", "--id", default=None)
    parser.add_argument("-p", "--packages", default="")
    parser.add_argument("-f", "--in-french", help="Change languages", action="store_true")
    parser.add_argument("-k", "--api-key", default=DEFAULT_TOKEN)
    parser.add_argument("-t", "--tokens", default=DEFAULT_TOKEN)

    argv = get_opts("-u", argv)
    api_key = argv[argv.index("-k") + 1] if "-k" in argv else DEFAULT_TOKEN
    token = argv[argv.index("-t") + 1] if "-t" in argv else DEFAULT_TOKEN
    atoken = argv[argv.index("-a") + 1] if "-a" in argv else DEFAULT_TOKEN
    mtoken = argv[argv.index("-m") + 1] if "-m" in argv else DEFAULT_TOKEN
    pass_code = argv[argv.index("-x") + 1] if "-x" in argv else DEFAULT_TOKEN

    if "-k" in argv:
        argv[argv.index("-k") + 1] = DEFAULT_TOKEN
    if "-t" in argv:
        argv[argv.index("-t") + 1] = DEFAULT_TOKEN
    if "-a" in argv:
        argv[argv.index("-a") + 1] = DEFAULT_TOKEN
    if "-m" in argv:
        argv[argv.index("-m") + 1] = DEFAULT_TOKEN
    if "-x" in argv:
        argv[argv.index("-x") + 1] = DEFAULT_TOKEN

    argv = parser.parse_args(argv)
    argv.api_key = "sk-" + api_key.split(":sk-")[-1] if ":sk-" in api_key else api_key
    argv.pass_code = pass_code.split(":skar_")[-1]
    argv.token = token.replace("/", ",,")
    argv.atoken = atoken.replace("/", ",,")
    argv.mtoken = mtoken.replace("/", ",,")

    return argv


def main(argv=sys.argv[1:]):
    args = get_install_parser(argv)

    # Set up a colab flag
    is_colab = os.path.exists("/content")

    # Log datetime
    start_time = time.time()
    # stime = datetime.datetime.now() + datetime.timedelta(seconds=3600) if is_colab else datetime.datetime.now()
    # print("RUN install bulkhours [%s]" % stime.strftime("%H:%M:%S"))

    # Set up the package directory
    bulk_dir = "/content" if is_colab else "/home/guydegnol/projects"
    env_id = "colab" if is_colab else "mock"

    # Install main package
    if is_colab:
        if args.atoken != DEFAULT_TOKEN:
            os.system(
                f"cd {bulk_dir} && rm -rf bulkhours_admin 2> /dev/null && git clone https://{args.atoken}@github.com/guydegnol/bulkhours_admin.git --depth 1 > /dev/null 2>&1"
            )
            if os.path.exists(f"{bulk_dir}/bulkhours_admin/"):
                print(
                    "\x1b[31mRUN git clone https://github.com/guydegnol/bulkhours_admin.git [%s, %.0fs]\x1b[0m⚠️\x1b[41m\x1b[37mfor teachers only\x1b[0m"
                    % (env_id, time.time() - start_time)
                )
            else:
                print(
                    "RUN install bulkhours_admin: installation failed 🚫. Check that your atoken is still valid (contact: bulkhours@guydegnol.net)"
                )

        if args.mtoken != DEFAULT_TOKEN:
            os.system(
                f"cd {bulk_dir} && rm -rf bulkhours_premium 2> /dev/null && git clone https://{args.mtoken}@github.com/guydegnol/bulkhours_premium.git --depth 1 > /dev/null 2>&1"
            )
            if not os.path.exists(f"{bulk_dir}/bulkhours_premium/"):
                print(
                    "RUN install bulkhours_premium: installation failed 🚫. Check that your mtoken is still valid (contact: bulkhours@guydegnol.net)"
                )
            else:
                print(
                    "\x1b[36mRUN git clone https://github.com/guydegnol/bulkhours_premium.git [%s, %.0fs]\x1b[0m🚀"
                    % (env_id, time.time() - start_time)
                )

        print(
            "RUN git clone https://github.com/guydegnol/bulkhours.git [%s, %.0fs]" % (env_id, time.time() - start_time)
        )
        os.system(
            f"cd {bulk_dir} && rm -rf bulkhours 2> /dev/null && git clone https://{args.token}@github.com/guydegnol/bulkhours.git --depth 1 > /dev/null 2>&1"
        )

    if not os.path.exists(f"{bulk_dir}/bulkhours/"):
        print("RUN install bulkhours: aborted 💥, package is no more available")
        return

    if args.packages != "":
        # Update pip
        print("\x1b[37mRUN pip install [%s]: pip [%.0fs]" % (env_id, time.time() - start_time), end="", flush=True)
        if is_colab:
            os.system(f"pip install --upgrade pip > /dev/null 2>&1")

        # Install packages
        for package in args.packages.split(","):
            if package not in ["wkhtmltopdf"]:
                print(", %s [%.0fs]" % (package, time.time() - start_time), end="", flush=True)
                os.system(f"pip install {package} > /dev/null 2>&1")
            else:
                print(", %s [apt, %.0fs]" % (package, time.time() - start_time), end="", flush=True)
                os.system(f"apt install {package} > /dev/null 2>&1")
        print("\x1b[0m")

    # Dump env variables
    data = {
        "login": args.user,
        "pass_code": args.pass_code,
        "atoken": args.atoken,
        "mtoken": args.mtoken,
        "promo": args.promo,
        "env": args.env_id,
        "nid": args.id,
        "in_french": args.in_french,
        "api_key": args.api_key,
    }
    with open(f"{bulk_dir}/bulkhours/.safe", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
