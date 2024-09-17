import numpy as np
import sys
import subprocess
import matplotlib.pyplot as plt

from . import lxmert  # noqa: F401
from .rl.hugs import PPOHugs  # noqa
from .viz import vizualize  # noqa

def runrealcmd(command, verbose=True):
    logfile = open("install.log", "w")
    stdout, stderr = subprocess.PIPE, subprocess.STDOUT
    stdout, stderr = logfile, logfile
    process = subprocess.Popen(command, stdout=stdout, shell=True, stderr=stderr, bufsize=1, close_fds=True)
    if verbose:
        print(f"RUN {command}")
    process.wait()


def init_env(verbose=True):
    """Use pip from the current kernel"""
    import tensorflow as tf

    if "google.colab" in sys.modules:
        # runrealcmd("sudo apt-get update", verbose=verbose)
        runrealcmd("sudo apt install swig cmake", verbose=verbose)
        runrealcmd("sudo apt-get install -y python-opengl ffmpeg", verbose=verbose)
        runrealcmd("pip install gym", verbose=verbose)
        runrealcmd("apt update && apt install xvfb && pip3 install pyvirtualdisplay && pip install pyvirtualdisplay")
        runrealcmd("pip install stable-baselines3[extra] box2d box2d-kengz array2gif", verbose=verbose)
        runrealcmd("pip install huggingface_sb3 pyglet==1.5.1", verbose=verbose)

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


def linear_forward_test():
    np.random.seed(3)
    """
    X = np.array([[-1.02387576, 1.12397796],
 [-1.62328545, 0.64667545],
 [-1.74314104, -0.59664964]])
    W = np.array([[ 0.74505627, 1.97611078, -1.24412333]])
    b = np.array([[1]])
    """
    A = np.random.randn(3, 2)
    W = np.random.randn(1, 3)
    b = np.random.randn(1, 1)

    return A, W, b


def forward_one_test():
    """
       X = np.array([[-1.02387576, 1.12397796],
    [-1.62328545, 0.64667545],
    [-1.74314104, -0.59664964]])
       W = np.array([[ 0.74505627, 1.97611078, -1.24412333]])
       b = 5
    """
    np.random.seed(1)
    A_prev = np.random.randn(3, 2)
    W = np.random.randn(1, 3)
    b = np.random.randn(1, 1)
    return A_prev, W, b


def compute_cost():
    Y = np.asarray([[1, 1, 0]])
    aL = np.array([[0.8, 0.9, 0.4]])

    return Y, aL


def linear_backward_test():
    """
    z, linear_cache = (np.array([[-0.8019545 ,  3.85763489]]), (np.array([[-1.02387576,  1.12397796],
       [-1.62328545,  0.64667545],
       [-1.74314104, -0.59664964]]), np.array([[ 0.74505627,  1.97611078, -1.24412333]]), np.array([[1]]))
    """
    np.random.seed(5)
    dZ = np.random.randn(3, 4)
    A = np.random.randn(5, 4)
    W = np.random.randn(3, 5)
    b = np.random.randn(3, 1)
    linear_cache = (A, W, b)
    return dZ, linear_cache


def linear_activation_backward_test():
    """
    aL, linear_activation_cache = (np.array([[ 3.1980455 ,  7.85763489]]), ((np.array([[-1.02387576,  1.12397796], [-1.62328545,  0.64667545], [-1.74314104, -0.59664964]]), np.array([[ 0.74505627,  1.97611078, -1.24412333]]), 5), np.array([[ 3.1980455 ,  7.85763489]])))
    """
    np.random.seed(4)
    dA = np.random.randn(1, 2)
    A = np.random.randn(3, 2)
    W = np.random.randn(1, 3)
    b = np.random.randn(1, 1)
    Z = np.random.randn(1, 2)
    linear_cache = (A, W, b)
    activation_cache = Z
    linear_activation_cache = (linear_cache, activation_cache)

    return dA, linear_activation_cache


def backward_all_test():
    """
     X = np.random.rand(3,2)
     Y = np.array([[1, 1]])
     parameters = {'W1': np.array([[ 1.78862847,  0.43650985,  0.09649747]]), 'b1': np.array([[ 0.]])}

     aL, caches = (np.array([[ 0.60298372,  0.87182628]]), [((np.array([[ 0.20445225,  0.87811744],
            [ 0.02738759,  0.67046751],
            [ 0.4173048 ,  0.55868983]]),
     np.array([[ 1.78862847,  0.43650985,  0.09649747]]),
     np.array([[ 0.]])),
    np.array([[ 0.41791293,  1.91720367]]))])
    """
    np.random.seed(3)
    AL = np.random.randn(1, 2)
    Y = np.array([[1, 0]])

    A1 = np.random.randn(4, 2)
    W1 = np.random.randn(3, 4)
    b1 = np.random.randn(3, 1)
    Z1 = np.random.randn(3, 2)
    linear_cache_activation_1 = ((A1, W1, b1), Z1)

    A2 = np.random.randn(3, 2)
    W2 = np.random.randn(1, 3)
    b2 = np.random.randn(1, 1)
    Z2 = np.random.randn(1, 2)
    linear_cache_activation_2 = ((A2, W2, b2), Z2)

    caches = (linear_cache_activation_1, linear_cache_activation_2)

    return AL, Y, caches


def gradient_descent_test_case():
    """
       parameters = {'W1': np.array([[ 1.78862847,  0.43650985,  0.09649747],
           [-1.8634927 , -0.2773882 , -0.35475898],
           [-0.08274148, -0.62700068, -0.04381817],
           [-0.47721803, -1.31386475,  0.88462238]]),
    'W2': np.array([[ 0.88131804,  1.70957306,  0.05003364, -0.40467741],
           [-0.54535995, -1.54647732,  0.98236743, -1.10106763],
           [-1.18504653, -0.2056499 ,  1.48614836,  0.23671627]]),
    'W3': np.array([[-1.02378514, -0.7129932 ,  0.62524497],
           [-0.16051336, -0.76883635, -0.23003072]]),
    'b1': np.array([[ 0.],
           [ 0.],
           [ 0.],
           [ 0.]]),
    'b2': np.array([[ 0.],
           [ 0.],
           [ 0.]]),
    'b3': np.array([[ 0.],
           [ 0.]])}
       grads = {'dW1': np.array([[ 0.63070583,  0.66482653,  0.18308507],
           [ 0.        ,  0.        ,  0.        ],
           [ 0.        ,  0.        ,  0.        ],
           [ 0.        ,  0.        ,  0.        ]]),
    'dW2': np.array([[ 1.62934255,  0.        ,  0.        ,  0.        ],
           [ 0.        ,  0.        ,  0.        ,  0.        ],
           [ 0.        ,  0.        ,  0.        ,  0.        ]]),
    'dW3': np.array([[-1.40260776,  0.        ,  0.        ]]),
    'da1': np.array([[ 0.70760786,  0.65063504],
           [ 0.17268975,  0.15878569],
           [ 0.03817582,  0.03510211]]),
    'da2': np.array([[ 0.39561478,  0.36376198],
           [ 0.7674101 ,  0.70562233],
           [ 0.0224596 ,  0.02065127],
           [-0.18165561, -0.16702967]]),
    'da3': np.array([[ 0.44888991,  0.41274769],
           [ 0.31261975,  0.28744927],
           [-0.27414557, -0.25207283]]),
    'db1': 0.75937676204411464,
    'db2': 0.86163759922811056,
    'db3': -0.84161956022334572}
    """
    np.random.seed(2)
    W1 = np.random.randn(3, 4)
    b1 = np.random.randn(3, 1)
    W2 = np.random.randn(1, 3)
    b2 = np.random.randn(1, 1)
    parameters = {"W1": W1, "b1": b1, "W2": W2, "b2": b2}
    np.random.seed(3)
    dW1 = np.random.randn(3, 4)
    db1 = np.random.randn(3, 1)
    dW2 = np.random.randn(1, 3)
    db2 = np.random.randn(1, 1)
    grads = {"dW1": dW1, "db1": db1, "dW2": dW2, "db2": db2}

    return parameters, grads


def forward_all_test():
    np.random.seed(6)
    X = np.random.randn(5, 4)
    W1 = np.random.randn(4, 5)
    b1 = np.random.randn(4, 1)
    W2 = np.random.randn(3, 4)
    b2 = np.random.randn(3, 1)
    W3 = np.random.randn(1, 3)
    b3 = np.random.randn(1, 1)

    parameters = {"W1": W1, "b1": b1, "W2": W2, "b2": b2, "W3": W3, "b3": b3}

    return X, parameters


def print_grads(grads):
    print("dW1 = " + str(grads["dW1"]))
    print("db1 = " + str(grads["db1"]))
    print("dA1 = " + str(grads["dA1"]))


def sigmoid(Z):
    """
    Implements the sigmoid activation in numpy

    Arguments:
    Z -- numpy array of any shape

    Returns:
    A -- output of sigmoid(z), same shape as Z
    cache -- returns Z as well, useful during backpropagation
    """

    A = 1 / (1 + np.exp(-Z))
    cache = Z

    return A, cache

def knn_2dplot(knn, X, y, 
               ax=None, # Axis
               h=0.2  # Step size in the mesh
               ):

    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt

    # Create graph if needed
    if ax is None:
        fig, ax = plt.subplots(ncols=1, figsize=(4, 4))

    num_clusters = len(np.unique(y))
    colors = ['#581845', '#C70039', '#FF5733', "#0097B2", "#52DE97", "#FBE555", "#053061", "#FAACB5", "black", "#924A5F"]
    labels = [f'Cluster {c}' for c in range(num_clusters)]

    # Create a mesh grid
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = knn.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    ax.contourf(xx, yy, Z, cmap=matplotlib.colors.ListedColormap([colors[c] + "44" for c in range(num_clusters)]))

    # Plot the data points and color them according to their cluster
    for i, color in zip(range(num_clusters), colors):
        idx = np.where(y == i)
        ax.scatter(X[idx, 0], X[idx, 1], c=color, label=labels[i], edgecolor='k', s=50)

    ax.set_xlim(xx.min(), xx.max())
    ax.set_ylim(yy.min(), yy.max())
    ax.set_title(f"{knn.n_neighbors}-Nearest Neighbors Classifier", fontsize=14)
    ax.set_xlabel("Feature 1")
    ax.set_ylabel("Feature 2")
    ax.legend()

    return ax
