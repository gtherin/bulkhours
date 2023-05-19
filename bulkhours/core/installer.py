import argparse
import os
import sys
import time
import json

import zlib
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

DEFAULT_TOKEN = "NO_TOKEN"
is_colab = os.path.exists("/content")

# Set up the package directory
bulk_dir = "/content" if is_colab else "/home/guydegnol/projects"


def obscure(data) -> bytes:
    return b64e(zlib.compress(data.encode("utf-8"), 9))


def unobscure(obscured: bytes) -> bytes:
    return zlib.decompress(b64d(obscured)).decode("utf-8")


def get_tokens(promo_token):
    _, nb_key = promo_token.split("::")

    with open(f"{bulk_dir}/bulkhours/data/radian.png") as f:
        TOKENS = f.readline()

    for db_key in TOKENS.split("::"):
        try:
            tokens = unobscure(nb_key.encode("utf-8") + db_key.encode("utf-8"))
            return eval(tokens)
        except:
            pass
    return {}


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
    parser.add_argument("-p", "--packages", default="None")
    parser.add_argument("-f", "--in-french", help="Change languages", action="store_true")
    parser.add_argument("-k", "--openai-token", default=DEFAULT_TOKEN)
    parser.add_argument("-t", "--tokens", default={})

    argv = get_opts("-u", argv)
    openai_token = argv[argv.index("-k") + 1].replace("-", "___") if "-k" in argv else DEFAULT_TOKEN

    argv = parser.parse_args(argv)
    argv.openai_token = openai_token.replace("___", "-")
    argv.tokens = get_tokens(argv.tokens)

    return argv


def install_pkg(pkg, is_colab, args, env_id, start_time):
    if not (f"{pkg}_token" in args.tokens and args.tokens[f"{pkg}_token"] != DEFAULT_TOKEN):
        return
    if is_colab:
        os.system(
            f"cd {bulk_dir} && rm -rf bulkhours_{pkg} 2> /dev/null && git clone https://{args.tokens['{pkg}_token'].replace('/', '_')}@github.com/guydegnol/bulkhours_{pkg}.git --depth 1 > /dev/null 2>&1"
        )

    if os.path.exists(f"{bulk_dir}/bulkhours_{pkg}/"):
        einfo = "🚀" if pkg != "admin" else "⚠️\x1b[41m\x1b[37mfor teachers only\x1b[0m"
        print(
            "\x1b[36mRUN git clone https://github.com/guydegnol/bulkhours_%s.git [%s, %.0fs]\x1b[0m%s"
            % (pkg, env_id, time.time() - start_time, einfo)
        )

    else:
        print(
            f"RUN install bulkhours_{pkg}: installation failed 🚫. Check that your {pkg}_token is still valid (contact: bulkhours@guydegnol.net)"
        )


def main(argv=sys.argv[1:]):
    # Log datetime
    start_time = time.time()
    env_id = "colab" if is_colab else "mock"

    # Get the bulkhours basic package
    print("RUN git clone https://github.com/guydegnol/bulkhours.git [%s, %.0fs]" % (env_id, time.time() - start_time))

    if is_colab:
        os.system(
            f"cd {bulk_dir} && rm -rf bulkhours 2> /dev/null && git clone https://github.com/guydegnol/bulkhours.git --depth 1 > /dev/null 2>&1"
        )

    if not os.path.exists(f"{bulk_dir}/bulkhours/"):
        print("RUN install bulkhours: aborted 💥, package is no more available")
        return

    args = get_install_parser(argv)
    # stime = datetime.datetime.now() + datetime.timedelta(seconds=3600) if is_colab else datetime.datetime.now()
    # print("RUN install bulkhours [%s]" % stime.strftime("%H:%M:%S"))

    # Install main package
    install_pkg("admin", is_colab, args, env_id, start_time)
    install_pkg("premium", is_colab, args, env_id, start_time)

    if args.packages != "None":
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
    data = {"login": args.user, "env": args.env_id, "nid": args.id, "in_french": args.in_french}
    data.update(args.tokens)
    # print("LOG login= %s, id=%s, env=%s [%s, %.0fs]" % (args.user, args.id, args.env_id, env_id, time.time() - start_time))
    with open(f"{bulk_dir}/bulkhours/.safe", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
