# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
import os
import pypyodbc

import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == "__main__":

    rootFolder = "DanhSachSV"
    if not os.path.exists(rootFolder):
        os.mkdir(rootFolder)

    driver = webdriver.Firefox()
    driver.get("http://sis.hust.edu.vn/ModuleSearch/GroupList.aspx")

    tblCourse = WebDriverWait(driver, 200).until(
        EC.presence_of_element_located((By.ID, "MainContent_cbStudyCourse_DDD_L_LBT"))
    )
    # get list course
    listCourse = []
    listCourseItemTD = tblCourse.find_elements_by_tag_name("td")
    for courseItemTD in listCourseItemTD:
        listCourse.append(courseItemTD.get_attribute("innerHTML"))
    print "list course: ", listCourse

    tblFaculty = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "MainContent_cbFaculty_DDD_L_LBT"))
    )
    # get list faculty
    listFaculty = []
    listFacultyItemTD = tblFaculty.find_elements_by_tag_name("td")
    for facultyItemTD in listFacultyItemTD:
        listFaculty.append(facultyItemTD.get_attribute("innerHTML"))

    tblGroup = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "MainContent_cbGroup_DDD_L_LBT"))
    )

    cmbCourse = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "MainContent_cbStudyCourse_B-1"))
    )
    cmbFaculty = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "MainContent_cbFaculty_B-1"))
    )
    cmbGroup = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "MainContent_cbGroup_B-1"))
    )

    dictCourse = {}
    isFirstCourse = True
    numberPixelcourse = 0
    for courseItemTD in listCourseItemTD:
        numStudentPerCourse = 0
        cmbCourse.click()
        # scroll down 20px if is not first item
        if isFirstCourse:
            isFirstCourse = False
        else:
            while True:
                divCourse = driver.find_element_by_id("MainContent_cbStudyCourse_DDD_PW-1")
                if "visibility: visible" in divCourse.get_attribute("style"):
                    break
            driver.execute_script(
                "$('#MainContent_cbStudyCourse_DDD_L_D').animate({scrollTop: '+=21px'})")
            try:
                WebDriverWait(driver, 0.5).until(
                    EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#MainCtent_gvStudents_DXTitle td"),
                                                         nameGroup)
                )
            except:
                driver.execute_script(
                    "$('#MainContent_cbStudyCourse_DDD_L_D').animate({scrollTop: '+=21px'})")
        numberPixelcourse += 22
        courseItemTD.click()

        nameCourse = courseItemTD.get_attribute("innerHTML")
        numCourse = int(nameCourse)

        pathFile = os.path.join(rootFolder,nameCourse + ".txt")
        with open(pathFile, "w") as f:
            # select faculty
            dictFaculty = {}
            isFirstFaculty = True
            numberPixelFaculty = 0

            for facultyItemTD in listFacultyItemTD:
                cmbFaculty.click()
                nameFaculty = facultyItemTD.get_attribute("innerHTML")
                # scroll down 20px if is not first item
                # if isFirstFaculty:
                #     isFirstFaculty = False
                # else:
                #     # while True:
                #     #     divFaculty = driver.find_element_by_id("MainContent_cbFaculty_DDD_PW-1")
                #     #     if "visibility: visible" in divFaculty.get_attribute("style"):
                #     #         break
                #     driver.execute_script(
                #         "$('#MainContent_cbFaculty_DDD_L_D').animate({scrollTop: '+=" + str(numberPixelFaculty) + "px'})")

                driver.execute_script(
                    "$('#MainContent_cbFaculty_DDD_L_D').animate({scrollTop: '" + str(numberPixelFaculty) + "px'})")
                try:
                    WebDriverWait(driver, 0.5).until(
                        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#MainCtent_gvStudents_DXTitle td"),
                                                         nameGroup)
                    )
                except:
                    driver.execute_script(
                        "$('#MainContent_cbFaculty_DDD_L_D').animate({scrollTop: '" + str(numberPixelFaculty) + "px'})")
                numberPixelFaculty += 22
                facultyItemTD.click()
                # time.sleep(0.2)
                # wait load list group
                try:
                    WebDriverWait(driver, 1.5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#MainContent_cbGroup_DDD_L_LBT td"))
                    )
                except:
                    print "{} khong co lop".format(nameFaculty)


                # select group
                # get list course td except first td
                listGroupItemTD = []
                startTime = time.time()
                while True:
                    try:
                        listGroupItemTD = tblGroup.find_elements_by_tag_name("td")
                        if (time.time()-startTime) > 2:
                            break
                        if len(listGroupItemTD) == 0:
                            continue
                    except:
                        # break
                        continue
                    break
                isFirstItem = True
                dictGroup = {}
                isFirstGroup = True
                numberPixelGroup = 22
                for groupItemTD in listGroupItemTD:
                    if isFirstItem:
                        isFirstItem = False
                        continue
                    cmbGroup.click()
                    # scroll down 20px if is not first item
                    # divScrollGroup = driver.find_element_by_id("MainContent_cbGroup_DDD_L_D")
                    if isFirstGroup:
                        isFirstGroup = False
                    else:
                        # while True:
                        #     divGroup = driver.find_element_by_id("MainContent_cbGroup_DDD_PW-1")
                        #     if "visibility: visible" in divGroup.get_attribute("style"):
                        #         break
                        driver.execute_script(
                            "$('#MainContent_cbGroup_DDD_L_D').animate({scrollTop: '"+str(numberPixelGroup)+"px'})")

                    nameGroup = groupItemTD.get_attribute("innerHTML")
                    try:
                        WebDriverWait(driver, 0.5).until(
                            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#MainCtent_gvStudents_DXTitle td"),
                                                             nameGroup)
                        )
                    except:
                        driver.execute_script(
                            "$('#MainContent_cbGroup_DDD_L_D').animate({scrollTop: '"+str(numberPixelGroup)+"px'})")
                    numberPixelGroup += 22
                    print "Click : ", groupItemTD.get_attribute("innerHTML")
                    groupItemTD.click()
                    print "nameGroup = {0}".format(nameGroup)
                    # wait until title is updated
                    while True:
                        try:
                            isHasTitle = WebDriverWait(driver, 30).until(
                                EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#MainContent_gvStudents_DXTitle td"),
                                                             nameGroup)
                            )
                        except:
                            # cmbGroup.click()
                            # groupItemTD.click()
                            break
                        # divTitle = driver.find_element_by_id("MainContent_gvStudents_DXTitle")
                        # title = divTitle.find_element_by_tag_name("td")
                        # if nameGroup in title.get_attribute("innerHTML"):
                        #     break
                        if isHasTitle:
                            break

                    # get list student
                    listStudent = []
                    # get student in page
                    # click btn One
                    try:
                        divBottom = driver.find_element_by_id("MainContent_gvStudents_DXPagerBottom")

                        isDivBottomExist = True
                    except NoSuchElementException:
                        isDivBottomExist = False

                    if isDivBottomExist:
                        listNumberPage = divBottom.find_elements_by_class_name("dxp-num")
                        onePage = listNumberPage[0]
                        print onePage.get_attribute("innerHTML")
                        onePage.click()
                    numberStudent = 0

                    # loop through all student in all page
                    while True:

                        tblStudent = WebDriverWait(driver, 60).until(
                            EC.presence_of_element_located((By.ID, "MainContent_gvStudents_DXMainTable"))
                        )

                        # wait until first row in next page is loaded
                        print "first row = ", numberStudent
                        try:
                            WebDriverWait(driver, 60).until(
                                EC.presence_of_element_located((By.ID, "MainContent_gvStudents_DXDataRow" + str(numberStudent)))
                            )
                        except:
                            print "Khong tim thay row {}".format(numberStudent)
                        numberStudent += 30
                        listStudentTR = []
                        # tblStudent = driver.find_element_by_id("MainContent_gvStudents_DXMainTable")
                        # listStudentTR = tblStudent.find_elements_by_css_selector("tr.dxgvDataRow_SisTheme")
                        try:
                            listStudentTR = WebDriverWait(driver, 60).until(
                                EC.presence_of_all_elements_located(
                                    (By.CSS_SELECTOR, "#MainContent_gvStudents_DXMainTable tr.dxgvDataRow_SisTheme"))
                            )
                        except:
                            print "{} khong co sinh vien".format(nameGroup)
                        # listStudentTR = listStudentTR[1::]
                        print "Len = ", len(listStudentTR)
                        # loop through one page
                        isFirstStudentTR = True
                        for studentTR in listStudentTR:
                            # if isFirstStudentTR:
                            #     isFirstStudentTR = False
                            #     continue
                            listTD = studentTR.find_elements_by_tag_name("td")
                            # print "len listTD = ", len(listTD)
                            listInfoStudent = []
                            # info one student
                            for td in listTD:
                                listInfoStudent.append(td.get_attribute("innerHTML"))
                            listInfoStudent.append(nameGroup)
                            listInfoStudent.append(nameFaculty)
                            listInfoStudent.append(nameCourse)
                            listInfoStudent = tuple(listInfoStudent)
                            print "1SV = ", listInfoStudent
                            f.write("\n")
                            f.write(",".join(listInfoStudent))
                            print ",".join(listInfoStudent)
                            # listStudent.append((listInfoStudent))
                            numStudentPerCourse += 1

                        # check btn next exist
                        isDivBottomExist = False
                        try:
                            divBottom = driver.find_element_by_id("MainContent_gvStudents_DXPagerBottom")
                            isDivBottomExist = True
                        except NoSuchElementException:
                            isDivBottomExist = False

                        if isDivBottomExist:
                            # loop until btn next is disabled click
                            listBtn = divBottom.find_elements_by_css_selector(".dxp-button")
                            btnNext = listBtn[-1]
                            # check disbaled button
                            if "dxp-disabledButton" in btnNext.get_attribute("class"):
                                break
                            btnNext.click()
                        else:
                            break

                    dictGroup.update({nameGroup: listStudent})
                    print "course {0} - faculty {1} - group {2} - numStudent = {3}" \
                        .format(nameCourse, nameFaculty, nameGroup, len(listStudent))
                    # print listStudent
                    # break
                # dictFaculty.update({nameFaculty: dictGroup})
                # break
            # dictCourse.update({nameCourse: dictFaculty})
            print "Course {0} has {1} students".format(nameCourse, numStudentPerCourse)
            # break

    os.system("taskkill /f /im geckodriver.exe")
