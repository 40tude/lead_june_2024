- Install postgreSQL Chart and set environment variables

  - `helm repo add bitnami https://charts.bitnami.com/bitnami`
  - `helm install psql-release bitnami/postgresql -f postgres-config.yaml`
    - `postgres-config.yaml` is in `with_postgres_chart` folder
  - Carefully read these instructions:

  ```shell
  NAME: psql-release
  LAST DEPLOYED: Sat May 28 23:00:19 2022
  NAMESPACE: default
  STATUS: deployed
  REVISION: 1
  TEST SUITE: None
  NOTES:
  CHART NAME: postgresql
  CHART VERSION: 11.5.0
  APP VERSION: 14.3.0

  ** Please be patient while the chart is being deployed **

  PostgreSQL can be accessed via port 5432 on the following DNS names from within your cluster:

      psql-release-postgresql.default.svc.cluster.local - Read/Write connection

  To get the password for "postgres" run:

      export POSTGRES_ADMIN_PASSWORD=$(kubectl get secret --namespace default psql-release-postgresql -o jsonpath="{.data.postgres-password}" | base64 --decode)

  To get the password for "antoine" run:

      export POSTGRES_PASSWORD=$(kubectl get secret --namespace default psql-release-postgresql -o jsonpath="{.data.password}" | base64 --decode)

  To connect to your database run the following command:

      kubectl run psql-release-postgresql-client --rm --tty -i --restart='Never' --namespace default --image docker.io/bitnami/postgresql:14.3.0-debian-10-r13 --env="PGPASSWORD=$POSTGRES_PASSWORD" \
      --command -- psql --host psql-release-postgresql -U antoine -d antoine-db -p 5432

      > NOTE: If you access the container using bash, make sure that you execute "/opt/bitnami/scripts/postgresql/entrypoint.sh /bin/bash" in order to avoid the error "psql: local user with ID 1001} does not exist"

  To connect to your database from outside the cluster execute the following commands:

      kubectl port-forward --namespace default svc/psql-release-postgresql 5432:5432 &
      PGPASSWORD="$POSTGRES_PASSWORD" psql --host 127.0.0.1 -U antoine -d antoine-db -p 5432
  ```

Here:

- DB_USERNAME="antoine"
- DB_PASSWORD="passw0rd"
- DB_HOST="psql-release-postgresql"
- DB_PORT=5432
- DB_NAME=antoine-db

Therefore:

- BACKEND_STORE_URI=postgresql://antoine:passw0rd@psql-release-postgresql:5432/antoine-db

**DOCUMENTATIONS**:

- Official Helm chart: https://artifacthub.io/packages/helm/bitnami/postgresql
- Repo with all configs: https://github.com/bitnami/charts/tree/master/bitnami/postgresql-ha
- Difficult but complete: https://docs.bitnami.com/kubernetes/infrastructure/postgresql-ha/

---

Few `psql` interesting commands:

- SHOW TABLES: `\dt`
- SHOW DB: `\db`
- SHOW USERS: `\du`
