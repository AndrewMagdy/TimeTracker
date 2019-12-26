import sqlite3
dbFileName = "timesheet.db"

class DB:
    conn = None
    dbFileName = "timesheet.db"

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

    def createActivity(self, activity):
        """
        Create a new activity into the activities table
        :param activity:
        :return: activity id
        """
        sql = 'SELECT * FROM activities WHERE name=?'
        cur =  self.conn.cursor()
        cur.execute(sql, (activity,))
        entry = cur.fetchone()

        if entry is None:
            sql = ''' INSERT INTO activities(name, extraInfo)
                VALUES(?,?) '''
            cur.execute(sql, (activity, ""))
            entry = cur.lastrowid
        else:
            entry = entry['id']
        
        return entry


    def createSegment(self, activityId, startTime, endTime, browser, url):
        sql = ''' INSERT INTO segments(activity_id, startTime, endTime, browser, url)
                VALUES(?,?,?,?,?) '''
        cur =  self.conn.cursor()
        cur.execute(sql, (activityId, startTime, endTime, browser, url))
        entry = cur.lastrowid

        return entry

    def addEntry(self, activity, startTime, endTime, browser, url):
        try:
            activityId = self.createActivity(activity)
            print ("Activity ID", activityId)
            entry = self.createSegment(activityId, startTime, endTime, browser, url)
            print ('HEllo', entry)
            self.conn.commit()
            return entry
        except Exception as e:
            self.conn.rollback()
            print(e)
             

    def initDB(self):
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

        if self.conn is not None:
            self.create_table(sql_create_activities_table)
            self.create_table(sql_create_segments_table)
        else:
            print("Error! cannot create the database connection.")
