# Import the RL algorithm (Trainer) we would like to use.
from ray.rllib.algorithms.ppo import PPO
import gym
from config import config
import ray
import os
from ray.tune.logger import pretty_print

# Create our RLlib Trainer.
trainer = PPO(config=config)

# Run it for n training iterations. A training iteration includes
# parallel sample collection by the environment workers as well as
# loss calculation on the collected batch and a model update.
for i in range(1, 200):
    print(f"#### ITERATION {i} ####")
    result = trainer.train()
    print(pretty_print(result))

    if i % 10 == 0:
       checkpoint = trainer.save(f'{os.getcwd()}/checkpoints')
       print("checkpoint saved at", checkpoint)
