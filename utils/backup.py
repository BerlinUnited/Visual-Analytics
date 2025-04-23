import argparse
from pathlib import Path
import subprocess
import os
import fileinput
import psycopg2
from psycopg2 import sql
import time

# kubectl port-forward postgres-postgresql-0 -n postgres 1234:5432
# full backup: python backup.py -a -g -o /opt/local-path-provisioner/db_backup
# full backup: python backup.py -a -t cognition_ballcandidates cognition_ballcandidatestop -o /opt/local-path-provisioner/db_backup

#tar --use-compress-program="pigz -k -3" -cf /opt/local-path-provisioner/db_backup.tar.gz -C /opt/local-path-provisioner/ db_backup/

# only full tables: python backup.py -g -o ./
# usefull backups for local testing: python backup.py -g -a -t image_naoimage -o /opt/local-path-provisioner/db_backup_small
# tar --use-compress-program="pigz -k -3" -cf /opt/local-path-provisioner/db_backup_small.tar.gz -C /opt/local-path-provisioner/ db_backup_small/


DB_HOST = "localhost"
DB_PORT = "1234"
DB_USER = "naoth"
DB_NAME = "vat"

conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=os.environ.get("PGPASSWORD"),
)


def replace_string_in_first_lines(file_path, old_string, new_string, num_lines):
    for i, line in enumerate(fileinput.input(file_path, inplace=True)):
        if i < num_lines:
            line = line.replace(old_string, new_string)
        print(line, end="")


def get_all_log_ids():
    # Create a cursor object
    cur = conn.cursor()
    query = sql.SQL("SELECT DISTINCT id FROM common_log;")
    cur.execute(query)

    # Fetch all results
    results = cur.fetchall()

    # Convert the results to a list of ids
    id_list = [row[0] for row in results]

    # Close the cursor and connection
    cur.close()

    return sorted(id_list)


def create_temp_table(table, table_name, log_id):
    delete_temp_table(table_name)

    cur = conn.cursor()
    query = sql.SQL(
        f"CREATE TABLE {table_name} AS SELECT * FROM {table} WHERE log_id = {log_id}"
    )
    cur.execute(query)
    conn.commit()
    cur.close()


def delete_temp_table(table_name):
    cur = conn.cursor()
    query = sql.SQL(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(query)
    cur.close()


def create_cognition_temp_table(table, table_name, log_id):
    delete_temp_table(table_name)
    command = f"""
    CREATE TABLE {table_name} AS
    SELECT i.*
    FROM common_log l
    JOIN cognition_cognitionframe f ON l.id = f.log_id
    JOIN {table} i ON f.id = i.frame_id
    WHERE l.id = {log_id};
    """
    cur = conn.cursor()
    cur.execute(sql.SQL(command))
    conn.commit()
    cur.close()


def create_motion_temp_table(table, table_name, log_id):
    delete_temp_table(table_name)
    command = f"""
    CREATE TABLE {table_name} AS
    SELECT i.*
    FROM common_log l
    JOIN cognition_motionframe f ON l.id = f.log_id
    JOIN {table} i ON f.id = i.frame_id
    WHERE l.id = {log_id};
    """
    cur = conn.cursor()
    cur.execute(sql.SQL(command))
    conn.commit()
    cur.close()


def export_full_tables():
    tables = [
        "common_event",
        "common_experiment",
        "common_game",
        "common_log",
        "common_logstatus",
        "common_videorecording",
        "behavior_xabslsymbolcomplete",
        "annotation_annotation",
    ]
    for table in tables:
        try:
            command = f"pg_dump -h {DB_HOST} -p {DB_PORT} -U {DB_USER} -d {DB_NAME} -t {table} --data-only"
            print(f"running {command} > {table}.sql")
            output_file = Path(args.output) / f"{table}.sql"
            f = open(str(output_file), "w")
            proc = subprocess.Popen(
                command,
                shell=True,
                env={"PGPASSWORD": os.environ.get("PGPASSWORD")},
                stdout=f,
            )
            proc.wait()
        except Exception as e:
            print("Exception happened during dump %s" % (e))


def export_cognition_tables(log_id, force=False, export_tables=None):
    cognition_tables = [
        "image_naoimage",
        "cognition_ballcandidates",
        "cognition_ballcandidatestop",
        #"cognition_audiodata",
        "cognition_ballmodel",
        "cognition_cameramatrix",
        "cognition_cameramatrixtop",
        "cognition_fieldpercept",
        "cognition_fieldpercepttop",
        "cognition_goalpercept",
        "cognition_goalpercepttop",
        "cognition_multiballpercept",
        "cognition_odometrydata",
        "cognition_ransaccirclepercept2018",
        "cognition_ransaclinepercept",
        "cognition_robotinfo",
        "cognition_scanlineedgelpercept",
        "cognition_scanlineedgelpercepttop",
        "cognition_shortlinepercept",
        "cognition_teammessagedecision",
        "cognition_teamstate",
        "cognition_whistlepercept",
    ]
    if export_tables:
        print(f"Will use tables: {export_tables}")
        cognition_tables = export_tables
        force = True

    for table in cognition_tables:
        output_file = Path(args.output) / f"{table}_{log_id}.sql"
        if output_file.exists() and not force:
            continue

        try:
            temp_table_name = f"temp_{table}"
            create_cognition_temp_table(table, temp_table_name, log_id)
            command = f"pg_dump -h {DB_HOST} -p {DB_PORT} -U {DB_USER} -d {DB_NAME} -t {temp_table_name} --data-only"
            print(f"\trunning {command} > {table}_{log_id}.sql")

            f = open(str(output_file), "w")

            proc = subprocess.Popen(
                command,
                shell=True,
                env={"PGPASSWORD": os.environ.get("PGPASSWORD")},
                stdout=f,
            )
            proc.wait()

            delete_temp_table(temp_table_name)
            # FIXME the last temp folder is not deleted??? - sometimes I see one temp table - check whats going on there.
        except Exception as e:
            print("Exception happened during dump %s" % (e))
            quit()

        # change the table name in the sql files
        replace_string_in_first_lines(output_file, "temp_", "", 200)


def export_motion_tables(log_id, force=False, export_tables=None):
    motion_tables = [
        "motion_accelerometerdata",
        "motion_buttondata",
        "motion_fsrdata",
        "motion_gyrometerdata",
        "motion_imudata",
        "motion_inertialsensordata",
        "motion_motionstatus",
        "motion_motorjointdata",
        "motion_sensorjointdata",
    ]
    if export_tables:
        print(f"Will use tables: {export_tables}")
        motion_tables = export_tables
        force = True

    for table in motion_tables:
        output_file = Path(args.output) / f"{table}_{log_id}.sql"
        if output_file.exists() and not force:
            continue

        try:
            temp_table_name = f"temp_{table}"
            create_motion_temp_table(table, temp_table_name, log_id)
            command = f"pg_dump -h {DB_HOST} -p {DB_PORT} -U {DB_USER} -d {DB_NAME} -t {temp_table_name} --data-only"
            print(f"\trunning {command} > {table}_{log_id}.sql")

            f = open(str(output_file), "w")

            proc = subprocess.Popen(
                command,
                shell=True,
                env={"PGPASSWORD": os.environ.get("PGPASSWORD")},
                stdout=f,
            )
            proc.wait()

            delete_temp_table(temp_table_name)
            # FIXME the last temp folder is not deleted??? - sometimes I see one temp table - check whats going on there.
        except Exception as e:
            print("Exception happened during dump %s" % (e))
            quit()

        # change the table name in the sql files
        replace_string_in_first_lines(output_file, "temp_", "", 200)


def export_split_table(log_id, force=False, export_tables=None):
    tables = [
        "cognition_cognitionframe",
        "motion_motionframe",
    ]

    for table in tables:
        output_file = Path(args.output) / f"{table}_{log_id}.sql"
        if output_file.exists() and not force:
            continue

        try:
            temp_table_name = f"temp_{table}"
            create_temp_table(table, temp_table_name, log_id)
            command = f"pg_dump -h {DB_HOST} -p {DB_PORT} -U {DB_USER} -d {DB_NAME} -t {temp_table_name} --data-only"
            print(f"\trunning {command} > {table}_{log_id}.sql")

            f = open(str(output_file), "w")

            proc = subprocess.Popen(
                command,
                shell=True,
                env={"PGPASSWORD": os.environ.get("PGPASSWORD")},
                stdout=f,
            )
            proc.wait()

            delete_temp_table(temp_table_name)
        except Exception as e:
            print("Exception happened during dump %s" % (e))
            quit()

        # change the table name in the sql files
        replace_string_in_first_lines(output_file, "temp_", "", 200)

    
    
    export_cognition_tables(log_id, force, export_tables)
    export_motion_tables(log_id, force, export_tables)
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--all", action="store_true", default=False)
    parser.add_argument(
        "-l",
        "--logs",
        nargs="+",
        required=False,
        type=int,
        help="Log Id's separated by space",
    )
    parser.add_argument(
        "-o", "--output", required=True, help="Output folder for all sql files"
    )
    parser.add_argument(
        "-g",
        "--global_tables",
        action="store_true",
        required=False,
        default=False,
        help="",
    )
    parser.add_argument(
        "-f", "--force", action="store_true", required=False, default=False, help=""
    )
    parser.add_argument(
        "-t",
        "--tables",
        nargs="+",
        required=False,
        type=str,
        help="table names to export",
    )

    args = parser.parse_args()
    Path(args.output).mkdir(exist_ok=True, parents=True)

    if args.global_tables:
        print("will export tables that are the same for all log ids")
        export_full_tables()

    if args.logs:
        for log_id in args.logs:
            print(f"exporting data for log {log_id}")
            t0 = time.time()
            export_split_table(log_id, args.force, args.tables)
            t1 = time.time()
            print(f"time to export: {t1 - t0}s")

    elif args.all:
        log_ids = get_all_log_ids()

        for log_id in log_ids:
            print(f"exporting data for log {log_id}")
            t0 = time.time()
            export_split_table(log_id, args.force, args.tables)
            t1 = time.time()
            print(f"time to export: {t1 - t0}s")
    
    conn.close()
