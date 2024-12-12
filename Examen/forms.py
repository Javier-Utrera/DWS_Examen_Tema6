from django import forms
from django.forms import ModelForm
from .models import *
from datetime import *
import re 
from django.utils import timezone 

    #Promocion   
class PromocionForm(ModelForm):
    class Meta:
        model = Promocion
        fields = '__all__'
        labels = {
            "descripcion" : ("Descripcion de producto"),
            "nombre": ("Nombre"),
            "producto": ("Producto"),
            "usuarios": ("Usuarios"),
            "descuento": ("Descuento"),
            "inicio": ("Fecha de inicio de la promocion"),
            "fin": ("Fecha de finalizacion de la promocion"),
            "activo": ("¿Está activa la promocion?")
        }
        help_texts = {
            "nombre" : ("Tiene que ser unico"),
            "descripcion" : ("Al menos 100 caracteres"),
            "usuarios" : ("Mayores de edad"),
            "descuento" : ("Numero entero entre 0 y 10"),
            "inicio" : ("Anterior a la fecha de finalizacion de la promocion"),
            "fin" : ("Superior a la fecha actual"),
        }
        widgets = {
            "descripcion" : forms.TextInput(),
            "usuarios" : forms.Select(),
            "descuento" : forms.NumberInput(),
            "inicio" : forms.DateInput(format="%Y-%m-%d", 
                                                        attrs={"type": "date"},),
            "fin" : forms.DateInput(format="%Y-%m-%d", 
                                                        attrs={"type": "date"},),
        }
        localized_fields = ["inicio","fin"]
        
    def clean(self):
        
        super().clean()
        nombre=self.cleaned_data.get('nombre')
        descripcion=self.cleaned_data.get('descripcion')
        producto=self.cleaned_data.get('producto')
        usuarios=self.cleaned_data.get('usuarios')
        descuento=self.cleaned_data.get('descuento')
        inicio=self.cleaned_data.get('inicio')
        fin=self.cleaned_data.get('fin')
        
        #VALIDAMOS DNI
               
        promocion=Promocion.objects.filter(nombre=nombre).first()
        
        if(promocion):
           self.add_error("nombre","Este nombre ya esta registrado en la base de datos")
           
        if(len(descripcion)<100):
            self.add_error("descripcion","Este campo debe tener mas de 100 caracteres")
            
        productos=Producto.objects.get(nombre=producto)
        
        if(productos.puede_tener_promociones==False):
           self.add_error("producto","El producto que ha seleccionado no se le permite hacerle promociones")
           
        if(descuento<0 or descuento>10):
           self.add_error("descuento","El valor del descuento tiene que ser entre 0 y 10")
           
        if(inicio>fin):
            self.add_error("inicio","La fecha de inicio no puede ser superior a la de finalizacion")
            
        if(fin<timezone.now().date()):
            self.add_error("fin","La fecha de finalizacion no puede ser inferior a la actual")
        return self.cleaned_data
            
class BusquedaAvanzadaPromocion(forms.Form):
    
    nombre=forms.CharField(required=False,label="Nombre")
    descripcion=forms.CharField(required=False,label="Descripcion")
    inicio = forms.DateField(label="Fecha Desde",
                                required=False,
                                 widget= forms.DateInput(format="%Y-%m-%d", 
                                                          attrs={"type": "date"},))
    
    fin = forms.DateField(label="Fecha Hasta",required=False,
                                  widget= forms.DateInput(format="%Y-%m-%d", 
                                                          attrs={"type": "date"},))
    descuento=forms.IntegerField(required=False)
    activo=forms.BooleanField(required=False)
    
    def clean(self):
        
        super().clean()
        
        nombre=self.cleaned_data.get("nombre")
        descripcion=self.cleaned_data.get("descripcion") 
        inicio=self.cleaned_data.get("inicio")
        fin=self.cleaned_data.get("fin")
        descuento=self.cleaned_data.get("descuento")
        activo=self.cleaned_data.get("activo")
        
        if(nombre == "" and descripcion =="" and inicio is None and fin is None and descuento is None):
            self.add_error("nombre","Debes rellenar algun dato")
            self.add_error("descripcion","Debes rellenar algun dato")
            self.add_error("inicio","Debes seleccionar una fecha")
            self.add_error("fin","Debes seleccionar una fecha")
            self.add_error("descuento","Debes rellenar algun dato")

        else:
            if inicio and (inicio>fin):
                self.add_error("inicio","La fecha de inicio no puede ser superior a la final")
            if fin and (fin<inicio):
                self.add_error("fin","La fecha final no puede ser inferior a la inicial")
            if activo==False:
                self.add_error("activo","Solo puedo buscar promociones activas")   
        return self.cleaned_data        