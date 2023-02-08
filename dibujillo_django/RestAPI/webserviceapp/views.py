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
		participa = Participa.objects.filter(token_usuario=usuario.token)
	except Participa.DoesNotExist:
		return JsonResponse({'error': 'No se puede obtener el perfil'}, status=400)

	response_data = {'drawings': []}
	for participacion in participa:
		try:
			dibujo = Dibujo.objects.get(token=participacion.token_dibujo)
		except Dibujo.DoesNotExist:
			continue
		comentarios = Comentario.objects.filter(token_dibujo=dibujo.token)
		drawing = {
			'id': dibujo.id,
			'history': dibujo.historia,
			'path': dibujo.link,
			'uploadAt': dibujo.fecha,
			'comments': [{
				'user': comentario.usuario.nombre,
				'comment': comentario.comentario,
			} for comentario in comentarios],
		}
		response_data['drawings'].append(drawing)

	return JsonResponse(response_data)
