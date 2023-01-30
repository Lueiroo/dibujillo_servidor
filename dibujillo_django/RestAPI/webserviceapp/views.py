from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario

import json
import jwt

# Create your views here.

@csrf_exempt
def invitado(request):
	if request.method != 'POST':
		return None

	json_peticion = json.loads(request.body)
	invitado = Usuario()
	invitado.nombre = json_peticion['name']

	if invitado.nombre == '':
		return HttpResponse("Faltan parámetros",status=400)

	payload = {
		'username':invitado.nombre
	}
	secret = 'muysecreto'
	token = jwt.encode(payload, secret, algorithm='HS256')

	invitado.token = token
	invitado.save()

	return JsonResponse({"sessionToken":token},status=200)


