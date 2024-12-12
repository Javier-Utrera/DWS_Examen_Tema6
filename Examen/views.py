from django.shortcuts import render
from .models import *
from .forms import *
from django.db.models import Q,Prefetch
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,"index.html")

def mi_error_400(request,exception=None):
    return render(request,"errores/400.html",None,None,400)

def mi_error_403(request,exception=None):
    return render(request,"errores/403.html",None,None,403)

def mi_error_404(request,exception=None):
    return render(request,"errores/404.html",None,None,404)

def mi_error_500(request,exception=None):
    return render(request,"errores/500.html",None,None,500)
def listar_promociones(request):
    promocion=Promocion.objects.select_related("producto","usuarios").all()
    return render(request,"promociones/listar_promocion.html",{'views_listar_promocion':promocion})
def procesar_promocion(request):
    if (request.method == "POST"):
        formulario=PromocionForm(request.POST)
        if formulario.is_valid():
            try:
                formulario.save()
                return redirect("listar_promociones")
            except Exception as error:
                print(error)
    else:
        formulario=PromocionForm()             
    return render(request,'promociones/create.html',{"formulario":formulario})

def buscar_promocion(request):
        
    if len(request.GET)>0:
        formulario = BusquedaAvanzadaPromocion(request.GET)
        if formulario.is_valid():
            mensaje="Se ha buscado los siguientes valores: \n"
            promociones=Promocion.objects.select_related("producto","usuarios")
            
            nombre=formulario.cleaned_data.get("nombre")
            descripcion=formulario.cleaned_data.get("descripcion") 
            inicio=formulario.cleaned_data.get("inicio")
            fin=formulario.cleaned_data.get("fin")
            descuento=formulario.cleaned_data.get("descuento")
            activo=formulario.cleaned_data.get("activo")
            
            if(nombre!=""):
                promociones=promociones.filter(nombre=nombre)
                mensaje+="Nombre que se ha buscado " + nombre  +"\n"
            if(descripcion!=""):
                promociones=promociones.filter(descripcion__contains=descripcion)
                mensaje+="Descripcion por el que se ha buscado " + descripcion + "\n"
            if(not inicio is None):
                promociones=promociones.filter(inicio__gte=inicio)
                mensaje+="La fecha por la que se esta buscando es" + datetime.strftime(inicio,'%d-%m-%Y')+"\n"
            if(not fin is None):
                promociones=promociones.filter(fin__gte=fin)
                mensaje+="La fecha por la que se esta buscando es" + datetime.strftime(fin,'%d-%m-%Y')+"\n"
            if(not descuento is None):
                promociones=promociones.filter(descuento__gte=descuento)
                mensaje+="Descuento por el que se ha buscado " + str(descuento) + "\n"
            if(activo):
                promociones=promociones.filter(activo=True)
                mensaje+="Descripcion por el que se ha buscado " + str(activo) + "\n"                
            
            promociones=promociones.all()
            
            return render(request,"promociones/listar_promocion.html",{
            "views_listar_promocion":promociones,
            "texto_busqueda":mensaje})
    
    else:
        formulario=BusquedaAvanzadaPromocion(None)
    return render(request, 'promociones/busqueda_avanzada.html',{"formulario":formulario})

def editar_promocion(request,promocion_id):
    promocion = Promocion.objects.get(id=promocion_id)
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    
    formulario = PromocionForm(datosFormulario,instance = promocion)
    
    if (request.method == "POST"):
       
        if formulario.is_valid():
            try:  
                formulario.save()
                messages.success(request, 'Se ha editado la promocion '+formulario.cleaned_data.get('nombre')+" correctamente")
                return redirect('listar_promociones')  
            except Exception as error:
                print(error)
    return render(request, 'promociones/actualizar.html',{"formulario":formulario,"promocion":promocion})

def eliminar_promocion(request,promocion_id):
    promocion = Promocion.objects.get(id=promocion_id)
    try:
        promocion.delete()
        messages.success(request, "Se ha elimnado el cliente "+promocion.nombre+" correctamente")
    except Exception as error:
        print(error)
    return redirect('listar_promociones')