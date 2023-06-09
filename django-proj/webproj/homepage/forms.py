from django import forms
from .models import Coffee # Model 호출

class CoffeeForm(forms.ModelForm): # ModelForm을 상속하는 CoffeeForm 생성
    class Meta:
        model = Coffee
        fields = ('name', 'price', 'is_ice', 'stock')
