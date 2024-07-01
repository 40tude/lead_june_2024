* Question : Compromis biais-variance
* Réponse  : Le biais mesure à quel point les prédictions d'un modèle diffèrent des valeurs réelles. Un modèle avec un biais élevé simplifie trop les données d'entraînement et sous-estime la complexité de la relation entre les features et la target. Conduit à des performances médiocres sur les données d'entraînement et de test. Les modèles à haut biais sont généralement trop simples pour capturer la complexité des données. Pour réduire le biais, on peut utiliser des modèles plus complexes ou augmenter la taille ou la complexité des caractéristiques utilisées. Features engineering.
La variance mesure la sensibilité d'un modèle aux petites variations dans l'ensemble de données d'entraînement. Un modèle avec une variance élevée est trop sensible au bruit dans les données d'entraînement, ce qui peut conduire à un surajustement. Le modèle fonctionne bien sur les données d'entraînement mais il a du mal à généraliser sur de nouvelles données. Les modèles à haute variance sont souvent complexes (arbres de décision profonds, réseaux neuronaux avec de nombreux paramètres). Pour réduire la variance, on peut utiliser la régularisation, la réduction de la dimensionnalité ou l'augmentation des données.
La validation croisée peut être utile pour évaluer comment le compromis biais-variance affecte les performances du modèle. En utilisant la validation croisée, on peut ajuster les hyperparamètres du modèle pour trouver le meilleur compromis entre biais et variance.



* Question : Batch Gradient Descent, Stochastic Gradient Descent, Mini-Batch Gradient Descent ? - ** 
* Réponse  : Blablabla...

1. Batch Gradient Descent (Batch Size = Number of Observations). Full Batch Gradient Descent. In this scenario, the entire dataset is used to compute the gradient of the cost function. The parameters are updated once per epoch (one pass through the entire dataset). This method is computationally expensive because it requires storing the entire dataset in memory and computing the gradients for all samples before updating the parameters. However, it usually leads to very stable updates and can converge to a good solution.

2. Stochastic Gradient Descent (Batch Size = 1). Here, the gradient is computed and parameters are updated after each individual sample. It's very noisy but can help the model escape local minima more easily and often converges faster, especially with large datasets.

3. Mini-Batch Gradient Descent (1 < Batch Size < Number of Observations). A compromise between batch gradient descent and stochastic gradient descent. It computes the gradient and updates the parameters using a subset of the dataset (a mini-batch) at each iteration. This strikes a balance between the stability of batch gradient descent and the faster convergence of stochastic gradient descent. The batch size is typically chosen to be a power of 2 for efficient memory usage.
