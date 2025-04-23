import argparse
from pathlib import Path
import subprocess
import os
import re


# Custom key function for natural sorting
def natural_sort_key(s):
    # Use a regular expression to split the string into parts
    return [
        int(text) if text.isdigit() else text.lower()
        for text in re.split("([0-9]+)", str(s))
    ]


def import_global_tables():
    sql_table = [
        "common_event.sql",
        "common_experiment.sql",
        "common_game.sql",
        "common_log.sql",
        "common_logstatus.sql",
        "common_videorecording.sql",
        "behavior_xabslsymbolcomplete.sql",
        "annotation_annotation.sql",
    ]

    for file in sql_table:
        try:
            command = f"psql -h {os.getenv('VAT_POSTGRES_HOST')} -p {os.getenv('VAT_POSTGRES_PORT')} -U {os.getenv('VAT_POSTGRES_USER')} -d {os.getenv('VAT_POSTGRES_DB')} -f '{args.input}/{file}'"
            print(f"running {command}")
            output_file = "error.txt"
            f = open(str(output_file), "w")
            proc = subprocess.Popen(
                command,
                shell=True,
                env={"PGPASSWORD": os.environ.get("VAT_POSTGRES_PASS")},
                stdout=f,
            )
            return_code = proc.wait()
            if return_code != 0:
                print(
                    f"Command failed with return code {return_code}. Aborting script."
                )
                quit()
        except Exception as e:
            print("Exception happened during dump %s" % (e))
            quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="path to the folder containing all the sql files",
    )
    parser.add_argument(
        "-t",
        "--table",
        nargs="+",
        required=False,
        type=str,
        help="tables that should be restored",
    )
    parser.add_argument(
        "--ids", nargs="+", required=False, type=int, help="ids that should be restored"
    )

    args = parser.parse_args()

    import_global_tables()

    sql_table = [
        "cognition_cognitionframe",
        "motion_motionframe",
        "image_naoimage",
        "cognition_ballcandidates",
        "cognition_ballcandidatestop",
        # "cognition_audiodata",
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
    for table in sql_table:
        if args.table:
            if table not in args.table:
                continue
        print(f"importing {table} tables")
        for file_path in sorted(
            Path(args.input).glob(f"{table}_*.sql"), key=natural_sort_key
        ):
            # if we have a list of ids, get the number of the file
            match = re.search(r"_(\d+)\.sql$", str(file_path))
            if match:
                # Extract the number from the match object
                number = int(match.group(1))
            else:
                print("ERROR: could not parse number of ")
                quit()
            if args.ids:
                # Check if the number is in the list of numbers
                if number not in args.ids:
                    continue

            print(f"importing table for log id {number}")
            try:
                command = f"psql -h {os.getenv('VAT_POSTGRES_HOST')} -p {os.getenv('VAT_POSTGRES_PORT')} -U {os.getenv('VAT_POSTGRES_USER')} -d {os.getenv('VAT_POSTGRES_DB')} -f '{file_path}'"
                print(f"running {command}")
                proc = subprocess.Popen(
                    command,
                    shell=True,
                    env={"PGPASSWORD": os.environ.get("VAT_POSTGRES_PASS")},
                    stdout=subprocess.DEVNULL,
                )
                return_code = proc.wait()
                if return_code != 0:
                    print(
                        f"Command failed with return code {return_code}. Aborting script."
                    )
                    quit()
            except Exception as e:
                print("Exception happened during dump %s" % (e))
                quit()
