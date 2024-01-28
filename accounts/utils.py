from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage,message
from django.conf import settings

#Helper Function
def detectUser(user):
    if user.role==1:
        redirectUrl = 'vendordashboard'
        return redirectUrl
    elif user.role==2:
        redirectUrl = 'customerdashboard'
        return redirectUrl
    
    elif user.role==None and user.is_superadmin:
        redirectUrl='/admin'
        return redirectUrl

def send_verification_email(request,user,mail_subject,email_template):
    from_email=settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    print('start')
    #mail_subject = 'Please activate your account'
    message = render_to_string(email_template,{
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),

    })
    to_email = user.email
    mail = EmailMessage(mail_subject , message ,from_email, to = [to_email])
    print('end')
    mail.send()  
'''
def send_password_reset_email(request,user):
     
    from_email=settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    print('start')
    mail_subject = 'Please reset your password'
    message = render_to_string('accounts/emails/reset_password_email.html',{
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),

    })
    to_email = user.email
    mail = EmailMessage(mail_subject , message ,from_email, to = [to_email])
    print('end')
    mail.send()  
'''
def send_notification(mail_subject,mail_template,context):
    from_email=settings.DEFAULT_FROM_EMAIL
    print('start')
    #mail_subject = 'Please activate your account'
    message = render_to_string(mail_template,context)

    ##Change of script becoz of orders.views confirmation_email
    #to_email = context['user'].email
    to_email=context['to_email']
    mail = EmailMessage(mail_subject , message ,from_email, to = [to_email])
    print('end')
    mail.send()  