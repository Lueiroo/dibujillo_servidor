from django.shortcuts import render
from django.http import HttpResponse
import jason
from .models import *


# Create your views here.

def registrarUsuario(request):
	if request.method != 'POST':
		return None

	json_peticion = json.loads(request.body)

