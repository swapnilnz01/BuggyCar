import pytest
from frameworkUtility.framework import frameworkClass


@pytest.fixture(scope="session")
def initializeTest1(self):
    f = frameworkClass()
    f.testSetUp()
    return f
    # yield f.driver
    # f.driver.quit()
