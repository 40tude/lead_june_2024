docker run --name postgres_container -e POSTGRES_USER=philippe -e POSTGRES_PASSWORD=secretpassword   -d -p 5432:5432 -v ${PWD}/db-data:/var/lib/postgresql/data postgres

minikube start 

kubectl apply -f secrets.yaml
kubectl apply -f mlflow--deployment.yaml
kubectl apply -f mlflow--services.yaml

minikube service mlflow--services

minikube service list
kubectl get deployments
kubectl delete deployment mlflow--deployment


kubectl get pods
kubectl delete pod NOM_DU_POD

