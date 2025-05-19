import argparse
from datetime import datetime
from pathlib import Path
import subprocess
import os
import fileinput
import psycopg2
import shutil
from psycopg2 import sql
import time


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


def create_annotation_table(table, table_name, log_id):
    delete_temp_table(table_name)
    command = f"""
    CREATE TABLE {table_name} AS
    SELECT a.*
    FROM common_log l
    JOIN cognition_cognitionframe f ON l.id = f.log_id
    JOIN image_naoimage i ON f.id = i.frame_id
    JOIN {table} a ON i.id = a.image_id
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
    ]
    for table in tables:
        try:
            command = f"pg_dump -h {args.db_host} -p {args.db_port} -U {args.db_user} -d {args.db_name} -t {table} --data-only"
            print(f"running {command} > {table}.sql")
            output_file = Path(output_folder) / f"{table}.sql"
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
        cognition_tables = [item for item in cognition_tables if item in export_tables]
        force = True

    for table in cognition_tables:
        output_file = Path(output_folder) / f"{table}_{log_id}.sql"
        if output_file.exists() and not force:
            continue

        try:
            temp_table_name = f"temp_{table}"
            create_cognition_temp_table(table, temp_table_name, log_id)
            command = f"pg_dump -h {args.db_host} -p {args.db_port} -U {args.db_user} -d {args.db_name} -t {temp_table_name} --data-only"
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
        motion_tables = [item for item in motion_tables if item in export_tables]
        force = True

    for table in motion_tables:
        output_file = Path(output_folder) / f"{table}_{log_id}.sql"
        if output_file.exists() and not force:
            continue

        try:
            temp_table_name = f"temp_{table}"
            create_motion_temp_table(table, temp_table_name, log_id)
            command = f"pg_dump -h {args.db_host} -p {args.db_port} -U {args.db_user} -d {args.db_name} -t {temp_table_name} --data-only"
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


def export_annotation_tables(log_id, force=False, export_tables=None):
    tables = [
        "annotation_annotation",
    ]
    if export_tables:
        tables = [item for item in tables if item in export_tables]
        force = True
    
    for table in tables:
        output_file = Path(output_folder) / f"{table}_{log_id}.sql"
        if output_file.exists() and not force:
            continue

        try:
            temp_table_name = f"temp_{table}"
            create_annotation_table(table, temp_table_name, log_id)
            command = f"pg_dump -h {args.db_host} -p {args.db_port} -U {args.db_user} -d {args.db_name} -t {temp_table_name} --data-only"
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
        output_file = Path(output_folder) / f"{table}_{log_id}.sql"
        if output_file.exists() and not force:
            continue

        try:
            temp_table_name = f"temp_{table}"
            create_temp_table(table, temp_table_name, log_id)
            command = f"pg_dump -h {args.db_host} -p {args.db_port} -U {args.db_user} -d {args.db_name} -t {temp_table_name} --data-only"
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
    export_annotation_tables(log_id, force, export_tables)


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
    # default arguments are correct if you use forwarding as described in the docs
    parser.add_argument("--db_host", required=False, default="localhost", help="")
    parser.add_argument("--db_port", required=False, default="1234", help="")
    parser.add_argument("--db_user", required=False, default="naoth", help="")
    parser.add_argument("--db_name", required=False, default="vat", help="")
    args = parser.parse_args()

    # setup postgres connection
    conn = psycopg2.connect(
        host=args.db_host,
        port=args.db_port,
        dbname=args.db_name,
        user=args.db_user,
        password=os.environ.get("PGPASSWORD"),
    )
    today = datetime.now()
    datestring = today.strftime("%Y%m%d%H")
    output_folder = Path(args.output) / Path(datestring)
    Path(output_folder).mkdir(exist_ok=True, parents=True)

    if args.global_tables:
        print("will export tables that are the same for all log ids")
        export_full_tables()

    if args.logs:
        for log_id in args.logs:
            print(f"exporting data for log {log_id}")
            t0 = time.time()
            export_split_table(log_id, args.force, args.tables)
            t1 = time.time()

    elif args.all:
        log_ids = get_all_log_ids()

        for log_id in log_ids:
            print(f"exporting data for log {log_id}")
            t0 = time.time()
            export_split_table(log_id, args.force, args.tables)
            t1 = time.time()
    
    conn.close()

    # zip
    print("zip all sql files")
    command = f"tar --use-compress-program='pigz -k -3' -cf {args.output}/{datestring}.tar.gz -C {args.output} {datestring}/"
    proc = subprocess.Popen(command,shell=True)
    proc.wait()

    print("cleanup sql files")
    shutil.rmtree(str(output_folder))