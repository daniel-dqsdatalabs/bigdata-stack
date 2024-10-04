#!/bin/bash
set -e

# Function to run SQL files
run_sql_file() {
    local file="$1"
    if [ -f "$file" ]; then
        echo "Executing $file"
        psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f "$file"
        echo "Finished executing $file"
    fi
}

# Wait for the database to be ready
until psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
    echo "Postgres is unavailable - sleeping"
    sleep 1
done

echo "Postgres is up - executing scripts"

# Execute all .sql files in alphabetical order
for sql_file in /docker-entrypoint-initdb.d/*.sql; do
    run_sql_file "$sql_file"
done

echo "All SQL files have been executed"
