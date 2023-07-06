import os


def is_huggingface_installed(verbose=False):
    if "BLK_HUGGINGFACE_TOKEN" in os.environ:
        return True
    if verbose:
        print("\x1b[31m⚠️Please install HUGGING_FACE libraries first\x1b[0m)")
    return False


class PPOHugs:
    def login(self, pass_code=None) -> None:
        import huggingface_hub

        # If you don't want to use a Google Colab or a Jupyter Notebook, you need to use this command instead: huggingface-cli login
        # huggingface_hub.notebook_login()
        # os.system("git config --global credential.helper store")
        huggingface_hub.login(pass_code, add_to_git_credential=True)

    def make(self) -> None:
        import gymnasium as gym

        env = gym.make(self.env_id)
        env.reset()
        return env

    def make_vec_env(self, n_envs=16) -> None:
        import stable_baselines3

        # Create n_envs different environment like a single one
        return stable_baselines3.common.env_util.make_vec_env(self.env_id, n_envs=n_envs)

    def __init__(self, pass_code=None, env_id="LunarLander-v2", model_architecture="PPO", init=None) -> None:
        """
        # MountainCar-v0, Pendulum-v1, CarRacing-v2, Blackjack-v1

        LunarLander-v2: seed="Classroom-workshop/assignment2-omar"
        CartPole-v1: seed="sb3/ppo_lstm-CartPoleNoVel-v1"

        """
        # Create the environment
        self.env_id = env_id
        self.model_name = f"ppo-{self.env_id}"
        self.model_architecture = model_architecture  # Define the model architecture we used
        self.repo_id = f"guydegnol/{self.model_name}"  # Change with your repo id, you can't push with mine 😄

        if is_huggingface_installed(verbose=True):
            self.login(pass_code=os.environ["BLK_HUGGINGFACE_TOKEN"] if pass_code is None else pass_code)
            # self.env = self.make_vec_env()
            if type(init) == str:
                self.pull(init)
            elif init:
                self.create_from_scratch()

    def create_from_scratch(self) -> None:
        import stable_baselines3

        # We added some parameters to accelerate the training
        self.model = stable_baselines3.PPO(
            policy="MlpPolicy",
            env=self.make(),
            n_steps=1024,
            batch_size=64,
            n_epochs=4,
            gamma=0.999,
            gae_lambda=0.98,
            ent_coef=0.01,
            verbose=1,
        )

    def push(self, repo_id=None) -> None:
        import gymnasium as gym
        import huggingface_sb3
        import stable_baselines3

        # from stable_baselines3.common.vec_env import DummyVecEnv

        repo_id = repo_id if type(repo_id) == str else self.repo_id

        # PLACE the package_to_hub function you've just filled here
        eval_env = stable_baselines3.common.vec_env.DummyVecEnv(
            [lambda: gym.make(self.env_id, render_mode="rgb_array")]
        )

        huggingface_sb3.package_to_hub(
            model=self.model,  # Our trained model
            model_name=self.model_name,  # The name of our trained model
            model_architecture=self.model_architecture,  # The model architecture we used: in our case PPO
            env_id=self.env_id,  # Name of the environment
            eval_env=eval_env,  # Create the evaluation env
            repo_id=self.repo_id,  # id of the model repository from the Hugging Face Hub (repo_id = {organization}/{repo_name} for instance ThomasSimonini/ppo-LunarLander-v2
            commit_message=f"Upload {self.model_architecture} {self.env_id} trained agent",
        )

    def pull(self, repo_id=None) -> None:
        import huggingface_sb3
        import stable_baselines3

        repo_id = repo_id if type(repo_id) == str else self.repo_id
        self.model = stable_baselines3.PPO.load(
            huggingface_sb3.load_from_hub(
                repo_id.replace("bulkhours", "guydegnol"), f"{self.model_name}.zip"
            ),  # The model filename.zip,
            # When the model was trained on Python 3.8 the pickle protocol is 5, But Python 3.6, 3.7 use protocol 4
            custom_objects={"learning_rate": 0.0, "lr_schedule": lambda _: 0.0, "clip_range": lambda _: 0.0},
            print_system_info=True,
            # env=self.make(),
        )
        return self.model

    def train(self, pull=True, push=True, timesteps=1_000_000):
        if not is_huggingface_installed(verbose=False):
            return

        if pull:
            self.pull(pull)
        if timesteps:
            self.model.learn(total_timesteps=timesteps)  # Do the training
            self.model.save(self.model_name)  # Save the model
        if push:
            self.push()

    def visualize(self, factor=1.5):
        import IPython

        IPython.display.display(
            IPython.display.HTML(
                f"""<video width="{factor*480}" height="{factor*360}" controls autoplay loop><source src="https://huggingface.co/guydegnol/ppo-LunarLander-v2/resolve/main/replay.mp4" type="video/mp4"></video>"""
            )
        )

    def evaluate(self):
        import gymnasium as gym
        import stable_baselines3

        eval_env = gym.make(self.env_id)
        mean_reward, std_reward = stable_baselines3.common.evaluation.evaluate_policy(
            self.model, eval_env, n_eval_episodes=10, deterministic=True
        )
        print(f"mean_reward={mean_reward:.2f} +/- {std_reward}")

    @staticmethod
    def get_instance(label, pass_code=None):
        return PPOHugs(env_id=label, pass_code=pass_code)
