from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import EmailLog
from .forms import EmailForm, RegisterForm, LoginForm
from .utils import encrypt_message, decrypt_message, calculate_bandwidth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage, BadHeaderError
from django.core.mail import send_mail, BadHeaderError
from cryptography.fernet import InvalidToken
from cryptography.fernet import Fernet
import smtplib

ENCRYPTION_KEY = Fernet.generate_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('send_email')
        else:
            messages.error(request, 'Please correct the errors below and try again.')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('send_email')  # Or your home/dashboard page
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect('login')
    return render(request, 'login.html')
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required

def send_email_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            recipient_email = form.cleaned_data['recipient_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            attachment = request.FILES.get('file_attachment')

            sender_name = request.user.username
            sender_email = request.user.email

            # 🔥 Correct encryption
            encrypted_message = encrypt_message(message)

            try:
                email = EmailMessage(
                    subject=f"[Encrypted] {subject}",
                    body=f"Encrypted Message:\n\n{encrypted_message}",
                    from_email=f"{sender_name} via Secure Email Sender <testprojecthere147@gmail.com>",
                    to=[recipient_email],
                )

                if attachment:
                    email.attach(attachment.name, attachment.read(), attachment.content_type)

                email.send()

                # Save in EmailLog model (correctly)
                bandwidth_used = calculate_bandwidth(message, attachment)
                EmailLog.objects.create(
                    user=request.user,
                    recipient=recipient_email,
                    subject=subject,
                    message=message,
                    encrypted_message=encrypted_message,
                    file_attachment=attachment,
                    bandwidth_used=bandwidth_used,
                )

                messages.success(request, 'Encrypted email sent successfully!')
                return redirect('send_email')

            except (smtplib.SMTPRecipientsRefused, smtplib.SMTPDataError, smtplib.SMTPException) as e:
                messages.error(request, f"Failed to deliver email. Address {recipient_email} was refused.")
            except Exception as e:
                messages.error(request, f"Unexpected error occurred: {str(e)}")
        else:
            messages.error(request, 'Please correct the form errors below.')
    else:
        form = EmailForm()

    return render(request, 'send_email.html', {'form': form})

@login_required
def dashboard(request):
    user_email = request.user.email
    messages = EmailLog.objects.filter(recipient=user_email)
    decrypted_messages = []
    
    for msg in messages:
        try:
            decrypted_msg = decrypt_message(msg.encrypted_message)
            decrypted_messages.append((msg, decrypted_msg))
        except InvalidToken:
            decrypted_messages.append((msg, None))  # Cannot decrypt

    return render(request, 'dashboard.html', {'messages': decrypted_messages})  