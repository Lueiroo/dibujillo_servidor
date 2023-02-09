import json
from .models import Usuario, Partida, Dibujo, Valora, Comentario, Participa
import jwt
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from json import JSONDecodeError
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario, Partida, Participa, Dibujo, Comentario
from django.contrib.auth.hashers import check_password
from django.utils import timezone

import json
import jwt

# Create your views here.



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
    print(session_token)

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
        print("Usuario no existe")
        return HttpResponse(status=401)

    try:
        participa = Participa.objects.get(
            token_usuario=usuario.token, codigo_partida=partida.codigo)
    except Participa.DoesNotExist:
        print("Participa no existe")
        return HttpResponse(status=401)

    try:
        dibujo = Dibujo.objects.get(
            token_usuario=usuario.token, codigo_partida=partida.codigo)
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

    session_token = request.headers.get('sessionToken')
    if not session_token:
        return JsonResponse({'error': 'Token inválido'}, status=401)

    try:
        partida = Partida.objects.get(codigo=cod)
    except Partida.DoesNotExist:
        return JsonResponse({'error': 'Código no existe'}, status=404)

    try:
        dibujo = Dibujo.objects.get(
            codigo_partida=partida, token_usuario=session_token)
    except Dibujo.DoesNotExist:
        return JsonResponse({'error': 'No se puede compartir el dibujo'}, status=400)

    dibujo.fecha = timezone.now()

    dibujo.save()

    return JsonResponse({'path': dibujo.link, 'uploadAt': dibujo.fecha}, status=200)


def profile(request, name):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    token = request.headers.get('SessionToken')
    user = Usuario.objects.filter(nombre=name).first()

    if not token or not name:
        return JsonResponse({'error': 'Invalid token or user not found'}, status=401)

    dibujosOrden = Dibujo.objects.filter(token_usuario=user).all().order_by("fecha").values()

    dibujos = []
    for dibujo in dibujosOrden:
        diccionario = {}
        diccionario['id'] = dibujo['id']
        diccionario['history'] = Partida.objects.get(codigo=dibujo['codigo_partida_id']).historia
        diccionario['path'] = dibujo['link']
        diccionario['UploadAt'] = dibujo['fecha']

        diccionario['comments'] = []
        comentarios = Comentario.objects.filter(id_dibujo=dibujo['id']).values()
        for comentario in comentarios:
            diccionario2 = {}
            diccionario2['user'] = Usuario.objects.get(token=comentario['token_usuario_id']).nombre
            diccionario2['comment'] = comentario['comentario']
            diccionario['comments'].append(diccionario2)

        dibujos.append(diccionario)

    return JsonResponse({'drawings': dibujos}, safe=False)



#Esta funciona
# 1. users
@csrf_exempt
def registrarUsuario(request):
    if request.method != 'POST':
        return None
    try:
        json_peticion = json.loads(request.body)
        usuario = Usuario()
        usuario.nombre = json_peticion['name']
        usuario.email = json_peticion['email']
        usuario.contrasena = json_peticion['password']
        print(json_peticion)
        if usuario.nombre == '' or usuario.email == '' or usuario.contrasena == '':
            return JsonResponse({"status": "Faltan parámetros"}, status=400)
        else:
            if Usuario.objects.filter(nombre=usuario.nombre).exists():
                return JsonResponse({"status": "Nombre de usuario ya existente"}, status=409)
            else:
                if Usuario.objects.filter(email=usuario.email).exists():
                    return JsonResponse({"status": "Email ya existente"}, status=409)
                else:
                    usuario.set_password(json_peticion['password'])
                    payload = {
                        'nombre': usuario.nombre,
                        'email': usuario.email
                    }
                    secret = 'kukizalazar'
                    token = jwt.encode(payload, secret, algorithm='HS256')
                    usuario.token = token
                    usuario.save()
                    return JsonResponse({"status": "joya"}, status=201)
    except (JSONDecodeError, Exception):
        return JsonResponse({"status": "Error"})

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

#funciona
#4. game
@csrf_exempt
def crearPartida(request):
    if request.method != 'POST':
        return None

    session_token = request.headers.get('SessionToken')
    if not session_token:
        return JsonResponse({'error': 'SessionToken no existe'}, status=400)
    try:
        if Usuario.objects.filter(token=session_token).exists():
            cantidadPartidas = Partida.objects.count() + 1
            usuario = Usuario.objects.get(token=session_token)
            players = usuario.nombre
            partida = Partida()
            partida.codigo = cantidadPartidas
            partida.createdat = timezone.now()
            partida.token_usuario = usuario
            partida.save()
            print("llega?")
            return JsonResponse({
                'code': cantidadPartidas,
                'players': [players],
                'createdAt': timezone.now()
            }, status=200)
            print("aquí no debería")
        else:
            return JsonResponse({'error': 'Invalid token'}, status=401)
    except Exception:
        return JsonResponse({"status": "Error"})

#funciona
#7.  game/codigo/drawing
@csrf_exempt
def subirDibujo(request, cod):
    if request.method != 'PUT':
        return None

    session_token = request.headers.get('SessionToken')
    if not session_token:
        return JsonResponse({'error': 'SessionToken no existe'}, status=400)
    try:
        if Usuario.objects.filter(token=session_token).exists():
            dibujo = Dibujo()
            usuario = Usuario.objects.get(token=session_token)
            dibujo.token_usuario = usuario
            dibujo.id = Dibujo.objects.count() + 1
            print("hehe")
            try:
                peticion = json.loads(request.body)
            except JSONDecodeError:
                return JsonResponse({"status": "Parámetro malformado"}, status=400)
            print("joya")
            dibujo.link = peticion["drawing"]
            partida = Partida.objects.get(codigo=cod)
            dibujo.codigo_partida=partida
            dibujo.save()
            return JsonResponse({'status':'joya'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid token'}, status=401)
    except (Exception):
        return JsonResponse({"status": "Error"})


#por probar
# 10. game/codigo/results
def podio(request, cod):
    if request.method != 'GET':
        return None
    session_token = request.headers.get('SessionToken')
    if not session_token:
        return JsonResponse({'error': 'SessionToken no existe'}, status=400)
    if Usuario.objects.filter(token=session_token).exists():
        try:
            valoresParticipa = Participa.objects.filter(codigo_partida=cod)
            listaJugadores = []
            for i in valoresParticipa:
                auxiliar = {}
                tokenAuxiliar = i.token_usuario
                print("joya")
                #usuario = Usuario.objects.filter(token=tokenAuxiliar)
                #print(usuario)
                dibujo = Dibujo.objects.filter(token_usuario=tokenAuxiliar, codigo_partida=cod).first()
                valoraciones = Valora.objects.filter(id_dibujo=dibujo)
                puntuacionAuxiliar = 0
                for j in valoraciones:
                    puntuacionAuxiliar = puntuacionAuxiliar + j.puntuacion
                auxiliar['name'] = "Usuario random porque no va lo que deberia ir" #usuario.nombre
                auxiliar['totalScore'] = puntuacionAuxiliar
                listaJugadores.append(auxiliar)
            return JsonResponse(listaJugadores, safe=False)

        except (Exception):
            return JsonResponse({"status": "Error"})
    else:
        return JsonResponse({"status": "Error"})

#funciona
#13. drawings/id/comments
@csrf_exempt
def comentar(request, id):
    if request.method != 'POST':
        return None
    session_token = request.headers.get('SessionToken')
    if not session_token:
        return JsonResponse({'error': 'SessionToken no existe'}, status=400)
    if Usuario.objects.filter(token=session_token).exists():
        try:
            requestBody = json.loads(request.body)
            comentario = Comentario()
            comentario.comentario = requestBody['comment']
            usuario = Usuario.objects.get(token=session_token)
            comentario.token_usuario = usuario
            if Dibujo.objects.filter(id=id).exists():
                dibujo = Dibujo.objects.get(id=id)
                comentario.id_dibujo = dibujo
                comentario.id = Comentario.objects.count() + 1
                comentario.save()
                return JsonResponse({"status": "Comentario añadido"}, status=201)
            else:
                return JsonResponse({"status": "La id no existe"}, status=404)
        except (Exception):
            return JsonResponse({"status": "Error"})
    else:
        return JsonResponse({"status": "Error"})
