import datetime

from coreapi.compat import force_text
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from fpdf import FPDF
import qrcode
from main.settings import MEDIA_ROOT
from .crt_gen import cert_gen
from .forms import UserRegisterForm, UserLoginForm
from .models import CustomUser, UserRequest
from .token import account_activation_token

result = ''
acc = ''
med = ''
email = ''
med_l = ''
id = ''


def index(request):
    return render(request, 'index.html')


def activate(request, uidb64, token):
    CustomUser = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            cert_gen(emailAddress=user.email,
                     commonName=user.last_name + " " + user.first_name + " " + user.after_name,
                     countryName="KZ",
                     localityName=user.username,
                     stateOrProvinceName="stateOrProvinceName",
                     organizationName="organizationName",
                     organizationUnitName="organizationUnitName",
                     serialNumber=0,
                     validityStartInSeconds=0,
                     validityEndInSeconds=10 * 365 * 24 * 60 * 60,
                     KEY_FILE=MEDIA_ROOT + f"\\media\\private-{user.username}.key",
                     CERT_FILE=MEDIA_ROOT + f"\\media\\cert-{user.username}.crt")
            form.save()
            current_site = get_current_site(request)
            mail_subject = f'Activation link has been sent to your email id'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.attach_file(MEDIA_ROOT + f"\\media\\cert-{user.username}.crt")
            email.attach_file(MEDIA_ROOT + f"\\media\\private-{user.username}.key")
            email.send()
            return redirect('index')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {"form": form})


def user_login(request):
    form = UserLoginForm(data=request.POST)
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        my_uploaded_file = request.FILES['serv_login'].read().decode().replace('\n', '').replace('\r', '')
        serv = open(MEDIA_ROOT + f"\\media\\cert-{user.username}.crt", "r").read().replace('\n', '').replace('\r', '')
        if str(my_uploaded_file) == serv:
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('account')
                else:
                    return HttpResponse("Account deleted or disabled")
        else:
            messages.error(request, "The certificate does not converge")

    return render(request, 'login.html', {"form": form})


""


def user_logout(request):
    logout(request)
    return redirect('index')


res = ""


def account(request):
    if request.user.is_authenticated:
        user = request.user
        med = user.med_id.all()
        if user.roles == 'P':
            try:
                if request.method == 'POST':
                    messages.success(request, 'The application has been sent')
            except:
                messages.success(request, 'The application for this mail was previously sent')
                pass
            if request.method == 'POST':
                my_uploaded_file = request.FILES['serv_verify'].read().decode().replace('\n', '').replace('\r', '')
                serv = open(MEDIA_ROOT + f"\\media\\private-{request.user.username}.key", "r").read().replace('\n',
                                                                                                              '').replace('\r', '')
                if str(my_uploaded_file) == serv:
                    values = list(dict(request.POST).values())
                    result1 = "".join(values[1]).split(" ")
                    if result1[-1] == 'GO':
                        print(result1)
                        print(values)
                        form = UserRequest(name=result1[1] + " " + result1[2] + " " + result1[3], email=result1[0],
                                           description=result1[-2])
                        form.save()
                else:
                    messages.error(request, "The certificate does not converge")
            return render(request, 'user.html', {"med": med})
        if user.roles == 'D':
            pacient = UserRequest.objects.all
            if request.method == 'POST':
                values = list(dict(request.POST).values())
                global res
                res = "".join(values[-1])
                print(values)
                print(res)
                return redirect('verify')
            return render(request, 'doctor_user.html', {"pacient": pacient})
        else:
            return HttpResponse('You have not been registered')
    else:
        return redirect('index')


def pacient_list(request):
    if request.user.is_authenticated:
        user = request.user
        med = user.med_id.all()
        if user.roles == 'P':
            return render(request, 'user.html', {"med": med})
        if user.roles == 'D':
            pacient = CustomUser.objects.all
            return render(request, 'doctor-patients.html', {"pacient": pacient, "med": med})
    else:
        return redirect('index')


def verify(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            if user.roles == 'D':
                person = UserRequest.objects.get(pk=res)
                my_uploaded_file = request.FILES['serv_verify'].read().decode().replace('\n', '').replace('\r', '')
                serv = open(MEDIA_ROOT + f"\\media\\private-{request.user.username}.key", "r").read().replace('\n', '').replace(
                    '\r', '')
                if str(my_uploaded_file) == serv:
                    message = "The application is approved!"
                    email_doc = EmailMessage(message, to={person.email})
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=15)
                    pdf.cell(200, 10, txt="E-medicine platform",
                             ln=1, align='C')
                    pdf.cell(200, 10, txt="The application is approved! Take the medicine " + person.description + '.',
                             ln=2)
                    pdf.cell(200, 10, txt='Doctor: ' + user.last_name + ' ' + user.first_name,  ln=3)
                    pdf.cell(200, 10, txt='Date: ' + str(datetime.datetime.now().date()),  ln=4)
                    pdf.cell(200, 10, txt='Medicine: ' + person.description, ln=4)

                    qr_image = qrcode.make('Check for medicine ' + person.description
                                           + '. Approved by ' + user.last_name + ' ' + user.first_name + '.'
                                           + ' Approved to ' + person.name)
                    qr_image.save(MEDIA_ROOT + f"\\media\\qr\\{person.name.replace(' ', '_') + ' ' + person.description + ' ' + str(datetime.datetime.now().date())}.png")
                    pdf.image(name=MEDIA_ROOT + f"\\media\\qr\\{person.name.replace(' ', '_') + ' ' + person.description + ' ' + str(datetime.datetime.now().date())}.png",
                              x = 60, y = 60, w = 100, h = 100)
                    pdf.output(
                        MEDIA_ROOT + f"\\media\\pdf\\{person.name.replace(' ', '_') + ' ' + person.description + ' ' + str(datetime.datetime.now().date())}.pdf")

                    email_doc.attach_file(
                        MEDIA_ROOT + f"\\media\\pdf\\{person.name.replace(' ', '_') + ' ' + person.description + ' ' + str(datetime.datetime.now().date())}.pdf")
                    email_doc.send()
                    UserRequest.objects.get(id=res).delete()
                    return redirect("account")
                else:
                    messages.error(request, "The certificate does not converge")
        else:
            pass

        return render(request, 'verify.html')
    else:
        return redirect('index')
