import sqlite3
import yaml

def load_schema(file_path):
    # Load schema from YAML file
    with open(file_path, 'r') as file:
        schema = yaml.safe_load(file)
    return schema

def init_db(schema):
    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect("housing_sanitation.db")
    cursor = conn.cursor()

    # Define table creation based on schema
    columns = []
    for field, properties in schema.items():
        # Map the YAML data types to SQLite data types
        if properties['type'] == 'numeric':
            field_type = "REAL"  # SQLite uses REAL for floating-point numbers
        elif properties['type'] == 'integer':
            field_type = "INTEGER"
        elif properties['type'] == 'string':
            field_type = "TEXT"
        else:
            raise ValueError(f"Unsupported type for field {field}")

        # Check if NULL values are allowed
        allow_null = "" if properties.get('allow_null', True) else "NOT NULL"
        
        # Add to columns list
        columns.append(f"{field} {field_type} {allow_null}")

    # Generate the CREATE TABLE statement
    create_table_query = f"CREATE TABLE IF NOT EXISTS housing_sanitation ({', '.join(columns)});"
    cursor.execute(create_table_query)

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Database initialized with table 'housing_sanitation'.")

# Load schema and initialize the database
schema = load_schema("data_schema.yaml")
init_db(schema)
