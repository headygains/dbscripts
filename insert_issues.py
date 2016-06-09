import pyodbc

db = r"x:\dataTest\android_team.accdb"
conn_string = r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" +db

sql_get_issues = 'SELECT ID, issues FROM Issues ORDER By ID;'
sql_drop_issues = 'DROP TABLE Issues'
sql_create_issues = 'CREATE TABLE Issues (ID int, ISSUE varchar(255))'
sql_insert_issue = 'INSERT INTO Issues VALUES('

path_issues_repo = r'x:\dataTest\qcm\repo\issues_list.txt'


def main():
    # Create Database Connection and Return Cursor
    connection, cursor = connect()
    issues = get_issues(cursor)
    update_issues(issues, cursor)
    cursor.close()
    connection.close()


# Create connection to our database and return the connection object
# along with a cursor object.
def connect():
    conn = pyodbc.connect(conn_string)
    cursor = conn.cursor();
    return conn, cursor


def get_issues(cursor):
    issues = dict()
    for row in cursor.execute(sql_get_issues):
        issues[row.ID] = row.issues
    return issues


# Returns an issues dictionary based upon the contents of the
# repo/issues.txt file. Using this file to manage the contents
# of the database works great for easy editing and updating of
# the actual database table Issues
def get_new_issues():
    count = 0
    issues = dict()
    f = open(path_issues_repo, 'r')
    for line in f:
        count += 1
        issues[count] = line
    f.close()
    return issues


# Drops the Issues table of the database, to be used in conjunction with
# get_new_issues() (to retrieve the updated list of issues from /repo/issues.txt)
# update_issues() (to update the database with updates.
def drop_issues(cursor):
    cursor.execute(sql_drop_issues)
    return True


# Insert an issue into the Issues table, this will be controlled by update_issues()
# and called while update_issues() is iterating through the updated issue list.
def add_issue(id,issue_description,cursor):
    sql = sql_insert_issue + id + ',' + issue_description + ')'
    cursor.execute(sql)
    return True


def update_issues(issues,cursor):
    # Instantiate new dict() object to hold the previous issues ID + ISSUE to compare against
    # the issues dict() in order to properly update audit_results_table if an ID changes for an
    # issue
    old_issues = get_issues(cursor)
    print "Issues Obtained From Database"
    old_count = len(old_issues)
    print "Old Issue Count: " + str(old_count)

    # Clear issues dict()
    issues.clear()
    # Assign issues dict() to results of get_new_issues() (returns dict() object)
    issues = get_new_issues()
    print "New Issue List Loaded"
    new_count = len(issues)
    print "New Issue Count: " + str(new_count)
    # Drop the current issues table, this will allow us to update/add an issue
    # And proper IDs will still be applied
    # TODO: Add ID updating function that on updates looks for IDs that have changed in the audit_results table
    drop_issues(cursor)
    print "Drop Issues Table"
    # Create the Issues table again to be populated with the updated list of issues
    create_issues_table(cursor)
    print "Create Issues Table"
    # Iterate through the updated issues dict() and for each key, value create a sql query string
    # and add each ID + ISSUE to the database
    for key, value in issues:
        sql = sql_insert_issue + str(key) + ',' + value + ')'
        cursor.execute(sql)
    print "Issues Table Populated"


def create_issues_table(cursor):
    cursor.execute(sql_create_issues)
    return True

    # def update_issues_changelog(old_issues,new_issues):


    # def update_issues_id(old_issues,new_issues):
    # TODO: Determine the best way to manage a changelog
    # I intend to use old_issues to manage current issue list, and new_issues to manage the data pulled
    # from /repo/issues.txt

if __name__ == "__main__":
    main()