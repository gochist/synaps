
import os
import traceback
import pika
import json
import time
from pika.exceptions import AMQPConnectionError, AMQPChannelError
from synaps import flags
from synaps import log as logging
from synaps.cep.storm import Spout, emit, log

FLAGS = flags.FLAGS
LOG = logging.getLogger(__name__)


class ApiSpout(Spout):
    SPOUT_NAME = "APISpout"
    
    def initialize(self, conf, context):
        self.pid = os.getpid()       
        self.connect()
        LOG.info("THIS IS HANDLERS %s", LOG.logger.handlers)
    

    def log(self, msg):
        LOG.info(msg)
    
    
    def connect(self):
        while True:
            try:
                self._connect()
            except (AMQPConnectionError, AMQPChannelError):
                self.log("AMQP Connection Error. Retry in 3 seconds.")
                time.sleep(3)            
            else:
                break
    
    def _connect(self):
        self.conn = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=FLAGS.get('rabbit_host'),
                port=FLAGS.get('rabbit_port'),
                credentials=pika.PlainCredentials(
                    FLAGS.get('rabbit_userid'),
                    FLAGS.get('rabbit_password')
                ),
                virtual_host=FLAGS.get('rabbit_virtual_host'),
            )
        )        
        
        self.channel = self.conn.channel()
        queue_args = {"x-ha-policy" : "all" }
        self.channel.queue_declare(queue='metric_queue', durable=True,
                                   arguments=queue_args)


    def ack(self, id):
        LOG.info("Acked message %s", id)

            
    def fail(self, id):
        LOG.error("Reject failed message %s", id)

    
    def nextTuple(self):
        try:
            (method_frame, header_frame, body) = self.channel.basic_get(
                queue="metric_queue", no_ack=True
            )
        except (AMQPConnectionError, AMQPChannelError):
            LOG.error("AMQP Connection or Channel Error. While get a message.")
            self.connect()
            return

        if method_frame:
            mq_msg_id = method_frame.delivery_tag
            msg_body = json.loads(body)
            msg_id, msg_uuid = msg_body['message_id'], msg_body['message_uuid']
            message = "Start processing message in the queue - [%s:%s]"
            LOG.info(message, msg_id, msg_uuid)
            emit([body], id=msg_uuid)
