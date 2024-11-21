import numpy as np
from ray import tune
from sklearn.datasets import load_digits
from sklearn.ensemble import RandomForestClassifier
from ray.tune.search.hyperopt import HyperOptSearch

digits = load_digits()

def objective(config):  # ①
    model = RandomForestClassifier(max_depth=config["max_depth"],
    min_samples_split=config["min_samples_split"],
    criterion="gini",
    )
    model.fit(digits.data, digits.target)
    accuracy = model.score(digits.data, digits.target)
    return {"accuracy": accuracy}

search_space = {'max_depth': tune.randint(2,20),
    'min_samples_split': tune.randint(2, 10)
    }  # ②
algo = HyperOptSearch()

tuner = tune.Tuner(  # ③
    objective,
    tune_config=tune.TuneConfig(
        metric="accuracy", # The search will attempt to optimize the accuracy metric
        mode="max", # The optimization process will attempt to maximize the accuracy
        search_alg=algo,
        num_samples=10 # the number of attempts in the grid search process
    ),
    param_space=search_space,
)
results = tuner.fit()