from django.shortcuts import render, redirect
from django_silly_adminplus.config import SILLY_ADMINPLUS


def adminplus(request):
    if request.user.is_staff and request.user.is_active:
        return render(request, SILLY_ADMINPLUS['TEMPLATE'])
    else:
        return redirect('admin:index')
