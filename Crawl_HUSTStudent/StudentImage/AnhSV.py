import shutil
import requests
import os
import datetime


def nextStudentID(curID):
    for i in range(len(curID) - 1, -1, -1):
        # Find first index has char < 9
        if int(curID[i]) < 9:
            nextID = curID[0:i] + str(int(curID[i]) + 1) + "0" * (len(curID) - i - 1)
            return nextID
    return "1" + "0" * len(curID)


def compare(id1, id2):
    if len(id1) < len(id2):
        return -1
    elif len(id1) > len(id2):
        return 1
    if id1 < id2:
        return -1
    elif id1 > id2:
        return 1
    else:
        return 0


def crawlAvatarHustStudent(startID, endID):
    if len(startID) != 8 or len(endID) != 8:
        return
    curId = startID
    totalCrawlImages = 0
    urlRootDirectory = "AvatarHustStudent/"

    if not os.path.exists(urlRootDirectory):
        os.mkdir(urlRootDirectory)
    curFatherDirectory = urlRootDirectory + curId[0:4]
    curChildDirectory = curFatherDirectory + "/" + (curId[-4::] + "-" + curId[-4] + "9" * 3)
    while compare(curId, endID) < 0:
        curFatherDirectory = urlRootDirectory + curId[0:4]
        # create new directory if not exist
        if not os.path.exists(curFatherDirectory):
            os.mkdir(curFatherDirectory)
        if curId[-3::] == "000":
            curChildDirectory = curFatherDirectory + "/" + (curId[-4::] + "-" + curId[-4] + "9" * 3) + "/"
            if not os.path.exists(curChildDirectory):
                os.mkdir(curChildDirectory)

        filePath = curChildDirectory + curId + ".jpg"
        if not os.path.exists(filePath):
            urlCrawl = "http://anhsv.hust.edu.vn/Student/" + str(curId) + ".jpg"
            response = requests.get(urlCrawl, stream=True)
            try:
                response.raise_for_status()
                with open(filePath, "wb") as file:
                    shutil.copyfileobj(response.raw, file)
                del response
                totalCrawlImages += 1
            except:
                print "Dont find image: ", curId

        curId = nextStudentID(curId)
    print "Total Crawl Images = ", totalCrawlImages

    # write statistic
    with open(urlRootDirectory + "Statistics.txt", "w") as file:
        now = datetime.datetime.now()
        strCurrentTime = now.strftime("%d/%m/%Y - %H:%M ")
        file.write("Last Update: " + strCurrentTime)
        file.write("\nDownload {0} images at last time".format(totalCrawlImages))
        for dirFather in os.listdir(urlRootDirectory):
            sumFile = 0
            path = os.path.join(os.path.abspath(urlRootDirectory), dirFather)
            for dirChild, subdir, files in os.walk(path):
                sumFile += len(files)
            if os.path.isdir(path):
                file.write("\nFolder " + dirFather + " : " + str(sumFile) + " images")


crawlAvatarHustStudent("20155000", "20160000")
