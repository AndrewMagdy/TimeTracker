import sqlite3
dbFileName = "timesheet.db"


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def createActivity(conn, activity):
    """
    Create a new activity into the activities table
    :param conn:
    :param activity:
    :return: activity id
    """
    sql = 'SELECT * FROM activities WHERE (name=?)', activity
    cur.execute(sql)
    entry = self.cur.fetchone()
    if entry is None:
        sql = ''' INSERT INTO activities(name, extraInfo)
            VALUES(?,?) '''
        cur = conn.cursor()
        cur.execute(sql, activity)
    return cur.lastrowid


def initDB():
    sql_create_activities_table = """ CREATE TABLE IF NOT EXISTS activities (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        extraInfo text
                                    ); """

    sql_create_segments_table = """CREATE TABLE IF NOT EXISTS segments (
                                    id integer PRIMARY KEY,
                                    activity_id integer NOT NULL,
                                    startTime integer NOT NULL,
                                    endTime integer NOT NULL,
                                    browser text,
                                    url text,
                                    FOREIGN KEY (activity_id) REFERENCES activities (id)
                                );"""

    conn = create_connection(dbFileName)
    if conn is not None:
        create_table(conn, sql_create_activities_table)
        create_table(conn, sql_create_segments_table)
    else:
        print("Error! cannot create the database connection.")
