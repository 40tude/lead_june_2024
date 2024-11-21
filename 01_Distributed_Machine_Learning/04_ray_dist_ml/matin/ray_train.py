# name this file ray_train.py
import joblib
from ray.util.joblib import register_ray
from sklearn.datasets import load_digits
from sklearn.svm import SVC

digits = load_digits()

model = SVC(kernel="rbf")

# Necessary otherwise your model will be trained only on one node
## FYI, you won't see any difference if you run `register_ray()` & `with joblib.parallel_backend('ray')
## on minikube, since it runs only one node. But if you run it in production, you will see that your task
## will be distributed on several machines.
register_ray()
with joblib.parallel_backend("ray"):
    model.fit(digits.data, digits.target)
    print(model.score(digits.data, digits.target))
