
# 🦆 DBT + DuckDB Project

This project demonstrates a simple data pipeline using **DuckDB** as the database and **dbt** for transformations and tests.
You can run everything locally or inside Docker for a reproducible environment.

---

## Prerequisites

* [Docker](https://www.docker.com/) installed and running.
* [Git](https://git-scm.com/) installed if you want to clone/push.

---

## Run the project with Docker

   From the root of the repository (where `docker-compose.yml` is located):

   ```bash
   docker compose up --build
   ```

   This will:

   * Build a Docker image with Python, dbt, DuckDB, and your project files.
   * Run `setup_duckdb.py` to clean csv file and generate `database.duckdb`
   * Run `dbt build` inside the container to run & build models and then export a table.
   

   You should see dbt running and creating models.

   The generated Parquet exports will be available in 

   ```
   ./exports/
   ```

   Warning : currently no log on the export, because it's executed inside DBT on post-hook


## Development (local)

You can also work locally if you prefer:

1. **Create a Python virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Generate the DuckDB database:**

   ```bash
   python ./duckdb/setup_duckdb.py
   ```

   This will create `database.duckdb` inside the `duckdb/` folder.

3. **Run dbt:**

   ```bash"
   cd ../dbt_project
   dbt build
   ```

   dbt will read the DuckDB file and run & test models defined in `models/`.

---

##  Navigating DuckDB

Once your `database.duckdb` is created, you can open a DuckDB shell:

```bash
duckdb duckdb/database.duckdb
```

Inside the shell, you can run SQL directly, for example:

```
SELECT * FROM raw.products LIMIT 10;
SELECT * FROM dwh.daily_metrics order by order_purchase_date desc LIMIT 20;
SELECT * FROM information_schema.tables;
```

Exit with:

```
.quit
```
