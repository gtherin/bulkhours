import matplotlib as mpl
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import collections
import random
import sys


def record_scenario(env, policy, num_frames=100) -> dict:
    frames = []
    obs_mat = np.empty((num_frames, 4))
    actions = np.empty((num_frames,))
    rewards = np.empty((num_frames,))
    dones = np.empty((num_frames,), dtype=int)
    first_done_info = ""
    obs, info = env.reset()
    for i in range(num_frames):
        action = policy(obs)
        obs, reward, done, truncated, info = env.step(action)
        img = env.render()
        frames.append(img)
        obs_mat[i, :] = obs
        actions[i] = action
        rewards[i] = reward
        dones[i] = int(done)
        if done and first_done_info == "":
            first_done_info = info
    record = {
        "frames": frames,
        "obs": obs_mat,
        "actions": actions,
        "rewards": rewards,
        "dones": dones,
        "first_done_info": first_done_info,
    }
    return record


def update_scene(num, frames, patch, time_text, obs_mat, actions, cum_rewards, dones):
    patch.set_data(frames[num])
    text = f"frame: {num}"
    text += ", Obs: ({:.3f}, {:.3f}, {:.3f}, {:.3f})\n".format(*obs_mat[num, :])
    text += f"Action: {actions[num]}"
    text += f", Cumulative Reward: {cum_rewards[num]}"
    text += f", Done: {dones[num]}"
    time_text.set_text(text)
    return patch, time_text


def plot_animation(record, repeat=False, interval=40):
    """record should contain
    frames: list of N frames
    obs: (N, 4) array of observations
    actions: (N, ) array of actions {0, 1}
    rewards: (N, ) array of rewards at each step {0, 1}
    dones: (N, 1) array of dones {0, 1}
    """
    cum_rewards = np.cumsum(record["rewards"])
    frames = record["frames"]
    fig = plt.figure()
    patch = plt.imshow(record["frames"][0])
    ax = plt.gca()
    time_text = ax.text(0.0, 0.95, "", horizontalalignment="left", verticalalignment="top", transform=ax.transAxes)
    plt.axis("off")
    anim = animation.FuncAnimation(
        fig,
        update_scene,
        fargs=(frames, patch, time_text, record["obs"], record["actions"], cum_rewards, record["dones"]),
        frames=len(frames),
        repeat=repeat,
        interval=interval,
    )
    plt.close()
    return anim


# position, velocity, angle, angular velocity
CPObs = collections.namedtuple("CartPole_obs", "x v theta omega")


N_scenario = 1000
MAX_ACTIONS = 500


def test_policy(env, policy_func, n_scenario=500, max_actions=200, verbose=False):
    final_rewards = []
    final_grads = []
    for episode in range(n_scenario):
        if verbose and episode % 50 == 0:
            print(episode)
        episode_rewards = 0
        obs, info = env.reset(seed=episode)
        for _ in range(max_actions):
            action = policy_func(obs)
            # obs, reward, done, truncated, grads = play_one_step(env, obs, model, loss_fn)
            obs, reward, done, truncated, info = env.step(action)

            episode_rewards += reward
            if done:
                break
        final_rewards.append(episode_rewards)
        # final_grads.append(episode_rewards)
    return final_rewards


def plot_policy(final_rewards, policy_name: str = ""):
    fig = plt.plot(range(len(final_rewards)), final_rewards)
    plt.grid()
    # np.mean(totals), np.std(totals), min(totals), max(totals)
    plt.title(
        policy_name + " Mean Reward {:.2f}, Std Reward {:.2f}".format(np.mean(final_rewards), np.min(final_rewards))
    )
    plt.ylabel("Cum Reward")
    plt.xlabel("Iteration")
    plt.ylim(0, max(final_rewards) * 1.1)
    return fig


def make(*kargs, seed=None, **kwargs):
    import gymnasium as gym

    env = gym.make(*kargs, **kwargs)
    if seed:
        env.reset(seed=seed)
    return env


def plot(env, policy, seed=42, policy_name: str = "", gif_filename=""):
    import IPython
    import os
    import array2gif

    env.reset(seed=seed)
    random.seed(seed)
    rewards = test_policy(env, policy)
    plot_policy(rewards, policy_name)
    records = record_scenario(env, policy, 100)

    if gif_filename != "":
        if not os.path.exists(gif_filename):
            array2gif.write_gif([np.transpose(f, axes=[2, 0, 1]) for f in records["frames"]], gif_filename, fps=30)
        IPython.display.Image(open(gif_filename, "rb").read())

    return plot_animation(records)


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

    runrealcmd("apt-get install -y xvfb python-opengl", verbose=True)
    runrealcmd("pip install gymnasium pyvirtualdisplay array2gif", verbose=True)
    runrealcmd("pip install gymnasium[atari,toy_text,box2d,classic_control,accept-rom-license]", verbose=True)

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
