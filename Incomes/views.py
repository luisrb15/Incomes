from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import Residente
from .generadorpdf import generar_pdf
from .enviarmail import enviar_email_con_pdf_residente
from .numeros_a_letras import numero_a_letras
from .mes_a_palabra import mes_a_palabra

# Create your views here.

@login_required
def home(request):  
    return render(request, 'home.html')

@login_required
def ingresos_form(request):
    print(request.POST.get('fecha'))
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            residente_id = request.POST.get('residente')
            fecha = request.POST.get('fecha')
            mes_imputacion = request.POST.get('mes')
            anio_imputacion = request.POST.get('anio')
            cuota = Cuota.objects.get(residente_id=residente_id)
            form.instance.cuota = cuota
            form.save()
            ingreso = Ingreso.objects.last()
            pdf = generar_pdf(ingreso, fecha, mes_imputacion, anio_imputacion)
            enviar_email_con_pdf_residente(ingreso, pdf)
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename={ingreso.residente.apellido}_{ingreso.residente.nombre}_{ingreso.fecha}.pdf'
            
            return redirect('Incomes:home')
    else:
        form = IncomeForm() 
        form.fields['residente'].queryset = Residente.objects.filter(active=True)        

    context = {'form': form}
    return render(request, 'ingresos-form.html', context)

@login_required
def residentes(request):
    residentes_lista = Residente.objects.filter(active=True)
    context = {'residentes': residentes_lista}
    return render(request, 'residentes.html', context)

@login_required
def residente_agregar(request):
    form = ResidentForm(request.POST)
    context = {'form' : form }
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('Incomes:residentes')   
    return render(request, 'residente-form.html', context)

@login_required
def residentes_modificar(request, id):
    residente = get_object_or_404(Residente, id=id)
    if request.method == 'POST':
        form = ResidentForm(request.POST, instance=residente)
        if form.is_valid():
            form.save()
            return redirect('Incomes:residentes')  # Redirige a la lista de residentes después de guardar
    else:
        form = ResidentForm(instance=residente)  
    context = {'form': form, 'residente': residente}
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

    context = {'form': form, 'residente': residente}
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
        ingresos_del_residente = Ingreso.objects.filter(residente=residente, mes=mes_actual).values('ingreso')
        total_ingresos = sum(ingreso['ingreso'] for ingreso in ingresos_del_residente)

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