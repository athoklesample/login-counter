from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
import json
import login_counter
import os
import tempfile
import traceback
import re
#import pdb; pdb.set_trace()

# Create your views here.

""" TESTAPI_Controller """
@csrf_exempt
def do_POST(request):
        try:
            if (request.path == "/TESTAPI/resetFixture"):
                UsersModel = login_counter.models.UsersModel();
                UsersModel.TESTAPI_resetFixture();
                response = HttpResponse(json.dumps({"errCode" : UsersModel.SUCCESS}), status=200, content_type="application/json");
                return response;

            elif (request.path == "/TESTAPI/unitTests"):
                import pdb; pdb.set_trace()
                 # We run the unit tests and collect the output into a temporary file
                # Conveniently, we have a Makefile target for all unit_tests
                # There are better ways of doing this in Python, but this is a more portable example
                ##thisDir = os.path.dirname(os.path.abspath(__file__))
                (ofile, ofileName) = tempfile.mkstemp(prefix="userCounter")
                os.close(ofile)
##                ofileName = os.path.join(thisDir,"userCounter");
##                open(ofileName,"w").close();
                try:
                    errMsg = ""     # We accumulate here error messages
                    output = ""     # Some default values
                    totalTests = 0
                    nrFailed   = 0
                    while True:  # Give us a way to break
                        # Find the path to the server installation
                        thisDir = os.path.dirname(os.path.abspath(__file__))
                        cmd = "nmake -C "+thisDir+" unit_tests >"+ofileName+" 2>&1"
                        Utils.log("Executing "+cmd)
                        code = os.system(cmd)
                        if code != 0:
                            # There was some error running the tests.
                            # This happens even if we just have some failing tests
                            errMsg = "Error running command (code="+str(code)+"): "+cmd+"\n"
                            # Continue to get the output, and to parse it

                        # Now get the output
                        try:
                            ofileFile = open(ofileName, "r")
                            output = ofileFile.read()
                            ofileFile.close ()
                        except:
                            errMsg += "Error reading the output "+traceback.format_exc()
                            # No point in continuing
                            break

                        Utils.log("Got "+output)
                        # Python unittest prints a line like the following line at the end
                        # Ran 4 tests in 0.001s
                        m = re.search(r'Ran (\d+) tests', output)
                        if not m:
                            errMsg += "Cannot extract the number of tests\n"
                            break
                        totalTests = int(m.group(1))
                        # If there are failures, we will see a line like the following
                        # FAILED (failures=1)
                        m = re.search('rFAILED.*\(failures=(\d+)\)', output)
                        if m:
                            nrFailures = int(m.group(1))
                        break # Exit while

                    # End while
                    if errMsg:
                        Utils.log(errMsg, err=True)

                    resp = { 'output' : errMsg + output,
                         'totalTests' : totalTests,
                         'nrFailed' : nrFailed }

                    response = HttpResponse(json.dumps(resp), status=200, content_type="application/json");
                    return response;

                finally:
                    os.unlink(ofileName)
            else:
                return HttpResponse("Unrecognized request", status=404);
        except:
            return HttpResponse("Catastrophic Error in TESTAPI_Controller!", status=500);



class Utils:
    """
    Utility functions
    """

    @staticmethod
    def log(msg, err=False):
        """
        Logging function
        """
        if err:
            msg = "ERROR: "+msg
        print msg
