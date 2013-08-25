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
from datetime import datetime, timedelta
import traceback
import time

class CheckSpout(Spout):
    SPOUT_NAME = "CheckSpout"
    lastchecked = datetime.utcnow().replace(second=0, microsecond=0)


    def ack(self, id):
        LOG.info("Acked message [%s]" % id)


    def fail(self, id):
        LOG.error("Reject failed message [%s]" % id)

    
    def initialize(self, conf, context):
        self.pid = os.getpid()
        self.cass = Cassandra()
        self.nextTuple()
        self.delivery_tags = {}
        self.lastchecked = time.time()

    
    def nextTuple(self):
        now = datetime.utcnow().replace(second=0, microsecond=0)
        if self.lastchecked != now:
            self.lastchecked = now
            msg_id = "periodic_%s" % str(uuid4())
            body = json.dumps({'message_id': CHECK_METRIC_ALARM_MSG_ID})
            message = "Periodic monitoring message sent %s"
            LOG.info(message, msg_id)
            emit([None, body], id=msg_id)
        else:
            time.sleep(1)
