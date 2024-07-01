# Import the RL algorithm (Trainer) we would like to use.

from ray.rllib.algorithms.ppo import PPO
import ray
from config import *

from ray.tune.logger import pretty_print

# Create our RLlib Trainer.
trainer = PPO(config=config)


# Run it for n training iterations. A training iteration includes
# parallel sample collection by the environment workers as well as
# loss calculation on the collected batch and a model update.


max_iter=1000
for i in range(1, max_iter+1):
    print(f"#### ITERATION {i} ####")
    result = trainer.train()
    print(pretty_print(result))

    print("episode_reward_max:",result['episode_reward_max'], 'episode_reward_min:', result["episode_reward_min"], 'episode_reward_mean:', result["episode_reward_mean"])
    if i % max_iter == 0:
       checkpoint = trainer.save(f'{os.getcwd()}/flappy-bird/checkpoints')
       print("checkpoint saved at", checkpoint)
