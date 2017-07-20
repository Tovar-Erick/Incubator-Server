
import time, sys
import logging
from datetime import datetime
import json
sys.path.insert(0, '/media/jica/PythonProjects/SynchronizeDb')
import sqlInterface
sys.path.insert(0, '/media/jica/PythonProjects/httpPost')
import post

sys.path.insert(0,'./utils')
from mqttListener import myMqtt
import imageRebuilder

def processCameraMessage(message):
    messageType = message['message_type']
    if messageType == 'camera':
        imageRebuilder.storeChunk(message)
    else:
        logging.warning('Invalid message arrived to camera channel')

def processSensorMessage(message):
    messageType = message['message_type']
    if messageType == 'sensor':
        sensor_name = message['sensor_name']
        value = message['measurement']
        time = message['datetime']
        RBunit = message['RBunit']
        storeSensorMessage(sensor_name, value, time, RBunit)
        post_message(sensor_name, value, time, RBunit)
    else:
        logging.warning('Invalid message arrived to camera channel')


def storeSensorMessage(sensor_name, value, time, RBunit):
    localPath = '/media/jica/PythonProjects/SynchronizeDb/'
    dbFilename = 'devices.db'
    dbPathFilename = localPath + dbFilename
    sqlInterface.setDb(dbPathFilename)
    sqlInterface.insert_measurement(sensor=sensor_name, value=value)

def post_message(sensor_name, value, time, RBunit):
    print('posteare {}'.format(sensor_name))
    post.post_heroku(sensor=sensor_name, value=value, timestamp=time)


def main():
    print('Starting...')
    logger = logging.getLogger(__name__)
    listener = myMqtt('JICA/Plantitas/#', processSensorMessage, processCameraMessage)
    listener.start_listening()

if __name__ == '__main__':
    main()
