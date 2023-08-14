import bulkhours


def test_ppohugs():
    captain_robot = bulkhours.ml.PPOHugs(env_id="LunarLander-v2", init="bulkhours/ppo-LunarLander-v2")
