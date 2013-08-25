from synaps import flags
from synaps import log as logging

FLAGS = flags.FLAGS
LOG = logging.getLogger(__name__)

from synaps.db import Cassandra
from synaps.rpc import CHECK_METRIC_ALARM_MSG_ID
from synaps.cep.storm import Spout, emit, log
from uuid import uuid4
import json
import os
import time
import traceback

class CheckSpout(Spout):
    SPOUT_NAME = "CheckSpout"
    lastchecked = 0
    
    def initialize(self, conf, context):
        self.pid = os.getpid()
        self.cass = Cassandra()
        self.nextTuple()
        self.delivery_tags = {}
        self.lastchecked = time.time()
    
    def nextTuple(self):
        now = time.time()
        if self.lastchecked == 0:
            self.lastchecked = now
        elif now - self.lastchecked >= 60: 
            self.lastchecked = now
            id = "periodic_%s" % str(uuid4())
            body = json.dumps({'message_id': CHECK_METRIC_ALARM_MSG_ID})
            message = "Periodic monitoring message sent [%s] %s"
            LOG.debug(message % (id, body))
            emit([None, body], id=id)
        else:
            time.sleep(1)
