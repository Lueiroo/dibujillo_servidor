from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from .models import Usuario, Partida, Dibujo, Valora, Comentario, Participa
import jwt
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from json import JSONDecodeError
from django.contrib.auth.hashers import check_password, make_password

# Create your views here.

#Esta funciona
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


#funciona
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
                dibujo = Dibujo.objects.get(token_usuario=tokenAuxiliar)
                linkAuxiliar = dibujo.link
                valoraciones = Valora.objects.filter(id_dibujo=linkAuxiliar)
                puntuacionAuxiliar = 0
                for j in valoraciones:
                    puntuacionAuxiliar = puntuacionAuxiliar + j.puntuacion
                usuario = Usuario.objects.filter(token=tokenAuxiliar)
                auxiliar['name'] = usuario.nombre #no sé por qué sale en blanco
                auxiliar['totalScore'] = puntuacionAuxiliar
                listaJugadores.append(auxiliar)
            return JsonResponse(listaJugadores, safe=False)

        except (Exception):
            return JsonResponse({"status": "Error"})
    else:
        return JsonResponse({"status": "Error"})

#por probar
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
            comentario.token_usuario = session_token
            if Comentario.objects.filter(id_dibujo=id).exists():
                comentario.id_dibujo = id
                comentario.id = Comentario.objects.count() + 1
                comentario.save()
                return JsonResponse({"status": "Comentario añadido"}, status=201)
            else:
                return JsonResponse({"status": "La id no existe"}, status=404)
        except (Exception):
            return JsonResponse({"status": "Error"})
    else:
        return JsonResponse({"status": "Error"})
