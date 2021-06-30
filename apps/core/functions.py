from project import settings
import requests
import cv2

import urllib.request
import urllib.parse


def imageFromVideo(videoPath, imagePath):
    video = cv2.VideoCapture(videoPath)
    framsQty = video.get(3)
    middleFrame = int(framsQty / 2)
    count = 0
    success = 1
    while success:
        success, image = video.read()
        if count == 1:
            path = "/%s.jpg" % imagePath
            cv2.imwrite("./media/%s.jpg" % imagePath, image)
        if count >= middleFrame:
            path = "/%s.jpg" % imagePath
            cv2.imwrite("./media/%s.jpg" % imagePath, image)
            break
        count += 1
    return path



def send_telegeram(mesage):
    if type(mesage) == list:
        bot_message = urllib.parse.quote('\n'.join(mesage))
    else:
        bot_message = urllib.parse.quote(mesage)
    url = f'https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage?chat_id={settings.BOT_CHATID}&text='+bot_message
    response = urllib.request.urlopen(url).read()
    return response


