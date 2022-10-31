from telnetlib import EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from frameworkUtility.logger import logger


class GenericComponents:
    f = None

    def __init__(self, fobject):
        self.f = fobject

    def resetHome(self):
        self.clickLink("icn_HomePage")

    def clickLink(self, strFieldName):
        try:
            strXpath = self.f.getObjectName(strFieldName)
            self.explicitWaitForElement(strXpath, 10)
            self.f.driver.find_element("xpath", strXpath).click()
            logger.logMessage("{0} - Field clicked".format(strFieldName), True,
                              "SOFT")
        except:
            logger.logMessage("{0} - Field not clicked".format(strFieldName), False,
                              "SOFT")

    def clickLinkXpath(self, strXpath, LinkName):
        try:
            self.explicitWaitForElement(strXpath, 10)
            self.f.driver.find_element("xpath", strXpath).click()
            logger.logMessage("{0} - Field clicked".format(LinkName), True,
                              "SOFT")
        except:
            logger.logMessage("{0} - Field not clicked".format(LinkName), False,
                              "SOFT")

    def clickButton(self, strFieldName):
        try:
            strXpath = self.f.getObjectName(strFieldName)
            self.explicitWaitForElement(strXpath, 10)
            self.f.driver.find_element("xpath", strXpath).click()
            logger.logMessage("{0} - Field clicked".format(strFieldName), True,
                              "SOFT")
        except:
            logger.logMessage("{0} - Field not clicked".format(strFieldName), False,
                              "SOFT")

    def enterText(self, strFieldName, text):
        try:
            strXpath = self.f.getObjectName(strFieldName)
            self.explicitWaitForElement(strXpath, 10)
            self.f.driver.find_element("xpath", strXpath).send_keys(text)
            logger.logMessage("{0} - Entered value in field".format(text), True,
                              "SOFT")
        except:
            logger.logMessage("{0} - Enter value in field".format(text), False,
                              "SOFT")

    def verifyElementExistance(self, strFieldName):
        try:
            strXpath = self.f.getObjectName(strFieldName)
            self.explicitWaitForElement(strXpath, 10)
            ele = self.f.driver.find_elements("xpath", strXpath)
            if len(ele) > 0:
                logger.logMessage("{0} - Element present".format(strFieldName), True,
                                  "SOFT")
            return True
        except:
            logger.logMessage("{0} - Element not present".format(strFieldName), False,
                              "SOFT")

    def verifyElementNotExistance(self, strFieldName):
        try:
            strXpath = self.f.getObjectName(strFieldName)
            # self.explicitWaitForElement(strXpath, 10)
            ele = self.f.driver.find_elements("xpath", strXpath)
            if len(ele) == 0:
                logger.logMessage("{0} - Element not present".format(strFieldName), True,
                                  "SOFT")
        except:
            logger.logMessage("{0} - Element present".format(strFieldName), False,
                              "SOFT")

    def verifyExpectedVsActual(self,strMessage, expectedValue, actualValue):
        try:
            if (expectedValue == actualValue):
                logger.logMessage("{0} -> Expected - {1} || Actual - {2}".format(strMessage,expectedValue, actualValue), True, "SOFT")
        except:
                logger.logMessage("{0} -> Expected - {1} || Actual - {2}".format(strMessage,expectedValue, actualValue), False, "SOFT")

    def explicitWaitForElement(self, xpath, time):
        try:
            myElem = WebDriverWait(self.f.driver, time).until(EC.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutError:
            logger.logMessage("Too Long to load the field - {0}".format(xpath),False,"Soft")

    def applicationLogin(self, strUsername, strPassword):
        try:
            self.enterText("input_UserName",strUsername)
            self.enterText("input_Password",strPassword)
            self.clickButton("btn_Login")
            logger.logMessage("Logged in As - {0}".format(strUsername), True,
                              "SOFT")
        except:
            logger.logMessage("Login of user failed - {0}".format(strUsername), False,
                              "SOFT")

    def registerApplication(self, strUsername, strFname, strLname, strPassword ):
        try:
            self.enterText("input_Register_UserName", strUsername)
            self.enterText("input_Register_FirstName", strFname)
            self.enterText("input_Register_LastName", strLname)
            self.enterText("input_Register_Password", strPassword)
            self.enterText("input_Register_Cpassword", strPassword)
            self.clickButton("btn_Register_Register")
            if self.verifyElementExistance("txt_Register_Confirmation"):
                logger.logMessage("Registered successfully in As - {0}".format(strUsername), True,
                              "SOFT")
        except:
            logger.logMessage("Registration of user failed - {0}".format(strUsername), False,
                              "SOFT")

    def addComment(self, strCartype, strCarName, strComment):
        try:
            #  Need to comment the below section due to a Defect - Home page not working
            # xpath = self.f.getObjectName("generic_CarType")
            # xpath_CarType = str.replace(xpath,"REPLACE",strCartype)
            # self.clickLinkXpath(xpath_CarType, "Car Name")

            xpath = self.f.getObjectName("generic_CarName")
            xpath_CarName = str.replace(xpath,"REPLACE",strCarName)
            self.clickLinkXpath(xpath_CarName, "Car Name")

            if self.verifyElementNotExistance("lbl_VoteConfirmation"):
                logger.logMessage("User Has already voted for this Car", True,
                                  "SOFT")
            else:
                self.enterText("txt_Comment", strComment)
                self.clickButton("txt_Vote")
                if self.verifyElementExistance("lbl_VoteConfirmation"):
                    logger.logMessage("Vote successfully  - {0}".format(strComment), True,
                                  "SOFT")
        except:
            logger.logMessage("Voting failed - {0}".format(strComment), False,
                              "SOFT")

    def getCellNumberFromText(self,xpath, text):
        #Verify the table
        self.explicitWaitForElement(xpath, 10)
        row_no = len(self.f.driver.find_elements("xpath",xpath + "/tr"))
        col_no = len(self.f.driver.find_elements("xpath",xpath + "/tr[1]/td"))

        for row in range(1,row_no + 1):
            for col in range(2, (col_no + 1)):
                webelement = self.f.driver.find_elements("xpath", "{0}/tr[{1}]/td[{2}]".format(xpath,row,col))
                rowText = webelement[0].text

                if rowText == text:
                    return row
                    break

    def logout(self,strFieldName):
        try:
            strXpath = self.f.getObjectName(strFieldName)
            self.explicitWaitForElement(strXpath, 10)
            self.f.driver.find_element("xpath", strXpath).click()
            logger.logMessage("LogOut successful", True,
                              "SOFT")
        except:
            logger.logMessage("LogOut successful", False,
                              "SOFT")

    # def getExitingVoteForBuggy(self, carType,carName):
        # self.clickLinkXpath(str.replace(self.f.getObjectName("generic_CarType"), "REPLACE", carType),
        #                   "Car Type")
        #
        # self.clickLinkXpath(str.replace(self.f.getObjectName("generic_CarName"), "REPLACE", carName),
        #                   "Car Name")
        #
        # # Below lines will read the Existing vote counts which would be used in further verifications
        # xpath = self.f.getObjectName("lbl_getVotes")
        # self.explicitWaitForElement(xpath, 10)
        # cnt_initial_vote = self.f.driver.find_element("xpath", xpath).text
        # logger.logMessage("Initial Vote count = " + cnt_initial_vote, "INFO", "Soft")
        # # Initialize the Application page to Home page
        # self.resetHome()
        # return cnt_initial_vote

# ==================

    def getExitingValuesForBuggy(self, carType, carName):

        # Get column values from the properties
        col_Vote = self.f.getProperty("TABLEHEADERS", "RatingVotes")
        col_Comment = self.f.getProperty("TABLEHEADERS", "RatingComments")

        self.clickLinkXpath(str.replace(self.f.getObjectName("generic_CarType"), "REPLACE", carType),
                          "Car Type")

        # Get row number for which the values were updated - RUNTIME
        rowNumber = self.getCellNumberFromText(self.f.getObjectName("tbl_raiting"),
                                             carName)
        xpathTable = self.f.getObjectName("tbl_raiting")
        voteCount = self.f.driver.find_element("xpath",
                                                 "{0}/tr[{1}]/td[{2}]".format(xpathTable, rowNumber, col_Vote)).text

        comment = self.f.driver.find_element("xpath",
                                                 "{0}/tr[{1}]/td[{2}]/div[1]".format(xpathTable, rowNumber, col_Comment)).text

        # Initialize the Application page to Home page
        return voteCount, comment

    def getExitingValuesForBuggy_OverAllRaiting(self, overall, carName):

        # Get column values from the properties
        col_Vote = self.f.getProperty("TABLEHEADERS", "OverAllRatingVotes")
        col_Comment = self.f.getProperty("TABLEHEADERS", "OverAllRatingComments")

        self.clickLinkXpath(str.replace(self.f.getObjectName("generic_CarType"), "REPLACE", overall),
                          "Car Type")

        # Get row number for which the values were updated - RUNTIME
        rowNumber = self.getCellNumberFromText(self.f.getObjectName("tbl_raiting"),
                                             carName)
        xpathTable = self.f.getObjectName("tbl_raiting")
        voteCount = self.f.driver.find_element("xpath",
                                                 "{0}/tr[{1}]/td[{2}]".format(xpathTable, rowNumber, col_Vote)).text

        comment = self.f.driver.find_element("xpath",
                                                 "{0}/tr[{1}]/td[{2}]/div[1]".format(xpathTable, rowNumber, col_Comment)).text

        # Initialize the Application page to Home page
        return voteCount, comment
