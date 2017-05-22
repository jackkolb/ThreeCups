import numpy as np
import cv2
import math
from Arduino import Arduino

def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

class DetectedObject(object):
    def __init__(self):
        self.posx = 0
        self.posy = 0

def tracking(board, initialcup):
    cups = 3
    cap = cv2.VideoCapture(1)
    yres = 500
    xres = 500
    cap.set(4, xres)
    cap.set(5, yres)

    objects = []
    for i in range(0, cups):
        ob = DetectedObject()
        objects.append(ob)

    lower = np.array([240, 240, 240], dtype="uint8")
    upper = np.array([255, 255, 255], dtype="uint8")

    posxs = [1,1,1]
    posys = [1,1,1]
    openSE = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    closeSE = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))

    params = cv2.SimpleBlobDetector_Params()
    params.filterByColor = True
    params.blobColor = 255
    params.filterByArea = True
    params.minArea = 300.0


    while True: # Capture frame-by-frame

        ret, frame = cap.read()  # Our operations on the frame come here

        mask = cv2.inRange(frame, lower, upper)
        output = cv2.bitwise_and(frame, frame, mask=mask)
        output = cv2.medianBlur(output, 5)
        output = cv2.morphologyEx(output, cv2.MORPH_OPEN, openSE)
        keypoints = cv2.SimpleBlobDetector_create(params).detect(output)

        output = cv2.drawKeypoints(output, keypoints, np.array([]), (0, 255, 0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        for i in range(0, len(objects)):
            cv2.putText(output, str(i), (int(objects[i].posx), int(objects[i].posy)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Keypoints", output)

        if (cv2.waitKey(1) & 0xFF == ord(' ')) or board.digitalRead(11): # pin 11 is the signal button pin
            objectsfinalposx = []
            for i in range(len(objects)):
                objectsfinalposx.append(int(objects[i].posx))

            objectsfinalposx.sort()
            returnint = objectsfinalposx.index(int(objects[0].posx))+1
            break

        if len(keypoints) != cups:
            continue


        usedkeys = [int] * 3

        prevobjxs = [1,1,1]
        prevobjys = [1,1,1]

        keylocxs = [int] * 3
        keylocys = [int] * 3

        for i in range(0, len(objects)):
            obposx = int(objects[i].posx)
            obposy = int(objects[i].posy)
            prevobjxs[i] = obposx
            prevobjys[i] = obposy

            usedkeys[i] = obposx

            if obposx == 0:
                objects[i].posx = int(keypoints[i].pt[0])
                objects[i].posy = int(keypoints[i].pt[1])
                continue

            objectdist = []



            for j in range(0, len(keypoints)):
                keyx = int(keypoints[j].pt[0])
                keylocxs[j] = keyx
                keyy = int(keypoints[j].pt[1])
                keylocys[j] = keyy
                dist = math.sqrt((keyx - obposx) * (keyx - obposx) + (keyy - obposy) * (keyy - obposy))
                objectdist.append(dist)

            keyloc = objectdist.index(min(objectdist))
            objects[i].posx = int(keypoints[keyloc].pt[0])
            objects[i].posy = int(keypoints[keyloc].pt[1])

            posxs[i] = objects[i].posx
            posys[i] = objects[i].posy

        duplist = []

        currobjxs = posxs #object position lists
        currobjys = posys

        blobxs = keylocxs #blob position lists
        blobys = keylocys

        if (len(list_duplicates_of(posxs, posxs[0])) == 2 or len(list_duplicates_of(posxs, posxs[1])) == 2):
            if len(list_duplicates_of(posxs, posxs[0])) != 1:
                duplist = list_duplicates_of(posxs, posxs[0])
            elif len(list_duplicates_of(posxs, posxs[1])) != 1:
                duplist = list_duplicates_of(posxs, posxs[1])
            elif len(list_duplicates_of(posxs, posxs[2])) != 1:
                duplist = list_duplicates_of(posxs, posxs[2])
            if (0 in duplist) and (1 in duplist):
                singlekey = 2
            elif (0 in duplist) and (2 in duplist):
                singlekey = 1
            elif (1 in duplist) and (2 in duplist):
                singlekey = 0
            if ((duplist[0] == 0 or duplist[1] == 0) and (singlekey == 1)) or ((duplist[0] == 1 or duplist[1] == 1) and (singlekey == 0)):
                emptykey = 2
            elif ((duplist[0] == 1 or duplist[1] == 1) and (singlekey == 2)) or ((duplist[0] == 2 or duplist[1] == 2) and (singlekey == 1)):
                emptykey = 0
            elif ((duplist[0] == 2 or duplist[1] == 2) and (singlekey == 0)) or ((duplist[0] == 0 or duplist[1] == 0) and (singlekey == 2)):
                emptykey = 1
            distance0 = math.sqrt((prevobjxs[duplist[0]] - currobjxs[duplist[0]])**2 + (prevobjys[duplist[0]] - currobjys[duplist[0]])**2)
            distance1 = math.sqrt((prevobjxs[duplist[0]] - currobjxs[duplist[0]])**2 + (prevobjys[duplist[0]] - currobjys[duplist[0]])**2)

            if distance0 > distance1:
                objects[duplist[0]].posx = blobxs[emptykey]
                objects[duplist[0]].posy = blobys[emptykey]
            else:
                objects[duplist[1]].posx = blobxs[emptykey]
                objects[duplist[1]].posy = blobys[emptykey]

    cap.release()
    cv2.destroyAllWindows()
    return returnint


