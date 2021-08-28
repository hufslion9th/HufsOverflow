from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()


@csrf_exempt
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = "Activate your Stackoberflow account."
            message = render_to_string(
                "userauth/user_active_email.html",
                {
                    "user": user.username,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            username = form.cleaned_data.get("username")
            messages.success(
                request,
                f"New account created: {username}, Please confirm your email address to complete the registration",
            )
            return redirect("/")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            return render(
                request=request,
                template_name="userauth/signup.html",
                context={"form": form},
            )

    form = SignUpForm()
    return render(request, "userauth/signup.html", {"form": form})


@login_required
def editprofile(request):
    user = request.user
    if request.method == "POST":
        data = request.POST.dict()
        firstname = data.get("firstname")
        lastname = data.get("lastname")
        about = data.get("about")
        if firstname != "":
            user.first_name = firstname
        if lastname != "":
            user.last_name = lastname
        if about != "":
            user.about_me = about
        if request.FILES and request.FILES["fileInput"]:
            user.profile_pic = request.FILES["fileInput"]
        user.save()
        messages.success(request, "프로필이 성공적으로 업데이트되었습니다.")
    return render(request, "userauth/editprofile.html", {"user": user})


@login_required
def logout_request(request):
    logout(request)
    messages.info(request, "성공적으로 로그아웃 되었습니다!")
    return redirect("/")


@csrf_exempt
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"{username}으로 로그인되었습니다!")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password")

        else:
            messages.error(request, "Invalid username or password")

    form = AuthenticationForm()
    return render(request, "userauth/login.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(
            request,
            "Account activated successfully. Thank you for your email confirmation. Now you can login your account.",
        )
        return redirect("name_login_req")
    else:
        messages.error(request, "Activation link is invalid!")
        return redirect("name_login_req")


def find_id(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            if user is not None:
                email_subject = "HufsOverflow 아이디 확인"
                email_message = f"가입하신 계정의 ID는 {str(user.username)}입니다."
                send_email = EmailMessage(email_subject, email_message, to=[email])
                send_email.send(fail_silently=False)
                return render(request, "userauth/ID_email_send.html")
        except:
            messages.info(request, "잘못된 이메일이거나 가입된 계정 정보가 없습니다.")
    return render(request, "userauth/ID_find.html")
