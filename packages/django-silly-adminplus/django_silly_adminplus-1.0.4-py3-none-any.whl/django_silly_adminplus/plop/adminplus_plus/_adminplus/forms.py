from django import forms
from .models import Configuration


class ConfigForm(forms.ModelForm):
    """Form for changing AdminPlus configuration."""
    error_css_class = 'error'

    class Meta:
        model = Configuration
        fields = '__all__'
        widgets = {
            # 'open_subscriptions': forms.CheckboxInput(attrs={'class': 'checkbox'}),
        }
