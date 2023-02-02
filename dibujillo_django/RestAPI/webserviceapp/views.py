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

	try:
		peticion = json.loads(request.body)
	except json.decoder.JSONDecodeError:
		return JsonResponse({'error':'JSON invalido'}, status=400)

	if not all(k in peticion for k in("name")):
		return JsonResponse({'error':'Faltan parametros'}, status=400)

	invitado = Usuario()
	nomInvitado = peticion['name']
	invitado2 = Usuario.objects.filter(nombre = nomInvitado)
	print(invitado2)
	if (nomInvitado != invitado2[0]):
		invitado.nombre = nomInvitado
		payload = {
			'username':invitado.nombre
		}
		secret = 'muysecreto'
		token = jwt.encode(payload, secret, algorithm='HS256')
		invitado.token = token
		invitado.save()
		return JsonResponse({"sessionToken":token},status=200)
	else:
		return JsonResponse({'error':'Nombre ya existe'}, status=400)


