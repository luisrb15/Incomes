from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import Residente
from .generadorpdf import generar_pdf
from .enviarmail import enviar_email_con_pdf_residente
from .numeros_a_letras import numero_a_letras
from .mes_a_palabra import mes_a_palabra
from datetime import date

hoy = date.today()

@login_required
def home(request):  
    return render(request, 'home.html')

@login_required
def ingresos_form(request):
    if request.method == 'POST':
        residente_id = request.POST.get('residente')
        fecha = request.POST.get('fecha')
        monto = request.POST.get('monto')
        mes_imputacion = request.POST.get('mes')
        anio_imputacion = request.POST.get('anio')
        print('residente_id', residente_id, '\nfecha', fecha, '\nmonto', monto, '\nmes_imputacion', mes_imputacion, '\nanio_imputacion', anio_imputacion)
        ingreso = Ingreso.objects.create(fecha=fecha, residente_id=residente_id, monto=monto, mes=mes_imputacion, anio=anio_imputacion) 
        pdf = generar_pdf(ingreso, fecha, mes_imputacion, anio_imputacion)
        enviar_email_con_pdf_residente(ingreso, pdf)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={ingreso.residente.apellido}_{ingreso.residente.nombre}_{ingreso.fecha}.pdf'
        
        return redirect('Incomes:home')
    residente_lista = Residente.objects.filter(active=True)
    print(residente_lista) 
    context = {
        'residentes': residente_lista,
        'hoy' : hoy,
        'mes' : hoy.month,
        'anio' : hoy.year,
        }
    return render(request, 'ingresos-form.html', context)

@login_required
def residentes(request):
    residentes_lista = Residente.objects.filter(active=True)
    context = {'residentes': residentes_lista}
    return render(request, 'residentes.html', context)

@login_required
def residente_agregar(request):
    if  request.method == 'POST':
        residente = Residente()
        residente.nombre = request.POST.get('nombre')
        residente.apellido = request.POST.get('apellido')
        residente.apodo = request.POST.get('apodo')
        residente.dni = request.POST.get('dni')
        residente.email = request.POST.get('email')
        residente.save()
        return redirect('Incomes:residentes')   
    return render(request, 'residente-form.html')

@login_required
def residentes_modificar(request, id):
    residente = get_object_or_404(Residente, id=id)
    print(residente)
    if request.method == 'POST':
        residente.nombre = request.POST.get('nombre')
        residente.apellido = request.POST.get('apellido')
        residente.apodo = request.POST.get('apodo')
        residente.dni = request.POST.get('dni')
        residente.email = request.POST.get('email')
        residente.save()
        return redirect('Incomes:residentes')  # Redirige a la lista de residentes después de guardar
    context = {'residente': residente}
    return render(request, 'residente-form.html', context)

@login_required
def residentes_eliminar(request, id):
    residente = get_object_or_404(Residente, id=id)
    residente.active = False
    residente.save()
    return redirect('Incomes:residentes')

@login_required
def cuota_crear(request, id):
    residente = get_object_or_404(Residente, id=id)
    try:
        cuota = Cuota.objects.get(residente=residente)
        form = FeeForm(request.POST or None, instance=cuota)  # Pasa la instancia a None si no hay POST data
    except Cuota.DoesNotExist:
        cuota = None
        form = FeeForm(request.POST or None)

    if request.method == 'POST':
        form = FeeForm(request.POST, instance=cuota)
        if form.is_valid():
            cuota = form.save(commit=False)
            cuota.residente = residente
            cuota.save()
            return redirect('Incomes:residentes')

    context = {'hoy': hoy , 'residente': residente, 'cuota': cuota}
    return render(request, 'cuota-form.html', context)

@login_required
def ingresos_restantes(request):
    # Obtener el mes actual
    mes_actual = datetime.now().month
    
    # Obtener todos los residentes
    residentes = Residente.objects.all()

    # Crear un diccionario para almacenar los datos de los residentes con ingresos restantes
    datos_residentes = []

    for residente in residentes:
        # Obtener la cuota del residente para el mes actual
        cuota = Cuota.objects.get(residente=residente)

        # Calcular la suma de los ingresos del residente para el mes actual
        ingresos_del_residente = Ingreso.objects.filter(residente=residente, mes=mes_actual).values('monto')
        total_ingresos = sum(ingreso['monto'] for ingreso in ingresos_del_residente)

        # Calcular el monto restante
        monto_restante = cuota.precio - total_ingresos

        datos_residentes.append({
            'residente': residente,
            'ingreso_restante': monto_restante,
        })

    context = {
        'datos_residentes': datos_residentes,
        'mes' : mes_actual,
    }
    return render(request, 'ingresos-restantes.html', context)

def ingresos(request):
    ingresos = Ingreso.objects.all().order_by('fecha')
    context = {'ingresos': ingresos}
    return render(request, 'ingresos.html', context)