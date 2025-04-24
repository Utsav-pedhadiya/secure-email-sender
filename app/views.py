from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import EmailLog
from .forms import EmailForm, RegisterForm, LoginForm
from .utils import encrypt_message, decrypt_message, calculate_bandwidth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user:
                login(request, user)
                return redirect("send_email")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def send_email_view(request):
    if request.method == "POST":
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            encrypted_message = encrypt_message(message)
            file = request.FILES.get('attach_file')
            bandwidth_used = calculate_bandwidth(message, file)

            EmailLog.objects.create(
                user=request.user,
                recipient=recipient,
                subject=subject,
                message=message,
                encrypted_message=encrypted_message,
                bandwidth_used=bandwidth_used,
                file_attachment=file
            )

            send_mail(subject, f"Encrypted Message:\n{encrypted_message}", 'your_email@gmail.com', [recipient], fail_silently=False)

            return render(request, "email_sent.html", {'recipient': recipient, 'bandwidth_used': bandwidth_used})

    else:
        form = EmailForm()

    return render(request, "send_email.html", {'form': form})

@login_required
def dashboard(request):
    # Show decrypted messages sent to the logged-in user
    user_email = request.user.email
    messages = EmailLog.objects.filter(recipient=user_email)
    decrypted_messages = [(msg, decrypt_message(msg.encrypted_message)) for msg in messages]
    return render(request, 'dashboard.html', {'messages': decrypted_messages})
