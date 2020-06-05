from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.contrib.auth.models import User
from . import models

class CostumerForm(UserCreationForm):
    name=forms.CharField(max_length=50)
    email = forms.EmailField(max_length=70)
    class Meta(UserCreationForm.Meta):
        model = User
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.save()
        costumer = models.Customer.objects.create(user=user)
        costumer.name=self.cleaned_data.get('name')
        costumer.email=self.cleaned_data.get('email')
        costumer.save()
        return user
