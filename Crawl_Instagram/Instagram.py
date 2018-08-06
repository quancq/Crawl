# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *

import shutil
import requests
import os
import time
import datetime
import math


def getImageName(src):
    # get name image
    for index in range(len(src) - 1, -1, -1):
        if src[index] == '/':
            return src[index + 1:]
    return None


def downloadImage(src, folder, typeImage):
    rootDir = "Instagram"
    userDir = os.path.join(rootDir, folder)
    typeImgDir = os.path.join(userDir, typeImage)
    imageName = getImageName(src)
    pathFile = os.path.join(typeImgDir, imageName)

    if not os.path.exists(rootDir):
        os.mkdir(rootDir)
    if not os.path.exists(userDir):
        os.mkdir(userDir)
    if not os.path.exists(typeImgDir):
        os.mkdir(typeImgDir)
    if os.path.exists(pathFile):
        return False

    try:
        respone = requests.get(src, stream=True)
        respone.raise_for_status()
        with open(pathFile, "wb") as file:
            shutil.copyfileobj(respone.raw, file)
        del respone
        return True
    except:
        return False


# driver.get(urlInstagram)

# listATag = driver.find_elements_by_tag_name("a")
# listHref = [aTag.get_attribute("href") for aTag in listATag
#             if ("taken-by=" + userName) in aTag.get_attribute("href")]
# listHref = []
# listNameImg = []
# for aTag in listATag:
#     if ("taken-by=" + userName) in aTag.get_attribute("href"):
#         listHref.append(aTag.get_attribute("href"))
#         imgSmall = aTag.find_element_by_tag_name("img")
#         listNameImg.append(getImageName(imgSmall.get_attribute("src")))
#
# print listNameImg
#
# for index in range(0, len(listHref)):
#     href = listHref[index]
#     nameImage = listNameImg[index]
#     print nameImage
#     driver.get(href);
#     imgBig = None
#     while True:
#         listImg = driver.find_elements_by_tag_name("img")
#         for img in listImg:
#             if nameImage in img.get_attribute("src"):
#                 imgBig = img
#                 break
#         else:
#             continue
#         break
#
#     srcImage = imgBig.get_attribute("src")
#     if downloadImage(srcImage, userName):
#         print "Down load {0} thanh cong".format(srcImage)
def crawlInstagramImages(userNameTarget="mtpsontung", maxDownloadImages=30,
                         isDownloadSmallImages=True, isDownloadBigImages=True,
                         userNameCrawler="chuquocquan96@gmail.com", pwdCrawler="quanchu"):
    driver = webdriver.Firefox()
    # login instagram
    driver.get("https://www.instagram.com/accounts/login/")
    formLogin = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.TAG_NAME, "form"))
    )
    inputUserName = formLogin.find_element_by_css_selector("input[name=username]")
    inputPassword = formLogin.find_element_by_css_selector("input[name=password]")
    btnLogin = formLogin.find_element_by_tag_name("button")

    inputUserName.clear()
    inputUserName.send_keys(userNameCrawler)
    inputPassword.clear()
    inputPassword.send_keys(pwdCrawler)
    btnLogin.click()

    # wait login successfull
    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "html[class='js logged-in client-root']"))
    )


    listHref = []
    listSrcSmallImg = []
    listNameImg = []
    # offsetTop = 700 + int(math.ceil(1.0 * maxDownloadImages / 3)) * 400
    numberDownloadedImages = 0
    # lastNumberDownloadedImages = 0

    # userName = "mtpsontung"
    urlInstagram = "https://www.instagram.com/" + userNameTarget
    driver.get(urlInstagram)
    # check btn Download more exist
    btnDownloadMore = None
    isExistBtnDownloadMore = True
    listATag = driver.find_elements_by_tag_name("a")
    for aTag in listATag:
        if userNameTarget in aTag.get_attribute("href") and \
                (aTag.get_attribute("innerHTML") == u"Tải thêm" or \
                             aTag.get_attribute("innerHTML") == "Load more"):
            btnDownloadMore = aTag
            print "Da tim thay btn load more"
            break
    else:
        isExistBtnDownloadMore = False
    if isExistBtnDownloadMore:
        btnDownloadMore.click()
        # wait 1s for load more images
        time.sleep(1)
    # loop scroll window until get enough number images
    top = 0
    count = 0
    listATag = []
    lastLenListATag = 0
    numLoadedImages = 0
    while True:
        print "num loaded images = ", numLoadedImages
        if count == 0:
            lastLenListATag = numLoadedImages
        driver.execute_script("window.scrollTo(0," + str(top) + ")")
        # if top >= offsetTop:
        #     break
        top += 1000
        # wait 0.4s
        time.sleep(0.4)
        listATag = driver.find_elements_by_tag_name("a")

        # check load enough images
        numLoadedImages = 0
        for aTag in listATag:
            if ("taken-by=" + userNameTarget) in aTag.get_attribute("href"):
                numLoadedImages += 1
        if numLoadedImages >= maxDownloadImages:
            print "num loaded img cuoi cung  line163 = ", numLoadedImages
            break
        count = (count + 1) % 5
        if count == 0:
            if lastLenListATag >= numLoadedImages:
                # scroll more 5 times but no load more images
                print "num loaded img cuoi cung  line169 = ", numLoadedImages
                break

    # load images
    # listATag = driver.find_elements_by_tag_name("a")
    for aTag in listATag:
        if ("taken-by=" + userNameTarget) in aTag.get_attribute("href"):
            listHref.append(aTag.get_attribute("href"))
            imgSmall = aTag.find_element_by_tag_name("img")
            listNameImg.append(getImageName(imgSmall.get_attribute("src")))
            listSrcSmallImg.append(imgSmall.get_attribute("src"))
    # remove images downloaded
    # listHref = listHref[numberDownloadedImages:]
    # listNameImg = listNameImg[numberDownloadedImages:]
    # listSrcSmallImg = listSrcSmallImg[numberDownloadedImages:]

    # download images
    print "sap down {} images".format(len(listHref))
    for index in range(0, len(listHref)):
        if isDownloadSmallImages:
            downloadImage(listSrcSmallImg[index], userNameTarget, "SmallImages")
        if isDownloadBigImages:
            nameImage = listNameImg[index]
            href = listHref[index]
            driver.get(href);
            imgBig = None
            time.sleep(1)
            listImg = driver.find_elements_by_tag_name("img")
            for img in listImg:
                if nameImage in img.get_attribute("src"):
                    imgBig = img
                    break

            if imgBig:
                srcImage = imgBig.get_attribute("src")
                downloadImage(srcImage, userNameTarget, "BigImages")
        numberDownloadedImages += 1

        if numberDownloadedImages >= maxDownloadImages:
            break

    print "Da down tat ca la {0} images".format(numberDownloadedImages)
    os.system("taskkill /f /im geckodriver.exe")


crawlInstagramImages()
