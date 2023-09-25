import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from .numeros_a_letras import numero_a_letras
from .mes_a_palabra import mes_a_palabra

w, h = A4

def restar_h(nuevo_h, resta):
    nuevo_h = nuevo_h - resta
    return nuevo_h

def crear_contenido(p, letras, mes, anio, nuevo_h):
    text = p.beginText(50, nuevo_h)
    text.setFont('Helvetica', 12)
    contenido = f'           En el día de la fecha se ha registrado un ingreso de dinero de pesos {letras} correspondientes a la cuota {mes}/{anio}'

    # Ancho máximo permitido
    ancho_maximo = w - 100

    # Dividir el contenido en fragmentos que quepan en el ancho máximo
    fragmentos = []
    fragmento_actual = ''

    for palabra in contenido.split():
        if p.stringWidth(f'{fragmento_actual} {palabra}') <= ancho_maximo:
            fragmento_actual += f' {palabra}'
        else:
            fragmentos.append(fragmento_actual)
            fragmento_actual = f'{palabra}'

    # Agregar el fragmento final si existe
    if fragmento_actual:
        fragmentos.append(fragmento_actual)

    # Agregar los fragmentos a text.textLine()
    for fragmento in fragmentos:
        text.textLine(fragmento)
        nuevo_h = restar_h(nuevo_h, 20)

    # Agregar text al PDF
    p.drawText(text)

    return nuevo_h

def generar_pdf(ingreso):
    dia = ingreso.fecha.day
    mes = ingreso.fecha.month
    mes_palabra = mes_a_palabra(ingreso.fecha.month)
    anio = ingreso.fecha.year
    letras = numero_a_letras(ingreso.ingreso)
    residente = ingreso.residente
    codigo = ingreso.pk
    monto = "${:,.2f}".format(ingreso.ingreso)

    nuevo_h = h  # Restablece la variable nuevo_h
    # Cree un búfer similar a un archivo para recibir datos PDF.
    buffer = io.BytesIO()

    # Cree el objeto PDF, utilizando el búfer como su "archivo".
    p = canvas.Canvas(buffer)
    # Crea el PDF
    nuevo_h = restar_h(nuevo_h, 170)
    p.drawImage('Incomes/static/img/logosolo.png', 40, nuevo_h, width=202, height=120)
    # p.drawImage('Incomes/static/img/Malvinas_color.png', 210, nuevo_h, width=169, height=100)
    # p.drawImage('Incomes/static/img/Larrea_color.png', 380, nuevo_h, width=169, height=100)

    p.setFont('Helvetica', 12)

    fecha_larga = f'Mendoza, {dia} de {mes_palabra} de {anio}'
    p.drawRightString(w - 50, nuevo_h, fecha_larga)

    nuevo_h = restar_h(nuevo_h, 40)
    nuevo_h = crear_contenido(p, letras, mes, anio, nuevo_h)

    nuevo_h = restar_h(nuevo_h,20)
    p.drawString(50, nuevo_h, f'Residente: {residente.apellido}, {residente.nombre}')

    nuevo_h = restar_h(nuevo_h, 20)
    p.drawString(50, nuevo_h, f'Son: {monto}')

    nuevo_h = restar_h(nuevo_h, 20)
    p.setFontSize(7)
    p.drawString(50, nuevo_h, f'COD: {codigo}')


    nuevo_h = restar_h(nuevo_h, 70)
    p.drawImage('Incomes/static/img/firma.png', 430, nuevo_h, width=122, height=80)
    nuevo_h = restar_h(nuevo_h, 5)
    p.drawRightString(w - 50, nuevo_h,'Flavia Micaela Melera')

    # Cierra el PDF
    p.showPage()
    p.save()

    buffer.seek(0)

    return buffer
