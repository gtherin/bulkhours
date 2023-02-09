import os


class PPOHugs:
    def login(self, pass_code=None) -> None:
        import huggingface_hub

        # If you don't want to use a Google Colab or a Jupyter Notebook, you need to use this command instead: huggingface-cli login
        # huggingface_hub.notebook_login()
        # os.system("git config --global credential.helper store")
        huggingface_hub.login(pass_code, add_to_git_credential=True)

    def make(self) -> None:
        import gym

        env = gym.make(self.env_id)
        env.reset()
        return env

    def make_vec_env(self, n_envs=16) -> None:
        from stable_baselines3.common.env_util import make_vec_env

        # Create n_envs different environment like a single one
        return make_vec_env(self.env_id, n_envs=n_envs)

    def __init__(self, pass_code=None, env_id="LunarLander-v2", model_architecture="PPO", init=None) -> None:
        # Create the environment
        self.env_id = env_id
        self.model_name = f"ppo-{self.env_id}"
        self.model_architecture = model_architecture  # Define the model architecture we used
        self.repo_id = f"guydegnol/{self.model_name}"  # Change with your repo id, you can't push with mine 😄

        self.login(pass_code=pass_code)
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
            env=self.make,
            n_steps=1024,
            batch_size=64,
            n_epochs=4,
            gamma=0.999,
            gae_lambda=0.98,
            ent_coef=0.01,
            verbose=1,
        )

    def push(self, repo_id=None) -> None:
        import huggingface_sb3

        from stable_baselines3.common.vec_env import DummyVecEnv

        repo_id = repo_id if repo_id else self.repo_id

        # PLACE the package_to_hub function you've just filled here
        huggingface_sb3.package_to_hub(
            model=self.model,  # Our trained model
            model_name=self.model_name,  # The name of our trained model
            model_architecture=self.model_architecture,  # The model architecture we used: in our case PPO
            env_id=self.env_id,  # Name of the environment
            eval_env=DummyVecEnv([lambda: self.make()]),  # Create the evaluation env
            repo_id=self.repo_id,  # id of the model repository from the Hugging Face Hub (repo_id = {organization}/{repo_name} for instance ThomasSimonini/ppo-LunarLander-v2
            commit_message=f"Upload {self.model_architecture} {self.env_id} trained agent",
        )

    def pull(self, repo_id=None) -> None:
        # repo_id = "Classroom-workshop/assignment2-omar" # The repo_id
        import huggingface_sb3
        import stable_baselines3

        repo_id = repo_id if repo_id else self.repo_id
        self.model = stable_baselines3.PPO.load(
            huggingface_sb3.load_from_hub(repo_id, f"{self.model_name}.zip"),  # The model filename.zip,
            # When the model was trained on Python 3.8 the pickle protocol is 5, But Python 3.6, 3.7 use protocol 4
            custom_objects={"learning_rate": 0.0, "lr_schedule": lambda _: 0.0, "clip_range": lambda _: 0.0},
            print_system_info=True,
            env=self.make(),
        )
        return self.model

    def train(self, pull=True, push=True, timesteps=1_000_000):
        if pull:
            self.pull()
        self.model.learn(total_timesteps=timesteps)  # Do the training
        self.model.save(self.model_name)  # Save the model
        if push:
            self.push()

    def evaluate(self):
        from stable_baselines3.common.evaluation import evaluate_policy

        eval_env = self.make()
        mean_reward, std_reward = evaluate_policy(self.model, eval_env, n_eval_episodes=10, deterministic=True)
        print(f"mean_reward={mean_reward:.2f} +/- {std_reward}")

    @staticmethod
    def get_instance(label, pass_code=None):
        return PPOHugs(env_id=label, pass_code=pass_code)
