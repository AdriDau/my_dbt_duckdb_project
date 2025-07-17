import duckdb
import csv
from pathlib import Path



def clean_csv(
        file_name: str, 
        src_dir: Path, 
        clean_dir: Path,  
        error_dir: Path, 
):
    """
    Clean a CSV file by validating column counts per row.

    Parameters
    ----------
    file_name : str
        Name of the CSV file to process (e.g. "products.csv").
    src_dir : Path
        Directory containing the source file. Defaults to DATA_SRC_DIR.
    clean_dir : Path
        Directory to save the cleaned file. Defaults to DATA_CLEAN_DIR.
    error_dir : Path
        Directory to save invalid rows (if any). Defaults to DATA_ERROR_DIR.

    Behavior
    --------
    - Reads the CSV from src_dir.
    - Keeps rows matching the header's column count.
    - Writes valid rows to clean_dir.
    - Writes invalid rows to error_dir if any are found.
    """   
   
   # Build the full input path from the source directory
    input_file = src_dir / file_name

    # output path for files cleaned & errors if any
    output_clean = clean_dir / file_name
    output_errors = error_dir / file_name

    # Read all rows
    with open(input_file, "r", newline="", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        rows = list(reader)

    header = rows[0]
    expected_columns = len(header)

    print(f"\n Processing : {file_name}")
    print(f"Header detected ({expected_columns} columns)")

    clean_rows = [header]
    error_rows = [["line_number"] + header]

    # Validate each row
    for i, row in enumerate(rows[1:], start=2):  # Header is line 1
        if len(row) == expected_columns:
            clean_rows.append(row)
        else:
            error_rows.append([i] + row)
            print(f"⚠️ Skipping line {i}: found {len(row)} columns instead of {expected_columns}")

    # Write valid rows to the clean output file
    with open(output_clean, "w", newline="", encoding="utf-8") as out_clean:
        writer = csv.writer(out_clean)
        writer.writerows(clean_rows)
    print(f"✨ Clean file saved: {output_clean} ({len(clean_rows)-1} valid rows)")

    # Write invalid rows if at least one error
    if len(error_rows) > 1:
        with open(output_errors, "w", newline="", encoding="utf-8") as out_err:
            writer = csv.writer(out_err)
            writer.writerows(error_rows)
        print(f"🗑️ Error file saved: {output_errors} ({len(error_rows)-1} invalid rows)")
    else:
        print("✅ No errors found; error file not created.")




def create_views_and_describe_schema(
    view_name: str,
    file_name: str,
    csv_dir: Path,
    con_duckdb: duckdb.DuckDBPyConnection,
    schema: str = "raw"
):
    """
    Create or replace a DuckDB view from a CSV file and print its schema.

    Parameters
    ----------
    view_name : str
        Name of the view to create.
    file_name : str
        Name of the CSV file to process (e.g. "products.csv").
    csv_dir : Path
        Directory containing the CSV file.
    con_duckdb : duckdb.DuckDBPyConnection
        Active DuckDB connection.
    schema : str
        Schema name in which to create the view (default: "raw").
    """

    csv_path = csv_dir / file_name
    # Print schema information inferred from the CSV => Used for the first check to see if Type are okay
    print(f"Schema for CSV file {file_name}:")
    schema_info = con_duckdb.execute(
        f"DESCRIBE SELECT * FROM read_csv('{csv_path}')"
    ).fetchdf()
    print(schema_info[['column_name', 'column_type']])

    # Create or replace the view in the given schema
    sql = f"""
    CREATE SCHEMA IF NOT EXISTS {schema};
    CREATE OR REPLACE VIEW {schema}.{view_name} AS
    SELECT * FROM read_csv('{csv_path}');
    """
    con_duckdb.execute(sql)
    print(f"✅ View '{schema}.{view_name}' created for {csv_path}\n")




if __name__ == "__main__":
    
    #
    ROOT_DIR = Path(__file__).parent.resolve()
    DATA_SRC_DIR = ROOT_DIR / "data" 
    DATA_CLEAN_DIR = ROOT_DIR / "data_clean"
    DATA_ERROR_DIR = ROOT_DIR /"data_parsing_error"
    DB_PATH = ROOT_DIR / "database.duckdb" 
    SCHEMA_RAW = "raw"
    
    # Connection open
    CON = duckdb.connect(DB_PATH)
    
    #  Files list
    SOURCE_FILES = {
        "products":"products.csv",
        "items":"items.csv",
        "orders":"orders.csv",
        "customer":"customer.csv",
    }
    
    # Cleaning CSV files : exclude raws with wrong amount of columns
    print("Cleaning CSV files...")
    for file_name in SOURCE_FILES.values():
        clean_csv(file_name, 
            src_dir= DATA_SRC_DIR, 
            clean_dir = DATA_CLEAN_DIR, 
            error_dir = DATA_ERROR_DIR)


    # 4. Création des vues et affichage du schéma pour chaque fichier nettoyé
    print("\n📦 Creating views and describing schemas...")
    for view_name, file_name in SOURCE_FILES.items():
        create_views_and_describe_schema(view_name=view_name,
                                        csv_dir=DATA_CLEAN_DIR, 
                                        file_name=file_name,
                                        con_duckdb=CON, 
                                        schema=SCHEMA_RAW)
    
    # 5. Close connecrtion
    CON.close() 