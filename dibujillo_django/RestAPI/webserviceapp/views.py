from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario, Partida

import json
import jwt
import random
import timedelta

# Create your views here.

#3. guest
@csrf_exempt
def invitado(request):
	if request.method != 'POST':
		return None

	try:
		peticion = json.loads(request.body)
	except json.decoder.JSONDecodeError:
		return JsonResponse({'error':'JSON invalido'}, status=400)

	invitado = Usuario()
	nomInvitado = peticion['name']

	if (nomInvitado == ""):
		return JsonResponse({'error':'Faltan parametros'}, status=400)

	invitado2 = Usuario.objects.filter(nombre = nomInvitado).exists()

	if (invitado2 is False):
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

#6. game/cod/historia
@csrf_exempt
def historia(request, cod):
	if request.method != 'GET':
		return None

	token = request.headers.get('sessionToken')
	tokenBD = Usuario.objects.filter(token = token).exists()

	if not token or tokenBD is False:
		return JsonResponse({'error': 'Invalid token'}, status=400)

	try:
		partida = Partida.objects.get(codigo = cod)
	except:
		return JsonResponse({'error': 'Codigo no existe'}, status=404)

	listaFrases = ["Perro sobre un caballo", "Un pato cocinado unos filetes de pollo", "Un dragon jugando al ajedrez con un humano"]
	frase = random.choice(listaFrases)

	time = partida.createdat + timedelta(minutes=2)
	print(time)

	partida.historia = frase
	partida.save()

	return JsonResponse({'history': frase, 'startTime': partida.createdat}, status = 200)
