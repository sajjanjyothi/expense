
from django import forms
from .models import Expenses
from django.conf import settings


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expenses
        exclude = ('total_expense',)
        date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
        widgets = {
            'date': forms.DateInput(attrs={'id': 'datefield'})
        }