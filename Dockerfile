#  airflow version==2.3.0
FROM quay.io/astronomer/astro-runtime:5.0.1

ENV AIRFLOW__SCHEDULER__CATCHUP_BY_DEFAULT=False