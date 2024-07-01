# Configure the algorithm.
config = {
    # Environment (RLlib understands openAI gym registered strings).
    "env": "ALE/Assault-v5",

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

    "preprocessor_pref": "rllib",

    "model": {
        "fcnet_hiddens": [256, 256],
        "fcnet_activation": "relu",
    },
}
