from django import forms

from credits import models


class OfferForm(forms.ModelForm):

    class Meta:
        model = models.Offer
        exclude = ['id']

    def clean(self):
        min_score = self.cleaned_data.get('min_score')
        max_score = self.cleaned_data.get('max_score')
        if max_score < min_score:
            raise forms.ValidationError('Минимальны скоринговый балл должен быть меньше максимального')
        return self.cleaned_data
