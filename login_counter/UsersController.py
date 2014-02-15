from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
import login_counter
import json
import os
import tempfile
import traceback
import re

# Create your views here.

""" UsersController """
@csrf_exempt
def do_POST(request):
    ##import pdb; pdb.set_trace()
    try:
        if request.path == "/users/login" or request.path == "/users/add":
            data = json.loads(request.body);
            username = data.get("user")
            password = data.get("password");

            if (username == None and password == None):
                return;
            UsersModel = login_counter.models.UsersModel();
            if request.path == "/users/login":
                rval = UsersModel.login(username, password)
            else:
                rval = UsersModel.add(username, password)

            if (rval < 0):
                resp = {"errCode" : rval};
            else:
                resp = {"errCode" : UsersModel.SUCCESS, "count" : rval}

            response = HttpResponse(json.dumps(resp), status=200, content_type="application/json");
            return response;

        else:
            return HttpResponse("Unrecognized request", status=404);
    except:
        return HttpResponse("Catastrophic Error in UsersController!", status=500);

