from django.shortcuts import render
from .models import Usuario
import json


# Create your views here.
@csrf_exempt 
def inicio_sesion(request):
	if request.method !=POST:
		return None
	
	json_peticion = json.loads(request.body)
	
