from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from login_counter.models import *
import os
import tempfile
import traceback
import re
#import pdb; pdb.set_trace()

# Create your views here.
def index(request):
    return render_to_response('client.html')


