import os


class LunarLander:
    def login(self, pass_code=None) -> None:
        import huggingface_hub

        # huggingface_hub.notebook_login()
        # os.system("git config --global credential.helper store")
        huggingface_hub.login(pass_code, add_to_git_credential=True)

    def make(self) -> None:
        import gym

        return gym.make(self.env_id)

    def make_vec_env(self, n_envs=16) -> None:
        from stable_baselines3.common.env_util import make_vec_env

        return make_vec_env(self.env_id, n_envs=n_envs)

    def __init__(self, pass_code=None) -> None:
        # Create the environment
        self.env_id = "LunarLander-v2"
        self.model_name = "ppo-LunarLander-v2"
        self.model_architecture = "PPO"  # Define the model architecture we used
        self.repo_id = f"guydegnol/{self.model_name}"  # Change with your repo id, you can't push with mine 😄

        self.login(pass_code=pass_code)
        self.env = self.make_vec_env()

    def create_from_scratch(self) -> None:
        from stable_baselines3 import PPO

        # We added some parameters to accelerate the training
        self.model = PPO(
            policy="MlpPolicy",
            env=self.env,
            n_steps=1024,
            batch_size=64,
            n_epochs=4,
            gamma=0.999,
            gae_lambda=0.98,
            ent_coef=0.01,
            verbose=1,
        )

    def push(self) -> None:
        from huggingface_sb3 import package_to_hub
        from stable_baselines3.common.vec_env import DummyVecEnv

        # PLACE the package_to_hub function you've just filled here
        package_to_hub(
            model=self.model,  # Our trained model
            model_name=self.model_name,  # The name of our trained model
            model_architecture=self.model_architecture,  # The model architecture we used: in our case PPO
            env_id=self.env_id,  # Name of the environment
            eval_env=DummyVecEnv([lambda: self.make()]),  # Create the evaluation env
            repo_id=self.repo_id,  # id of the model repository from the Hugging Face Hub (repo_id = {organization}/{repo_name} for instance ThomasSimonini/ppo-LunarLander-v2
            commit_message=f"Upload {self.model_architecture} {self.env_id} trained agent",
        )

    def pull(self, repo_id="guydegnol/ppo-LunarLander-v2") -> None:
        from huggingface_sb3 import load_from_hub
        from stable_baselines3 import PPO

        # repo_id = "Classroom-workshop/assignment2-omar" # The repo_id
        self.model = PPO.load(
            load_from_hub(repo_id, f"{self.model_name}.zip"),  # The model filename.zip,
            # When the model was trained on Python 3.8 the pickle protocol is 5, But Python 3.6, 3.7 use protocol 4
            custom_objects={"learning_rate": 0.0, "lr_schedule": lambda _: 0.0, "clip_range": lambda _: 0.0},
            print_system_info=True,
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
