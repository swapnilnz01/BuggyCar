import os.path
import xlrd
from frameworkUtility.logger import logger
from configparser import RawConfigParser
from selenium import webdriver

class frameworkClass():
    driver = None

    def testSetUp(self):
        try:
            logger.logMessage("Initalizing Framework", "INFO", "SOFT")
            self.readConfig()
            self.initBrowser()
        except:
            logger.logMessage("Initalizing Framework", False, "SOFT")

    def readConfig(self):
        strFileName = "{0}".format(os.path.abspath("..\\config.ini"))
        self.prop = RawConfigParser()
        self.prop.read(strFileName)

    def initBrowser(self):
        strPath = "{0}".format(os.path.abspath("..\\resouces"))
        if (self.getProperty("DEFAULT", "Browser")) == "Chrome":
            self.driver = webdriver.Chrome(executable_path="{0}{1}".format(strPath, "\\chromedriver"))
        # elif (self.getProperty("DEFAULT", "Browser")) == "IE":

        self.driver.maximize_window()

    def getProperty(self, sectionHeader, propertyKey):
        setValue = ""
        try:
            setValue = self.prop.get(sectionHeader, propertyKey)
            return setValue
            logger.logMessage("Value from - {0} is retrieved as - {1}".format(sectionHeader, propertyKey), "INFO",
                              "SOFT")

        except:
            logger.logMessage("Value from - {0} is not retrieved as - {1}".format(sectionHeader, propertyKey), "INFO",
                              "SOFT")

    def getObjectName(self, strFieldName):
        try:
            xpath = ""
            col = 0
            strPath = "{0}".format(os.path.abspath("..\\objectRepository"))
            # strFileName = "ObjectRepository.xls"
            strFileName = self.getProperty("DEFAULT", "ObjectRepo")
            strWorkSheetName = "OR"
            workBook = xlrd.open_workbook(strPath + "\\" + strFileName)
            workSheet = workBook.sheet_by_name(strWorkSheetName)

            for i, cell in enumerate(workSheet.col(0)):
                if cell.value == strFieldName:
                    rowNumber = i
                    break

            xpath = workSheet.cell(rowNumber,1)
            return xpath.value
        except:
            logger.logMessage("{0} - field is not present in the Object repository".format(strFieldName), False,
                              "SOFT")

    def getTestDataDict(self, strTestCaseId, dataSheet):
        try:
            testData = {}
            col = 0
            strPath = "{0}".format(os.path.abspath("..\\data"))
            strFileName = "testdata.xls"
            workBook = xlrd.open_workbook(strPath + "\\" + strFileName)
            workSheet = workBook.sheet_by_name(dataSheet)

            for i, cell in enumerate(workSheet.col(0)):
                if cell.value == strTestCaseId:
                    rowNumber = i
                    break

            while col < workSheet.ncols:
                key = workSheet.cell(0,col).value
                value = workSheet.cell(rowNumber,col).value
                testData[key] = value
                col+=1
            logger.logMessage("{0} - Data found in Datasheet".format(testData), True,
                              "SOFT")
            return testData
        except:
            logger.logMessage("{0} - Data not found in Datasheet".format(strTestCaseId), False,
                              "SOFT")