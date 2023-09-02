from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Configuration
from .forms import ConfigForm


def adminplus(request):
    if not request.user.is_staff or not request.user.is_active:
        return redirect('admin:index')

    if request.method == 'POST':
        config_form = ConfigForm(request.POST)
        configuration = Configuration.objects.first()
        if config_form.is_valid():
            # configuration.open_subscriptions = config_form.cleaned_data['open_subscriptions']
            configuration.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                message="Configuration updated successfully",
                extra_tags="success")
        else:
            messages.add_message(
                request,
                messages.ERROR,
                message="Invalid form",
                extra_tags="danger")

    configuration = Configuration.objects.first()
    config_form = ConfigForm(instance=configuration)
    context = {
        'configuration': configuration,
        'config_form': config_form,
    }

    return render(request, '_adminplus/adminplus.html', context)
