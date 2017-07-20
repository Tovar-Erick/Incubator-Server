import base64
from datetime import datetime

class imgContainer():

    def __init__(self, total_messages, camera_name, time, RBunit):
        self.total_messages = total_messages
        self.camera_name = camera_name
        self.time = time
        self.RBunit = RBunit
        self.imgChunks = {} # Image number, Image data

    def addChunk(self, message_number, data):
        self.imgChunks[message_number] = data

    def isImageComplete(self):
        isComplete = (len(self.imgChunks) == self.total_messages)
        # print( '{}/{}'.format(len(self.imgChunks), self.total_messages))
        # if isComplete:
        #     print('             Image complete!')
        return isComplete

imageDirectory = {}

#main function
def storeChunk(message):
    message_id = message['message_id']
    if imageDirectory.get(message_id) == None:
        storeFirstMessage(message)
    else:
        storeMessage(message)
        if isImageComplete(message_id):
            reconstructImage(message_id)
            removeFromDirectory(message_id)

def reconstructImage(message_id):
    chunks = imageDirectory[message_id].imgChunks
    encodedImageString = ''
    for imageNum in range(1, len(chunks)+1):
        imageData = chunks[imageNum]
        assert imageData != None, 'Image part #{} is MISSING, aborting reconstruct method'
        encodedImageString += imageData
    decodedImageString = base64.b64decode(encodedImageString)

    path = './photos/'
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    photo_name = path + message_id + now + '.jpg'
    with open(name=photo_name, mode='wb') as image_file:
        image_file.write(decodedImageString)

def isImageComplete(message_id):
    return (imageDirectory[message_id]).isImageComplete()

def removeFromDirectory(message_id):
    imageDirectory.pop(message_id)
    return

def storeFirstMessage(message):
    message_id = message['message_id']

    message_number = message['message_number']
    data = message['data']

    RBunit = message['RBunit']
    time = message['datetime']
    total_messages = message['total_messages']
    camera_name = message['camera_name']

    imageObj = imgContainer(total_messages, camera_name, time, RBunit)
    imageObj.addChunk(message_number, data)
    imageDirectory[message_id] = imageObj


def storeMessage(message):
    message_id = message['message_id']
    message_number = message['message_number']

    data = message['data']
    (imageDirectory[message_id]).addChunk(message_number, data)
