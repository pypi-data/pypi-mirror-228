from django.shortcuts import render, redirect


def adminplus(request):
    if not request.user.is_staff or not request.user.is_active:
        return redirect('admin:index')

    return render(request, '_adminplus/adminplus.html')
