from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site

from Member.models import Member, MemberRole
from .models import CustomUser
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_unusable_password()
            user.save()
            return redirect('accounts:registration_complete')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def registration_complete(request):
    return render(request, 'registration_complete.html')

@login_required
def set_password(request):
    if request.method == 'POST':
        form = SetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            return redirect('accounts:password_set_complete')
    else:
        form = SetPasswordForm(user=request.user)
    return render(request, 'set_password.html', {'form': form})

def password_set_complete(request):
    return render(request, 'password_set_complete.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('accounts:dashboard')
                else:
                    return redirect('accounts:user_landing_page')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    django_logout(request)
    return redirect('accounts:login')

@login_required
def dashboard(request):
    if request.user.is_staff:
        pending_users = CustomUser.objects.filter(is_approved=False)
        approved_users = CustomUser.objects.filter(is_approved=True)
        members = Member.objects.filter(is_approved=False)
        approved_members = Member.objects.all()
        roles = MemberRole.objects.all()
        
        
        approved_users_with_password = [user for user in approved_users if user.has_usable_password()]
        approved_users_without_password = [user for user in approved_users if not user.has_usable_password()]
        
        return render(request, 'dashboard.html', {
            'pending_users': pending_users,
            'approved_users_with_password': approved_users_with_password,
            'approved_users_without_password': approved_users_without_password,
            'members':members,
            'approved_members':approved_members,
            'roles':roles,
        })
    else:
        return redirect('home')

@login_required
def approve_user(request, user_id):
    if request.user.is_staff:
        user = get_object_or_404(CustomUser, id=user_id)
        user.is_approved = True
        user.is_active = True
        user.save()
        
        current_site = get_current_site(request)
        mail_subject = 'Your account has been approved'
        message = render_to_string('approve_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        send_mail(mail_subject, message, 'sakhyam4@gmail.com', [user.email])
        
        return redirect('accounts:dashboard')
    else:
        return redirect('home')

@login_required
def disapprove_user(request, user_id):
    if request.user.is_staff:
        user = get_object_or_404(CustomUser, id=user_id)
        user.delete()
        return redirect('accounts:dashboard')
    else:
        return redirect('home')

@login_required
def delete_user(request, user_id):
    if request.user.is_staff:
        user = get_object_or_404(CustomUser, id=user_id)
        user.delete()
        return redirect('accounts:dashboard')
    else:
        return redirect('home')

@login_required
def user_landing_page(request):
    return render(request, 'user_landing_page.html', {'user': request.user})

def set_initial_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, user)
                return redirect('accounts:password_set_complete')
        else:
            form = SetPasswordForm(user=user)
        return render(request, 'set_password.html', {'form': form})
    else:
        return render(request, 'password_reset_invalid.html')



