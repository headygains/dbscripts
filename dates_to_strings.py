import pyodbc,csv,os,shlex

db = r"x:\dataTest\android_team.accdb"
conn_string = r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" +db
path_auditor_repo = r'x:\dataTest\qcm\repo\auditor_crates.csv'
path_auditor_new_repo = r'x:\dataTest\qcm\repo\update_auditor_crates.csv'
auditor_list = ["gcn647", "tbh643", "gkwr86"]
_SELECT = "SELECT "
_FROM = "FROM "
_WHERE = "WHERE "
_INSERT = "INSERT "
_INTO = "INTO "
_ALL = "ID,repair_tech,crate_number,passed_units,failed_units,auditor,min_count,check_date "
_CRATES = "Crates "
_COLUMN_CHECK_DATE = "check_date"
_COLUMN_AUDITOR = "auditor"
_RP = "("
_LP = ")"
_SQL = "SELECT * From Crates"


def main():
    clear()
    while True:
        cmd, arg1 = shlex.split(input('#!'))

        if cmd == "update":
            clear()
            update()
        else:
            help()


def connect():
    # Create the database connection and the cursor to work with the connection
    conn = pyodbc.connect(conn_string)
    cursor = conn.cursor()
    return conn, cursor


def disconnect(conn):
    conn.close()
    return True


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_crates(cursor):
    # Preform the query to select all from crates where auditor = ?
    # Write the results of that query into a csv file
    # Each row being a new line, The file will end up ordered by auditor.
    count = 0
    # Get all crates by auditor and write them to a csv file
    with open(path_auditor_repo, "a") as file:
        writer = csv.writer(file, delimiter=";")
        for row in cursor.execute(_SQL):
            writer.writerow([row[1], row[2], row[3],
                             row[4], row[5], row[6], row[7]])
            count += 1
            clear()
            print "Database Entries Processed: " + str(count)
    file.close()
    print "Operation Completed, " + str(count) + " Entries Processed."


def change_crate_dates_to_str():
    # Originally I did not want to make the dates into strings because parsing the later
    # would be less efficient, unfortunately I haven't been able to work with the date
    # format in access, this is fine as I'm not to concerned about the extra resource usage
    # at this point.

    with open(path_auditor_repo, "r") as file:
        with open(path_auditor_new_repo, "a") as nFile:
            writer = csv.writer(nFile, delimiter=";")
            reader = csv.reader(file, delimiter=";")

            # I want to seperate the date from the time, time is useless here.
            for line in reader:
                date = line[6]
                day, time = shlex.split(date)
                line[6] = day
                writer.writerow(line)
                print "OD: " + date + " ND: " + day
        nFile.close()
    file.close()


def update():

    conn, cursor = connect()
    get_crates(cursor)
    change_crate_dates_to_str()

def help():