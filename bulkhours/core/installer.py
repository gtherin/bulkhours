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


def get_tokens(token):
    if "::" not in token:  # Invalid token
        return {}

    _, nb_key = token.split("::")

    with open(f"{bulk_dir}/bulkhours/data/radian2.png") as f:
        TOKENS = f.readline()

    for db_key in TOKENS.split("::"):
        try:
            tokens = unobscure(nb_key.encode("utf-8") + db_key.encode("utf-8"))
            tokens = eval(tokens)
            return {s[0]: s[1] for s in tokens}
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


def format_opt(label, raw2norm=True):
    rr = {"-": "__minus__", "@": "__at__", " ": "__space__", "/": "__slash__"}
    if len(label) > 0 and label[0] != "-":
        for k, v in rr.items():
            label = label.replace(k, v) if raw2norm else label.replace(v, k)
    return label


def format_opts(argv):
    nargv = []
    for a in argv:
        if a[0] != "-" and nargv[-1][0] != "-":
            nargv[-1] += " " + a
        else:
            nargv.append(a)
    return [format_opt(a) for a in nargv]


def get_install_parser(argv):
    parser = argparse.ArgumentParser(
        description="Installation script", formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-p", "--packages", default="None")
    parser.add_argument("-k", "--openai-token", default=DEFAULT_TOKEN)
    parser.add_argument("-t", "--tokens", default={})
    parser.add_argument("-d", "--debug", action="store_true")

    argv = parser.parse_args(format_opts(argv))
    for k in ["packages", "openai_token", "tokens"]:
        if getattr(argv, k):
            setattr(argv, k, format_opt(getattr(argv, k), raw2norm=False))

    argv.tokens = get_tokens(argv.tokens)

    return argv


def install_pkg(pkg, is_colab, tokens, env_id, start_time, debug):
    if not (f"{pkg}_token" in tokens and (token := tokens[f"{pkg}_token"]) != DEFAULT_TOKEN):
        return
    if is_colab:
        os.system(
            f"cd {bulk_dir} && rm -rf bulkhours_{pkg} 2> /dev/null && git clone https://{token.replace('/', '_')}@github.com/guydegnol/bulkhours_{pkg}.git --depth 1 > /dev/null 2>&1"
        )
    if debug:
        print(f"git clone https://{token.replace('/', '_')}@github.com/guydegnol/bulkhours_{pkg}.git --depth 1")

    if os.path.exists(f"{bulk_dir}/bulkhours_{pkg}/"):
        if 0:
            einfo = "🚀" if pkg != "admin" else "⚠️\x1b[41m\x1b[37mfor teachers only\x1b[0m"
            color = "\x1b[36mRUN git clone " if pkg != "admin" else "\x1b[31mRUN git clone "

            print(
                "%shttps://github.com/guydegnol/bulkhours_%s.git [%s, %.0fs]\x1b[0m%s"
                % (color, pkg, env_id, time.time() - start_time, einfo)
            )

    else:
        print(
            f"RUN install bulkhours_{pkg}: installation failed 🚫. Check that your {pkg}_token is still valid (contact: bulkhours@guydegnol.net)"
        )


def install_dependencies(packages, start_time, debug):
    if packages in [None, "None", ""]:
        return

    if start_time is None:
        start_time = time.time()

    env_id = "colab" if is_colab else "mock"

    # Update pip
    print("\x1b[37mRUN pip/apt install [%s]: " % (env_id), end="", flush=True)

    # packages = "swig,cmake,python-opengl,ffmpeg,xvfb,gym==0.25.2,pyvirtualdisplay,stable-baselines3[extra],box2d,box2d-kengz,array2gif,huggingface_sb3,pyglet==1.5.1"
    packages = packages.replace(
        "HUGGING_FACE", "swig,cmake,HF_UNIT1,apt-get,python-opengl,ffmpeg,xvfb,pyvirtualdisplay,shimmy>=0.2.1"
    )
    # if packages in ["rl", "reinforcement learning"]:
    #    rl.init_env(verbose=verbose)

    # Install packages
    for package in packages.split(","):
        print("%s [%.0fs]," % (package, time.time() - start_time), end="", flush=True)
        if not is_colab:
            continue

        if package == "pip":
            os.system(f"pip install --upgrade pip > /dev/null 2>&1")
        elif package == "apt-get":
            os.system(f"sudo apt-get update > /dev/null 2>&1")
        elif package == "HF_UNIT1":  # stable-baselines3==2.0.0a5,gymnasium[box2d],huggingface_sb3
            os.system(
                f"pip install -r https://raw.githubusercontent.com/huggingface/deep-rl-class/main/notebooks/unit1/requirements-unit1.txt > /dev/null 2>&1"
            )
        elif package not in "wkhtmltopdf,swig,cmake,python-opengl,ffmpeg,xvfb".split(","):
            os.system(f"pip install {package} > /dev/null 2>&1")
        else:
            os.system(f"apt install {package} > /dev/null 2>&1")
    print("\x1b[0m")


def main(argv=sys.argv[1:]):
    # Log datetime
    start_time = time.time()
    env_id = "colab" if is_colab else "mock"

    # Get the bulkhours basic package
    print(
        "RUN git clone https://github.com/guydegnol/bulkhours.git [%s, %.0fs, 16:12]"
        % (env_id, time.time() - start_time)
    )

    if is_colab:
        os.system(
            f"cd {bulk_dir} && rm -rf bulkhours 2> /dev/null && git clone https://github.com/guydegnol/bulkhours.git --depth 1 > /dev/null 2>&1"
        )

    if not os.path.exists(f"{bulk_dir}/bulkhours/"):
        print("RUN install bulkhours: failed 💥")
        return

    args = get_install_parser(argv)

    # Install main package
    install_pkg("admin", is_colab, args.tokens, env_id, start_time, args.debug)
    install_pkg("premium", is_colab, args.tokens, env_id, start_time, args.debug)
    install_dependencies(args.packages, start_time, args.debug)

    # Dump env variables
    with open(f"{bulk_dir}/bulkhours/.safep", "w", encoding="utf-8") as f:
        json.dump(args.tokens, f, ensure_ascii=False, indent=4)
        if args.debug:
            print(args.tokens)


if __name__ == "__main__":
    main()
