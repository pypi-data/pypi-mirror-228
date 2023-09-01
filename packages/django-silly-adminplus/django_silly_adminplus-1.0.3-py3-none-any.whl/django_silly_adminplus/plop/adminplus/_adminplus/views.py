from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages

from django_silly_adminplus.config import SILLY_ADMINPLUS


User = get_user_model()


def create_user(request):
    if not request.user.is_staff and request.user.is_active:
        return redirect('admin:index')

    if request.method == 'POST':
        print("=== request.post: ", request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(username) < 1:
            messages.add_message(
                request,
                messages.ERROR,
                message="Userame must be at least 1 character long",
                extra_tags="danger")

            return render(request, '_adminplus/create_user.html')
        try:
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()
        except Exception as e:
            messages.add_message(
                request,
                messages.ERROR,
                message=str(e),
                extra_tags="danger")

            return render(request, '_adminplus/create_user.html')

        messages.add_message(
            request,
            messages.SUCCESS,
            message="User created successfully",
            extra_tags="success")

    return render(request, '_adminplus/create_user.html')


def adminplus(request):
    if not request.user.is_staff or not request.user.is_active:
        return redirect('admin:index')

    return render(request, SILLY_ADMINPLUS['TEMPLATE'])
