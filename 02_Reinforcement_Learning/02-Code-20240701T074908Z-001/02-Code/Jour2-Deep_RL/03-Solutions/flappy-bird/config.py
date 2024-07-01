import flappy_bird_gym
from ray.tune.registry import register_env
import gym
    
def env_creator(env_config):
    import flappy_bird_gym
    env = flappy_bird_gym.make("FlappyBird-v0")
    return env

register_env("flappy_bird", env_creator)

# Configure the algorithm.

config = {
    # Environment (RLlib understands openAI gym registered strings).
    "env": "flappy_bird",
    #"env": "FlappyBird-v0",


    # Use 2 environment workers (aka "rollout workers") that parallelly
    # collect samples from their own environment clone(s).
    "num_workers": 0,
    # Change this to "framework: torch", if you are using PyTorch.
    # Also, use "framework: tf2" for tf2.x eager execution.
    "framework": "tf",
    # Tweak the default model provided automatically by RLlib,
    # given the environment's observation- and action spaces.
    "render_env": False,

    "train_batch_size": 256,

    "preprocessor_pref": "deepmind",

    "model": {
        "fcnet_hiddens": [32, 16],
        "fcnet_activation": "relu",
    },
    "evaluation_interval":1,
    "exploration_config": {
        "type": "EpsilonGreedy",
        "initial_epsilon": 1.0,
        "final_epsilon": 0.1,
        "epsilon_timesteps": 100000, }
}
