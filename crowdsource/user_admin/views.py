from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def admin_login(request):
    try:
        # already logged in
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect('/user_admin/dashboard')

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            # check account exists
            user_qs = User.objects.filter(username=username)
            if not user_qs.exists():
                messages.info(request, 'Account not found')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/admin-panel/'))

            # authenticate
            user_obj = authenticate(username=username, password=password)

            if user_obj and user_obj.is_superuser:
                login(request, user_obj)
                return redirect('/user_admin/dashboard/')

            messages.info(request, 'Invalid password')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/admin-panel/'))

        return render(request, 'home/admin_panel.html')
    except Exception:
        messages.error(request, 'Something went wrong')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/admin-panel/'))

@login_required(login_url='/admin-panel/')
def dashboard(request):
    if not request.user.is_superuser:
        logout(request)
        return redirect('/admin-panel/')
    return render(request, 'home/admin_panel.html')

@login_required(login_url='/user_admin/admin-panel/')
def admin_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('/user_admin/admin-panel/')

def demo(request):
    return render(request ,'home/index1.html')