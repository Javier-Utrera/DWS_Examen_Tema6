from django.db import models
from django.conf import settings
from django.utils import timezone 

# Create your models here.
class Usuario(models.Model):    
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    puede_tener_promociones = models.BooleanField()

    def __str__(self):
        return self.nombre

class Promocion(models.Model):
    nombre = models.CharField(max_length=100,unique=True)
    descripcion = models.TextField(default="")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE,related_name="producto_Promocion")
    usuarios = models.ForeignKey(Usuario, on_delete=models.CASCADE,related_name="usuario_Promocion")
    descuento = models.PositiveSmallIntegerField(default=0)
    inicio=models.DateField(null=True)
    fin=models.DateField(null=True)
    activo=models.BooleanField(default=False)
    