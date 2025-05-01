#!/bin/bash

# Check if $1 is provided
if [ -z "$1" ]; then
  echo "Error: No mode specified."
  echo "Usage: $0 {renew|create}"
  exit 1
fi


# Set the mode based on $1
mode=$1

if [ "$mode" == "renew" ]; then

    cd ../django
    pushd .
    cd /tmp
    # Execute the drop database command
    sudo -u postgres psql -c "DROP DATABASE IF EXISTS $VAT_POSTGRES_DB";
    sudo -u postgres psql -c "CREATE DATABASE $VAT_POSTGRES_DB;"

    sudo -u postgres psql -c "DROP OWNED BY $VAT_POSTGRES_USER;"
    sudo -u postgres psql -c "DROP USER IF EXISTS $VAT_POSTGRES_USER"
    sudo -u postgres psql -c "CREATE USER $VAT_POSTGRES_USER WITH PASSWORD '${VAT_POSTGRES_PASS}'"

    # set permissions
    sudo -u postgres psql -c  "GRANT ALL ON DATABASE $VAT_POSTGRES_DB TO $VAT_POSTGRES_USER;"
    sudo -u postgres psql -c  "GRANT ALL PRIVILEGES ON DATABASE $VAT_POSTGRES_DB TO $VAT_POSTGRES_USER;"
    sudo -u postgres psql -c  "ALTER DATABASE $VAT_POSTGRES_DB OWNER TO $VAT_POSTGRES_USER;"
    sudo -u postgres psql -c  "GRANT ALL ON SCHEMA PUBLIC TO $VAT_POSTGRES_USER;"
    sudo -u postgres psql -c  "GRANT SET ON PARAMETER session_replication_role TO $VAT_POSTGRES_USER;"
    # needed for creating test databases
    sudo -u postgres psql -c  "ALTER USER $VAT_POSTGRES_USER CREATEDB;"
    

    popd
    source venv/bin/activate
    python manage.py migrate

    # Check if the command was successful
    if [ $? -eq 0 ]; then
        echo "Database renewed successfully."
    else
        echo "Failed to renew database."
    fi

elif [ "$mode" == "create" ]; then
          # create db and user
    cd /tmp
    sudo -u postgres psql -c "CREATE DATABASE $VAT_POSTGRES_DB;"
    #fails if user is already created
    sudo -u postgres psql -c "CREATE USER $VAT_POSTGRES_USER WITH PASSWORD '${VAT_POSTGRES_PASS}';"
    # set permissions
    sudo -u postgres psql -c  "GRANT ALL ON DATABASE $VAT_POSTGRES_DB TO $VAT_POSTGRES_USER;"
    sudo -u postgres psql -c  "GRANT ALL PRIVILEGES ON DATABASE $VAT_POSTGRES_DB TO $VAT_POSTGRES_USER;"
    sudo -u postgres psql -c  "ALTER DATABASE $VAT_POSTGRES_DB OWNER TO $VAT_POSTGRES_USER;"
    sudo -u postgres psql -c  "GRANT ALL ON SCHEMA PUBLIC TO $VAT_POSTGRES_USER;"
    # needed for creating test databases
    sudo -u postgres psql -c  "ALTER USER $VAT_POSTGRES_USER CREATEDB;"

    # Check if the command was successful
    if [ $? -eq 0 ]; then
        echo "Database created successfully."
    else
        echo "Failed to create database."
    fi
    

else
  echo "Error: Invalid mode specified."
  echo "Usage: $0 {renew|create}"
  exit 1
fi

