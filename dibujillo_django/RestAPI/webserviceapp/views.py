from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario, Partida, Participa, Dibujo, Comentario
from django.contrib.auth.hashers import check_password

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
		return JsonResponse({'error': 'JSON invalido'}, status=400)

	invitado = Usuario()
	nomInvitado = peticion['name']

	if (nomInvitado == ""):
		return JsonResponse({'error': 'Faltan parametros'}, status=400)

	invitado2 = Usuario.objects.filter(nombre=nomInvitado).exists()

	if (invitado2 is False):
		invitado.nombre = nomInvitado
		payload = {
			'username': invitado.nombre
		}
		secret = 'muysecreto'
		token = jwt.encode(payload, secret, algorithm='HS256')
		invitado.token = token
		invitado.save()
		return JsonResponse({"sessionToken": token}, status=201)
	else:
		return JsonResponse({'error': 'Nombre ya existe'}, status=400)


@csrf_exempt
def login(request):
	if request.method != 'POST':
		return None

	try:
		peticion = json.loads(request.body)
	except json.decoder.JSONDecodeError:
		return JsonResponse({'error': 'JSON invalido'}, status=400)

	usuario = Usuario()
	nameOrEmail = peticion['nameOrEmail']
	password = peticion['password']
	usuario.set_password(password)

	if (nameOrEmail == ''):
		return JsonResponse({'error': 'Faltan parámetros'}, status=400)

	name1 = Usuario.objects.filter(nombre=nameOrEmail).exists()
	email1 = Usuario.objects.filter(email=nameOrEmail).exists()

	if (name1 is True):
		usuario2 = Usuario.objects.get(nombre=nameOrEmail)
		pass
	elif (email1 is True):
		usuario2 = Usuario.objects.get(email=nameOrEmail)
		pass
	else:
		return JsonResponse({'error': 'El susuario no existe'}, status=400)

	if check_password(password, usuario2.contraseña):
		secret = 'muysecreto'
		token = jwt.encode(payload, secret, algorithm='HS256')
		usuario.token = token
		usuario.save()
		return JsonResponse({"sessionToken": token}, status=200)
	else:
		return JsonResponse({'error': 'La contraseña es incorrecta'}, status=401)


@csrf_exempt
def join_game(request, cod):
    if request.method != 'POST':
        return None

    try:
       session_token = request.headers.get('sessionToken')
    except Exception:
        return JsonResponse({'error': 'SessionToken does no exist'}, status=401)
    try:
        user = Usuario.objects.get(token=session_token)
    except Usuario.DoesNotExist:
        return JsonResponse({'error': 'Invalid token'}, status=401)

    print(cod)
    if not cod:
        return JsonResponse({'error': 'Code does not exist'}, status=400)

    partida = Partida.objects.all()
    for p in partida:
        print(p.codigo)

    try:
        game = Partida.objects.get(codigo=cod)
    except Partida.DoesNotExist:
        return JsonResponse({'error': 'Code does not exist'}, status=404)

    Participa.objects.create(token_usuario=user, codigo_partida=game)

    return JsonResponse({
        'code': game.codigo,
        'players': [p.token_usuario.nombre for p in game.participa_set.all()],
        'createdAt': game.createdat,
    }, status=200)


def get_drawing(request, cod, name):
    if request.method != 'GET':
        return None

    try:
        partida = Partida.objects.get(codigo=cod)
    except Partida.DoesNotExist:
        print("Partida no existe")
        return HttpResponse(status=404)
    
    try:
        usuario = Usuario.objects.get(nombre=name)
    except Usuario.DoesNotExist:
        return HttpResponse(status=401)
    
    try:
        participa = Participa.objects.get(token_usuario=usuario.token, codigo_partida=partida.codigo)
    except Participa.DoesNotExist:
        return HttpResponse(status=401)
    
    try:
        dibujo = Dibujo.objects.get(token_usuario=usuario.token, codigo_partida=partida.codigo)
    except Dibujo.DoesNotExist:
        print("Dibujo no existe")
        return HttpResponse(status=404)
    
    response_data = {
        'path': dibujo.link
    }
    return JsonResponse(response_data)

@csrf_exempt 
def share_drawing(request, cod):
    if request.method != 'POST':
          return None
    
    session_token = request.headers.get('SessionToken', None)
    if not session_token:
        return JsonResponse({'error': 'Token inválido'}, status=401)

    try:
        partida = Partida.objects.get(codigo=cod)
    except Partida.DoesNotExist:
        return JsonResponse({'error': 'Código no existe'}, status=404)

    try:
        dibujo = Dibujo.objects.get(codigo_partida=partida, token_usuario=session_token)
    except Dibujo.DoesNotExist:
        return JsonResponse({'error': 'No se puede compartir el dibujo'}, status=400)

    return JsonResponse({'path': dibujo.link, 'uploadAt': dibujo.fecha}, status=200)


def profile(request, name):
	if request.method != 'GET':
		return None

	session_token = request.headers.get('SessionToken', None)
	if not session_token:
		return JsonResponse({'error': 'Token inválido'}, status=401)

	try:
		usuario = Usuario.objects.get(nombre=name)
	except Usuario.DoesNotExist:
		return JsonResponse({'error': 'Usuario no existe'}, status=404)

	try:
		participa = Participa.objects.get(token_usuario=usuario.token)
	except Participa.DoesNotExist:
		return JsonResponse({'error': 'No se puede obtener el perfil'}, status=400)
        
	try:
		dibujo = Dibujo.objects.get(token_usuario=usuario.token)
	except Dibujo.DoesNotExist:
		return JsonResponse({'error': 'No se puede obtener el perfil'}, status=400)
	
	try:
		comentario = Comentario.objects.get(token_usuario=usuario.token)
	except Comentario.DoesNotExist:
		return JsonResponse({'error': 'No se puede obtener el perfil'}, status=400)

	response_data = {
		'drawings': [{
              'path': dibujo.link,
              'uploadAt': dibujo.fecha,
              'comments':[{
				  'user': usuario.nombre,
				  'comment': comentario.comentario,
			}]
		}],
	}
	return JsonResponse(response_data)
