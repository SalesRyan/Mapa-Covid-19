from django.core.mail import send_mail
from django.contrib.auth.models import User

def mail(subject, message):
    user = User.obejcts.all()
    send_mail(
        subject,
        message,
        'notificacaodaaplicacao@gmail.com',
        [ob.email for ob in user],
        fail_silently=False,
    )