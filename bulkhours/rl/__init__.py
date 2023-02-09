import sys
import matplotlib.pyplot as plt


def runrealcmd(command, verbose=True):
    from subprocess import Popen, PIPE, STDOUT

    process = Popen(command, stdout=PIPE, shell=True, stderr=STDOUT, bufsize=1, close_fds=True)
    if verbose:
        for line in iter(process.stdout.readline, b""):
            print(line.rstrip().decode("utf-8"))
    process.stdout.close()
    process.wait()


def init_env(ip):
    """Use pip from the current kernel"""
    import tensorflow as tf

    print("AAAAAAAA", sys.modules)
    if "google.colab" in sys.modules:
        # runrealcmd("sudo apt-get update", verbose=True)
        runrealcmd("sudo apt install swig cmake", verbose=True)
        runrealcmd("sudo apt-get install -y xvfb python-opengl, ffmpeg", verbose=True)
        # runrealcmd("pip install gymnasium pyvirtualdisplay array2gif", verbose=True)
        # runrealcmd("pip install gymnasium[atari,toy_text,box2d,classic_control,accept-rom-license]", verbose=True)
        runrealcmd("pip install gym stable-baselines3[extra] box2d box2d-kengz", verbose=True)
        runrealcmd("pip install huggingface_sb3 pyglet==1.5.1", verbose=True)

    if not tf.config.list_physical_devices("GPU"):
        print("No GPU was detected. Neural nets can be very slow without a GPU.")
        if "google.colab" in sys.modules:
            print("Go to Runtime > Change runtime and select a GPU hardware accelerator.")
        if "kaggle_secrets" in sys.modules:
            print("Go to Settings > Accelerator and select GPU.")

    plt.rc("font", size=14)
    plt.rc("axes", labelsize=14, titlesize=14)
    plt.rc("legend", fontsize=14)
    plt.rc("xtick", labelsize=10)
    plt.rc("ytick", labelsize=10)
    plt.rc("animation", html="jshtml")


def plot_environment(env, figsize=(5, 4)):
    plt.figure(figsize=figsize)
    img = env.render()
    if type(img) == list:
        img = img[0]
    plt.imshow(img)
    plt.axis("off")
    plt.show()
    return img
