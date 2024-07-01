## Database setup (backend store)

Let's start by running a container that will serve the postgres database used by the mlflow tracking server:

```shell
docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 -v ${PWD}/db-data:/var/lib/postgresql/data postgres
```

the uri of this database is of the form:

postgres[ql]://[username[:password]@][host[:port],]/database[?parameter_list]

Considering the arguments we used at creation, the URI is:

postgresql://postgres:mysecretpassword@host.docker.internal:5432/postgres

All the information relative to this database setup can be found on [DockerHub](https://hub.docker.com/_/postgres)

## S3 setup (artifact store)

In aws, choose a S3 bucket to use as artifact store or create one. The URI you'll use is of the form `s3://name-of-my-bucket/path/to/my/folder`.

## Setup the mlflow tracking server on k8

Start the minikube cluster :

`minikube start`

Start the pods using :
`kubectl apply -f mlflow-deployment.yaml`
`kubectl apply -f mlflow-service.yaml`

Then use the following command to access the mlflow tracking server :
`minikube service mlflow-service`

## Test the tracking server

Use the mlflow server URI to define the `"APP_URI"` environment variable in the test-mlflow.ipynb notebook, then run the cells. You should see a new experiment appear as well as information relative to your model.