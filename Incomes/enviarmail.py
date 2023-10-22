from django.core.mail import EmailMessage
from FinancesMaster.settings import EMAIL_HOST_USER
from .mes_a_palabra import mes_a_palabra
from .numeros_a_letras import numero_a_letras

def enviar_email_con_pdf_residente(ingreso, pdf):

    # Convierte el objeto BytesIO en bytes
    pdf_bytes = pdf.getvalue()

    monto = ingreso.monto
    # monto = "${:,.2f}".format(ingreso.ingreso)

    # Crea el mensaje de correo
    message = EmailMessage(
        f'Recibo {ingreso.residente.apellido}, {ingreso.residente.nombre}',
        f'Hemos recibido un pago. Adjunto encontrará el recibo correspondiente',
        EMAIL_HOST_USER,
        [ingreso.residente.email],
        cc=[EMAIL_HOST_USER],
    )
    
    # Adjunta el PDF al correo
    message.attach(f'{ingreso.residente.apellido}_{ingreso.residente.nombre}_{ingreso.fecha}.pdf', pdf_bytes, 'application/pdf')

    # Envía el correo
    message.send()
