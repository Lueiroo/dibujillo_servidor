# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Comentario(models.Model):
    id = models.IntegerField(primary_key=True)
    comentario = models.CharField(max_length=1000)
    token_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='token_usuario')
    id_dibujo = models.ForeignKey('Dibujo', models.DO_NOTHING, db_column='id_dibujo')

    class Meta:
        managed = False
        db_table = 'comentario'


class Contiene(models.Model):
    id = models.IntegerField(primary_key=True)
    id_dibujo = models.ForeignKey('Dibujo', models.DO_NOTHING, db_column='id_dibujo')
    codigo_partida = models.ForeignKey('Partida', models.DO_NOTHING, db_column='codigo_partida')
    historia = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'contiene'


class Dibujo(models.Model):
    id = models.IntegerField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    link = models.CharField(max_length=100)
    token_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='token_usuario')

    class Meta:
        managed = False
        db_table = 'dibujo'


class Participa(models.Model):
    id = models.IntegerField(primary_key=True)
    token_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='token_usuario')
    codigo_partida = models.ForeignKey('Partida', models.DO_NOTHING, db_column='codigo_partida')

    class Meta:
        managed = False
        db_table = 'participa'


class Partida(models.Model):
    codigo = models.IntegerField(primary_key=True)
    publica = models.IntegerField()
    token_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='token_usuario')

    class Meta:
        managed = False
        db_table = 'partida'


class Usuario(models.Model):
    token = models.CharField(primary_key=True, max_length=256)
    nombre = models.CharField(max_length=20)
    email = models.CharField(max_length=50, blank=True, null=True)
    contrasena = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'


class Valora(models.Model):
    id = models.IntegerField(primary_key=True)
    token_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='token_usuario')
    id_dibujo = models.ForeignKey(Dibujo, models.DO_NOTHING, db_column='id_dibujo')
    puntuacion = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'valora'
