import sys
import sqlite3
from uriUtils import domainFromUri


# this is a pointer to the module object instance itself.
this = sys.modules[__name__]


this.conn = None
this.dbFileName = "timesheet2.db"
this.conn = None


def create_connection():
    try:
        # Is this Safe ?
        this.conn = sqlite3.connect(this.dbFileName,  check_same_thread=False)
        this.conn.row_factory = sqlite3.Row
    except Exception as e:
        print(e)


def create_table(create_table_sql):
    try:
        c = this.conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        print(e)


def getAllActivities():
    """
    Query all rows in the activities table
    :return:
    """
    cur = this.conn.cursor()
    cur.execute("SELECT * FROM activities")
    rows = [dict(row) for row in cur.fetchall()]

    return rows


def getAllSegments():
    """
    Query all rows in the segments table
    :return:
    """
    cur = this.conn.cursor()
    cur.execute("SELECT * FROM segments")
    rows = [dict(row) for row in cur.fetchall()]

    return rows


def getAllDomains():
    """
    Query all rows in the domains table
    :return:
    """
    cur = this.conn.cursor()
    cur.execute("SELECT * FROM domains")
    rows = [dict(row) for row in cur.fetchall()]

    return rows


def createActivity(activityBundleIdentifier, activityLocalizedName):
    """
    Create a new activity into the activities table
    :param activity:
    :return: activity id
    """
    sql = 'SELECT * FROM activities WHERE activityBundleIdentifier=?'
    cur = this.conn.cursor()
    cur.execute(sql, (activityBundleIdentifier,))
    entry = cur.fetchone()

    if entry is None:
        sql = ''' INSERT INTO activities(activityBundleIdentifier, activityLocalizedName)
            VALUES(?,?) '''
        cur.execute(sql, (activityBundleIdentifier, activityLocalizedName))
        entry = cur.lastrowid
    else:
        entry = entry['id']

    return entry


def createDomain(uri):
    domain = domainFromUri(uri)
    sql = 'SELECT * FROM domains WHERE domain=?'
    cur = this.conn.cursor()
    cur.execute(sql, (domain,))
    entry = cur.fetchone()

    if entry is None:
        sql = ''' INSERT INTO domains(domain)
            VALUES(?) '''
        cur.execute(sql, (domain,))
        entry = cur.lastrowid
    else:
        entry = entry['id']

    return entry


def createSegment(activityId, domainId, startTime, endTime, url):
    sql = ''' INSERT INTO segments(activityId, domainId, startTime, endTime, url)
            VALUES(?,?,?,?, ?) '''
    cur = this.conn.cursor()
    cur.execute(sql, (activityId, domainId, startTime, endTime, url))
    entry = cur.lastrowid

    return entry


def addEntry(activityBundleIdentifier, activityLocalizedName, startTime, endTime, isBrowser, url):
    try:
        activityId = createActivity(
            activityBundleIdentifier, activityLocalizedName)
        domainId = None

        if isBrowser:
            domainId = createDomain(url)

        createSegment(activityId, domainId, startTime, endTime, url)
        this.conn.commit()
    except Exception as e:
        this.conn.rollback()
        print(e)


def initDB():
    sql_create_activities_table = """ CREATE TABLE IF NOT EXISTS activities (
                                        id integer PRIMARY KEY,
                                        activityBundleIdentifier text NOT NULL,
                                        activityLocalizedName text NOT NULL
                                    ); """

    sql_create_segments_table = """CREATE TABLE IF NOT EXISTS segments (
                                    id integer PRIMARY KEY,
                                    activityId integer NOT NULL,
                                    domainId integer,
                                    startTime integer NOT NULL,
                                    endTime integer NOT NULL,
                                    url text,
                                    FOREIGN KEY (activityId) REFERENCES activities (id)
                                );"""

    sql_create_domains_table = """CREATE TABLE IF NOT EXISTS domains (
                                    id integer PRIMARY KEY,
                                    domain text NOT NULL
                                );"""

    if this.conn is not None:
        create_table(sql_create_activities_table)
        create_table(sql_create_segments_table)
        create_table(sql_create_domains_table)
    else:
        print("Error! cannot create the database connection.")


create_connection()
initDB()
