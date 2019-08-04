from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from ranker.models import FormatInGameInstance


class UploadForm(forms.Form):

    game_format = forms.ModelChoiceField(queryset=FormatInGameInstance.objects.all())

    file_format = forms.ChoiceField(choices=(
        (1, _("TCG Ranker Format")),
        (2, _("Magic Tournament Software")),
        (3, _("Yu-Gi-Oh Tournament Software")),
        ), label="File Format", widget=forms.Select(), required=True)

    file = forms.FileField(max_length=300, required=True)
