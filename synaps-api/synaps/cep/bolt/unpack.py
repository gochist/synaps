from uuid import UUID
import os
import md5
import json
import traceback
from synaps import flags
from synaps import log as logging
from synaps.cep import storm
from synaps.db import Cassandra
from synaps.rpc import (PUT_METRIC_DATA_MSG_ID, PUT_METRIC_ALARM_MSG_ID,
                        DELETE_ALARMS_MSG_ID, SET_ALARM_STATE_MSG_ID)

FLAGS = flags.FLAGS
LOG = logging.getLogger(__name__)
threshhold = 10000


class UnpackMessageBolt(storm.BasicBolt):
    BOLT_NAME = "UnpackMessageBolt"
    
    def initialize(self, stormconf, context):
        self.pid = os.getpid()
        self.cass = Cassandra()
        self.key_dict = {}
    
    def log(self, msg):
        LOG.info(msg)
        
    def tracelog(self, e):
        msg = traceback.format_exc(e)
        for line in msg.splitlines():
            self.log("TRACE: " + line)
                
    def get_metric_key(self, message):
        memory_key = md5.md5(str((message['project_id'],
                                  message['namespace'],
                                  message['metric_name'],
                                  message['dimensions']))).digest()
        
        if memory_key not in self.key_dict:
            if len(self.key_dict) > threshhold:
                self.key_dict.popitem()
            
            self.key_dict[memory_key] = self.cass.get_metric_key_or_create(
                 message['project_id'], message['namespace'],
                 message['metric_name'], message['dimensions'],
                 message['unit']
            )
            
        return self.key_dict[memory_key]
    
    def get_alarm_metric_key(self, alarmkey):
        alarm = self.cass.get_metric_alarm(alarmkey)
        if alarm:
            return str(alarm.get('metric_key'))
        else:
            return None

    def emit(self, tup):
        storm.emit(tup)
        self.log("Emitted %s" % tup)
    
    def process(self, tup):
        message_buf = tup.values[0]
        message = json.loads(message_buf)

        message_id = message['message_id']
        message_uuid = message['message_uuid']
        self.log("start processing msg[%s:%s]" % (message_id, message_uuid))
        
        if message_id == PUT_METRIC_DATA_MSG_ID:
            metric_key = str(self.get_metric_key(message))
            storm.emit([metric_key, message_buf])
        elif message_id == PUT_METRIC_ALARM_MSG_ID:
            metric_key = message.get('metric_key')
            storm.emit([metric_key, message_buf])
        elif message_id == DELETE_ALARMS_MSG_ID:
            project_id = message['project_id']
            alarmkeys = message['alarmkeys']
            for alarmkey in alarmkeys:
                try:
                    alarmkey_uuid = UUID(alarmkey)
                    metric_key = self.get_alarm_metric_key(alarmkey_uuid)
                    metric_key = str(metric_key)
                    if metric_key:
                        message['alarmkey'] = alarmkey
                        storm.emit([metric_key, json.dumps(message)])
                except Exception as e:
                    storm.log("Alarm %s does not exists" % alarmkey)
                    storm.log(traceback.format_exc(e))
        elif message_id == SET_ALARM_STATE_MSG_ID:
            project_id = message['project_id']
            alarm_name = message['alarm_name']
            alarm_key = self.cass.get_metric_alarm_key(project_id,
                                                       alarm_name)
            if alarm_key:
                alarm = self.cass.get_metric_alarm(alarm_key)
                metric_key = str(alarm['metric_key'])
                storm.emit([metric_key, json.dumps(message)])
