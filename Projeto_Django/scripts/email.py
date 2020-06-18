from django.core.mail import send_mail

def mail(subject, message):
    send_mail(
        subject,
        message,
        'notificacaodaaplicacao@gmail.com',
        ['slelis@ufpi.edu.br', 'lucasbezerraufpi527@ufpi.edu.br', 'sales@ufpi.edu.br'],
        fail_silently=False,
    )