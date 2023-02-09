from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario, Partida, Dibujo, Valora, Comentario, Participa
from datetime import timedelta

import json
import jwt
import random

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
	nomInvitado = peticion['username']

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
		return JsonResponse({"sessionToken":token},status=201)
	else:
		return JsonResponse({'error':'Nombre ya existe'}, status=400)

#6. game/cod/historia ()
@csrf_exempt
def historia(request, cod):
	if request.method != 'GET':
		return None

	token = request.headers.get('sessionToken')
	tokenBD = Usuario.objects.filter(token = token).exists()

	if not token or tokenBD is False:
		return JsonResponse({'error': 'Invalid token'}, status=401)

	try:
		partida = Partida.objects.get(codigo = cod)
	except:
		return JsonResponse({'error': 'Codigo no existe'}, status=404)

	listaFrases = ["Perro sobre un caballo", "Un pato cocinado unos filetes de pollo", "Un dragon jugando al ajedrez con un humano"]
	frase = random.choice(listaFrases)

	time = partida.createdat + timedelta(minutes=2)

	partida.historia = frase
	partida.save()

	return JsonResponse({'history': frase, 'startTime': time}, status = 200)

#5b. game/cod ()
@csrf_exempt
def datosSala(request, cod):
	if request.method != 'GET':
		return None

	token = request.headers.get('sessionToken')
	tokenBD = Usuario.objects.filter(token = token).exists()

	if not token or tokenBD is False:
		return JsonResponse({'error': 'Invalid token'}, status=401)

	try:
		partida = Partida.objects.get(codigo = cod)
	except:
		return JsonResponse({'error':'Codigo no existe'})

	participantes = Participa.objects.filter(codigo_partida = cod).values()
	usuarios = []
	for participante in participantes:
		usuario = Usuario.objects.filter(token = participante['token_usuario_id']).values();
		usuarios.append(usuario[0]['nombre'])

	print(usuarios)
	resultado = {
		'code': cod,
		'players' : usuarios,
		'createdAt': partida.createdat
	}

	return JsonResponse(resultado, safe=False)

#9. game/cod/player/name/drawing/rating ()
@csrf_exempt
def puntuacion(request, cod, nom):
	if request.method != 'PUT':
		return None

	token = request.headers.get('sessionToken')
	tokenBD = Usuario.objects.filter(token = token).exists()

	if not token or tokenBD is False:
		return JsonResponse({'error': 'Invalid token'}, status=401)

	try:
		peticion = json.loads(request.body)
	except json.decoder.JSONDecodeError:
		return JsonResponse({'error':'JSON invalido'}, status=400)

	puntuacion = peticion['rating']
	if (puntuacion == ""):
		return JsonResponse({'error':'Faltan parametros'}, status=400)

	try:
		tokenDibujante = Usuario.objects.get(nombre = nom)
	except:
		return JsonResponse({'error':'Nombre no existe'}, status=404)

	try:
		dibujo = Dibujo.objects.get(codigo_partida = cod, token_usuario = tokenDibujante.token)
	except:
		return JsonResponse({'error':'Codigo no existe'}, status=404)

	valorar = Valora()

	valorar.token_usuario = tokenDibujante
	valorar.id_dibujo = dibujo
	valorar.puntuacion = puntuacion

	valorar.save()

	return JsonResponse({'state': 'OK'}, status = 200)

#12. drawings
@csrf_exempt
def dibujos(request):
	if request.method != 'GET':
		return None

	token = request.headers.get('sessionToken')
	tokenBD = Usuario.objects.filter(token = token).exists()

	if not token or tokenBD is False:
		return JsonResponse({'error': 'Invalid token'}, status=401)

	dibujosOrdenados = Dibujo.objects.all().order_by("fecha").values()

	respuesta = []
	for dibujo in dibujosOrdenados:
		diccionario = {}
		diccionario['id'] = dibujo['id']
		diccionario['path'] = dibujo['link']
		diccionario['UploadAt'] = dibujo['fecha']
		
		historia = Partida.objects.get(codigo = dibujo['codigo_partida_id'])
		diccionario['history'] = historia.historia

		nombreUsuario = Usuario.objects.get(token = dibujo['token_usuario_id'])
		diccionario['user'] = nombreUsuario.nombre
		diccionario['comments'] = []

		comentarios = Comentario.objects.all().filter(id_dibujo = dibujo['id']).values()

		respuesta.append(diccionario)
		for comentario in comentarios:
			diccionario2 = {}
			tokenUsuario = Usuario.objects.get(token = comentario['token_usuario_id'])
			nombre = Usuario.objects.get(token = tokenUsuario.token)
			diccionario2['user']  = nombre.nombre
			diccionario2['comment'] = comentario['comentario']
			diccionario['comments'].append(diccionario2)

	return JsonResponse(respuesta,safe=False)
