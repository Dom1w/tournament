from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from ranker.models import GameAndFormatMeta


class UploadForm(forms.Form):

    game_format = forms.ModelChoiceField(queryset=GameAndFormatMeta.objects.all())

    file_format = forms.ChoiceField(choices=(
        (1, _("TCGRanks.com Format")),
        (2, _("Magic Tournament Software")),
        (3, _("Yu-Gi-Oh Tournament Software")),
        ), label="File Format", widget=forms.Select(), required=True)

    file = forms.FileField(max_length=300, required=True)
