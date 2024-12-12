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
            
            nombrev=formulario.cleaned_data.get("nombre")
            descripcionv=formulario.cleaned_data.get("descripcion") 
            iniciov=formulario.cleaned_data.get("inicio")
            finv=formulario.cleaned_data.get("fin")
            descuentov=formulario.cleaned_data.get("descuento")
            activov=formulario.cleaned_data.get("activo")
            
            if(nombrev!=""):
                promociones=promociones.filter(nombre=nombrev)
                mensaje+="Nombre que se ha buscado " + nombrev  +"\n"
            if(descripcionv!=""):
                promociones=promociones.filter(descripcion__contains=descripcionv)
                mensaje+="Descripcion por el que se ha buscado " + descripcionv + "\n"
            if(not iniciov is None and not finv is None):
                promociones=promociones.filter(fin__gt=iniciov,fin__lt=finv)
                mensaje+="Estamos buscando por dos fechas" + datetime.strftime(iniciov,'%d-%m-%Y')+" hasta "+datetime.strftime(finv,'%d-%m-%Y')+"\n"
            elif(not iniciov is None):
                promociones=promociones.filter(fin__gt=iniciov)
                mensaje+="La fecha desde que se esta buscando es" + datetime.strftime(iniciov,'%d-%m-%Y')+"\n"                
            elif(not finv is None):
                promociones=promociones.filter(fin__lt=finv)
                mensaje+="La fecha hasta la que se esta buscando es" + datetime.strftime(finv,'%d-%m-%Y')+"\n"
            if(not descuentov is None):
                promociones=promociones.filter(descuento__gt=descuentov)
                mensaje+="Descuento por el que se ha buscado " + str(descuentov) + "\n"
            if(activov):
                promociones=promociones.filter(activo=activov)
                mensaje+="Descripcion por el que se ha buscado " + str(activov) + "\n"                
            
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