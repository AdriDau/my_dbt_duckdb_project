FROM python:3.11-slim

# Working directory
WORKDIR /app

# Install packages
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt


# Copy project
COPY duckdb/ duckdb/
COPY dbt_project/ dbt_project/

#export directory
RUN mkdir /app/exports

ENV DBT_PROFILES_DIR=/app/dbt_project
ENV EXPORT_PATH=/app/exports
ENV ENVIRONMENT=docker

CMD python duckdb/setup_duckdb.py && dbt build --project-dir /app/dbt_project
