import SharedData.Defaults
from SharedData.AWSKinesis import KinesisStreamProducer
from SharedData.Logger import Logger
import os
import sys
import json

from SharedData.SharedData import SharedData
shdata = SharedData('SharedData.Routines.SendCommand', user='master')

producer = KinesisStreamProducer(os.environ['WORKERPOOL_STREAM'])

if len(sys.argv) >= 2:
    _argv = sys.argv[1:]
else:
    Logger.log.error('command not provided!')
    raise Exception('command not provided!')

try:
    data_str = ''.join(_argv)
    data_str = data_str.replace('\'', '\"')
    data = json.loads(data_str)
except Exception as e:
    Logger.log.error('master error:%' % (e))

producer.produce(data, 'command')
