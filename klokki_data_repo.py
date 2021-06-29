import sqlite3
from datetime import datetime
import pdb

class KlokkiDataRepo:

    def __init__(self):
        self.db_path = '../db/timepal.storedata'
        self.klokki_time_offset = 978285600
        self.conn = sqlite3.connect(self.db_path)

    def get_time_log_for_day(self, year, month, day):
        '''function gets all red colored sessions for the specified day'''
        max = datetime(year, month, day, 23, 59, 59).timestamp() - self.klokki_time_offset
        min = datetime(year, month, day).timestamp() - self.klokki_time_offset
        cursor = self.conn.execute('''
            SELECT N.ZNAME, S.ZBEGIN, S.ZCONFIRMEDDURATION, N.ZCOLORID FROM ZSESSION S
            LEFT JOIN ZNODE N ON S.ZTASK = N.Z_PK
            WHERE S.ZBEGIN < :max and S.ZBEGIN > :min
            ''', {'max':max, 'min':min})
        return [{
            'issue':a[0].split(' ')[0],
            'started':datetime.fromtimestamp(a[1] + self.klokki_time_offset),
            'timeSpentSeconds':a[2],
            'jira': a[3] == 0
            } for a in cursor]

