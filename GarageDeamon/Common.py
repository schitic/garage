import sqlite3
from datetime import datetime
from GarageDeamon.Logger import LogCreator


class SensorBase(object):

    def __init__(self, sensor_name=None):
        if sensor_name:
            self.sensor_name = sensor_name
        else:
            self.sensor_name = self.__class__.__name__
        self.log = LogCreator()
        self.log.write("", "INIT", component_id=self.sensor_name)
        self.current_state = self._current_state()
        self._merge_state()

    def get_state(self):
        return self.current_state

    def set_state(self, value):
        self.current_state = value
        self._set_state()

    def _merge_state(self):
        db_state = Utils.get_state(self.sensor_name)
        if self.current_state is None:
            self.current_state = db_state
        elif self.current_state != db_state:
            self.log.write("Changed Value: from %s to %s" %
                           (db_state, self.current_state),
                           "DBMERGE", component_id=self.sensor_name)
            self._set_state()

    def _set_state(self):
        if self.current_state is not None:
            self.log.write("Value: %s" % self.current_state,
                           "DBSAVE", component_id=self.sensor_name)
            Utils.save_state(self.sensor_name, self.current_state)


class ActorBase(object):
    def __init__(self, actor_name=None):
        if actor_name:
            self.actor_name = actor_name
        else:
            self.actor_name = self.__class__.__name__


class Utils(object):

    @staticmethod
    def save_state(sensor_name, sensor_value):
        db = _DataBase()
        db.insert_or_update(sensor_name, sensor_value)
        db.close()

    @staticmethod
    def get_state(sensor_name):
        db = _DataBase()
        rows = db.query(sensor_name)
        db.close()
        if rows:
            return rows[0][0]
        return None


class _DataBase(object):

    def __init__(self):
        self.conn = sqlite3.connect('garage.db')
        self._create_table()

    def close(self):
        self.conn.close()

    def _create_table(self):
        sql = 'create table if not exists sensors ' \
              '(uid INTEGER PRIMARY KEY, ' \
              'sensorName TEXT, sensorValue TEXT, time TEXT);'
        self.conn.execute(sql)
        self.conn.commit()

    def query(self, sensor_name):
        cur = self.conn.cursor()
        cur.execute("SELECT sensorValue FROM sensors "
                    "WHERE sensorName = '%s'" % sensor_name)
        rows = cur.fetchall()
        return rows

    def queryALL(self):
        cur = self.conn.cursor()
        cur.execute("SELECT sensorValue FROM sensors ")
        rows = cur.fetchall()
        return rows

    def insert_or_update(self, sensor_name, sensor_value):
        dtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if len(self.query(sensor_name)):
            sql = "UPDATE sensors SET sensorValue='%s' " \
                  "WHERE sensorName='%s'" % (sensor_value, sensor_name)

        else:
            last_row_id = len(self.queryALL())
            if not last_row_id:
                last_row_id = 1
            sql = 'INSERT INTO sensors VALUES(%s,\'%s\', \'%s\', \'%s\');' % (
                last_row_id,
                sensor_name,
                sensor_value,
                dtime
            )
        self.conn.execute(sql)
        self.conn.commit()

