import os
import time
import zlib
import subprocess
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from .tools import get_platform

DEFAULT_TOKEN = "NO_TOKEN"


# Set up the package directory
bulk_dir = os.path.abspath(os.path.dirname(__file__) + f"/../../..")


def obscure(data) -> bytes:
    return b64e(zlib.compress(data.encode("utf-8"), 9))


def unobscure(obscured: bytes) -> bytes:
    return zlib.decompress(b64d(obscured)).decode("utf-8")


def get_tokens(token, raise_error=False, verbose=True):
    def unobscure_token(tokens):
        tokens = unobscure(tokens)
        tokens = eval(tokens)
        return {s[0]: s[1] for s in tokens}

    nb_helper, nb_key = token.split("::")
    import glob

    for filename in glob.glob(f"{bulk_dir}/bulkhours/data/radian*.png"):
        with open(filename) as f:
            TOKENS = f.readline()

            for db_key in TOKENS.split("::"):
                ali, baba = db_key.split("__RR__")
                if nb_helper == ali:
                    tokens = nb_key.encode("utf-8") + baba.encode("utf-8")
                    if raise_error:
                        return unobscure_token(tokens)
                    else:
                        try:
                            return unobscure_token(tokens)
                        except:
                            pass
    if verbose:
        print(
            f"""⚠️\x1b[41m\x1b[37mYour token was not found. Check that your token is still valid (contact: contact@bulkhours.eu)\x1b[0m⚠️"""
        )

    return {}


def install_dependencies(packages, start_time, is_admin):
    if start_time is None:
        start_time = time.time()

    if get_platform() == "sagemaker":
        if "CONDA_PREFIX" in os.environ and "sagemaker-distribution" not in os.environ["CONDA_PREFIX"]:
            print(
                f"""⚠️\x1b[33mFor sagemaker, please use the \033[1msagemaker-distribution:Python\x1b[0m\x1b[33m kernel (data science libraries are already installed) \x1b[0m"""
            )
        packages = "graphviz," + packages

    packages = packages.replace(
        "HUGGING_FACE", "swig,cmake,HF_UNIT1,apt-get,python-opengl,ffmpeg,xvfb,pyvirtualdisplay,shimmy>=0.2.1"
    )

    # Set default value
    if packages in [None, "None"]:
        packages = ""

    # Install packages if admin
    if packages == "" and not is_admin:
        return

    # Update pip
    print("\x1b[37mRUN pip/apt install [%s]: " % (get_platform()), end="", flush=True)

    # packages = "swig,cmake,python-opengl,ffmpeg,xvfb,gym==0.25.2,pyvirtualdisplay,stable-baselines3[extra],box2d,box2d-kengz,array2gif,huggingface_sb3,pyglet==1.5.1"
    packages = packages.replace(
        "HUGGING_FACE", "swig,cmake,HF_UNIT1,apt-get,python-opengl,ffmpeg,xvfb,pyvirtualdisplay,shimmy>=0.2.1"
    )
    # if packages in ["rl", "reinforcement learning"]:
    #    rl.init_env(verbose=verbose)

    # Install the xattr package if admin
    if is_admin and ",xattr" not in packages:
        packages += ",xattr"

    # Install packages
    for package in packages.split(","):
        if package == "":
            continue

        status = "0"
        print(package, end="", flush=True)
        if get_platform() == "local":
            status = "0"
        elif package == "pip":
            os.system(f"pip install --upgrade pip > /dev/null 2>&1")
            status = "U"
        elif package == "apt-get":
            os.system(f"sudo apt-get update > /dev/null 2>&1")
            status = "U"
        elif package == "HF_UNIT1":  # stable-baselines3==2.0.0a5,gymnasium[box2d],huggingface_sb3
            os.system(
                f"pip install -r https://raw.githubusercontent.com/huggingface/deep-rl-class/main/notebooks/unit1/requirements-unit1.txt > /dev/null 2>&1"
            )
            status = "M"
        elif package not in "wkhtmltopdf,swig,cmake,python-opengl,ffmpeg,xvfb,git-lfs,xattr".split(","):
            res = subprocess.run(
                f"pip show {package}".split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            ).stdout
            if "not found" in res:
                os.system(f"pip install {package} > /dev/null 2>&1")
                status = "I"
        else:
            os.system(f"apt install {package} > /dev/null 2>&1")
            status = "A"
        print(" [%s,%.0fs]," % (status, time.time() - start_time), end="", flush=True)

    print("\x1b[0m")
