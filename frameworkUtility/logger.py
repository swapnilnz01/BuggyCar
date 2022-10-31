import sys
import warnings

import verify as verify

class logger:

    def logMessage(srtMessage, isPassFail, hault):
        warnings.simplefilter(action='ignore', category=FutureWarning)
        warnings.simplefilter(action='ignore', category=ResourceWarning)

        if isPassFail is True:
            verify.is_true
            print("[PASS] {0}".format(srtMessage))

        elif isPassFail == "INFO":
            print("[INFO] {0}".format(srtMessage))

        elif isPassFail is False:
            verify.is_false
            print("[FAIL] {0}".format(srtMessage))
            sys.exit()
