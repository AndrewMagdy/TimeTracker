import sqlite3
from uriUtils import domainFromUri

dbFileName = "timesheet.db"

class DB:
    conn = None
    dbFileName = "timesheet2.db"

    def __init__(self):
        self.create_connection()
        self.initDB()

    def create_connection(self):
        try:
            # Is this Safe ?
            self.conn = sqlite3.connect(self.dbFileName,  check_same_thread=False) 
            self.conn.row_factory = sqlite3.Row
        except Exception as e:
            print(e)

        return None

    def create_table(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Exception as e:
            print(e)

    def createActivity(self, activityBundleIdentifier, activityLocalizedName):
        """
        Create a new activity into the activities table
        :param activity:
        :return: activity id
        """
        sql = 'SELECT * FROM activities WHERE activityBundleIdentifier=?'
        cur =  self.conn.cursor()
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

    def createDomain(self, uri):
        domain = domainFromUri(uri)
        sql = 'SELECT * FROM domains WHERE domain=?'
        cur =  self.conn.cursor()
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

    def createSegment(self, activityId, domainId, startTime, endTime, url):
        sql = ''' INSERT INTO segments(activityId, domainId, startTime, endTime, url)
                VALUES(?,?,?,?, ?) '''
        cur =  self.conn.cursor()
        cur.execute(sql, (activityId, domainId, startTime, endTime, url))
        entry = cur.lastrowid

        return entry


    def addEntry(self, activityBundleIdentifier, activityLocalizedName, startTime, endTime, isBrowser, url):
        try:
            activityId = self.createActivity(activityBundleIdentifier, activityLocalizedName)
            domainId = None

            if isBrowser:
                domainId = self.createDomain(url)

            self.createSegment(activityId, domainId, startTime, endTime, url)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)
             

    def initDB(self):
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

        if self.conn is not None:
            self.create_table(sql_create_activities_table)
            self.create_table(sql_create_segments_table)
            self.create_table(sql_create_domains_table)
        else:
            print("Error! cannot create the database connection.")
