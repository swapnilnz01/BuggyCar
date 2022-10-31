import pytest
from frameworkUtility.framework import frameworkClass
from reusableFiles.reusableFunctions import GenericComponents
from frameworkUtility.logger import logger
import random

class Test:

    # This is a Fixture in Python. Use this for Setting up the test. This will execute everytime the test runs
    @pytest.fixture(scope="function")
    def initializeTest(self):
        f = frameworkClass()
        f.testSetUp()
        return f

    @pytest.mark.parametrize("testCaseName", ["E2E2"
                                              # "E2E3",
                                              # "E2E4",
                                              # "E2E5"
                                              ])
    def test_E2E(self, initializeTest, testCaseName):
        # Initializing the test
        try:
            f = initializeTest
            gc = GenericComponents(f)

            # This function will read the test data from excel and create a dictionary object
            testData = f.getTestDataDict(testCaseName, "TestData")
            uniqueNumber = random.randint(999, 99999)

            # Opening the application URL
            f.driver.get(f.getProperty("DEFAULT", "buggyLoginURL"))
            # Wait for the page to load
            gc.explicitWaitForElement(f.getObjectName("icn_HomePage"), 10)

            # Register User
            logger.logMessage("==========Register==========", "INFO", "Soft")
            gc.clickButton("btn_Register")
            gc.registerApplication(testData["UserName"] + str(uniqueNumber),
                                   testData["Fname"],
                                   testData["Lname"],
                                   testData["Password"])

            # Login Application
            logger.logMessage("==========Login==========", "INFO", "Soft")
            gc.applicationLogin(testData["UserName"] + str(uniqueNumber),
                                testData["Password"])

            # Initialize the Application page to Home page
            gc.resetHome()

            # Add Comment and verify the review to a Buggy Car
            logger.logMessage("==========Note Initial Values before updating the comments==========", "INFO", "Soft")

            # This is the generic code written which can be used for any car type and car name.
            # To execute the script for multiple cars just update CarName and CarType in datasheet
            cnt_initial_vote, initial_comment = gc.getExitingValuesForBuggy(testData["CarType"],
                                                                            testData["CarName"])
            logger.logMessage(" Vote count = " + cnt_initial_vote, "INFO", "Soft")

            #This function will go to the CarType and CarMake and put in the vote and comment
            logger.logMessage("==========Adding Comment==========", "INFO", "Soft")
            gc.addComment(testData["CarType"],
                          testData["CarName"],
                          testData["Comments"])

            # Initialize the Application page to Home page
            gc.resetHome()

            # Get column values from the properties
            cnt_updated_vote, added_comment = gc.getExitingValuesForBuggy(testData["CarType"],
                                                                            testData["CarName"])
            # The Vote count should be updated by 1.
            #  Using a function to verify the results
            logger.logMessage("==========Final Verification #1 Popular Make==========", "INFO", "Soft")
            gc.verifyExpectedVsActual("Vote has been updated",
                                      int(str.strip(cnt_initial_vote))+1,
                                      int(cnt_updated_vote))

            gc.verifyExpectedVsActual("Comments has been updated",
                                      str.strip(added_comment),
                                      testData["Comments"])

            # Initialize the Application page to Home page
            gc.resetHome()

            # Validate the Values on Overall Raiting
            logger.logMessage("==========Final Verification #2 Overall Raiting==========", "INFO", "Soft")
            f.driver.get(f.getProperty("DEFAULT", "buggyLoginURL"))
            cnt_overall_vote, added_overall_comment = gc.getExitingValuesForBuggy_OverAllRaiting("overall",
                                                                                        testData["CarName"])
            gc.verifyExpectedVsActual("Vote has been updated",
                                      int(str.strip(cnt_initial_vote))+1,
                                      int(cnt_overall_vote))

            gc.verifyExpectedVsActual("Comments has been updated",
                                      str.strip(added_overall_comment),
                                      testData["Comments"])

            # Initialize the Application page to Home page
            gc.resetHome()

        except:
            logger.logMessage("{0} - Test case Failed".format(testCaseName), False,
                              "SOFT")
        finally:
            gc.logout("btn_Logout")
            # gc.teardown()