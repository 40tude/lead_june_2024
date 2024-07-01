import gym
env = gym.make("ALE/Assault-v5", render_mode="human")
#env = gym.make("Taxi-v3")
print(env.action_space)
env.action_space.seed(42)

observation = env.reset()

for _ in range(100000):
    observation, reward, done, info,_ = env.step(env.action_space.sample())
    env.render()

    if done:
        observation = env.reset()

env.close()
