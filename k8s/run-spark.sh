#! /bin/sh.
helm upgrade --install my-release my-repo/spark -n airflow
kubectl cp postgresql-42.5.1.jar my-release-spark-master-0:/tmp -n airflow
kubectl cp postgresql-42.5.1.jar my-release-spark-worker-0:/tmp -n airflow
kubectl cp postgresql-42.5.1.jar my-release-spark-worker-1:/tmp -n airflow