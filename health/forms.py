from django import forms
from django.forms import ModelForm, Textarea

from health.models import Main_food, Profile_user

class RegisterForm(forms.Form):
    username        = forms.CharField(max_length=100, widget=forms.TextInput(
                                        attrs={'class':'form__input', 'placeholder': 'Username'}))
    password        = forms.CharField(max_length=32, widget=forms.PasswordInput(
                                        attrs={'class': 'form__input', 'placeholder': 'Password'}))
    password_conf   = forms.CharField(max_length=32, widget=forms.PasswordInput(
                                        attrs={'class': 'form__input', 'placeholder': 'Repeat Password'}))
    email           = forms.EmailField(label="Email", max_length=150, widget=forms.EmailInput(
                                        attrs={'class': 'form__input', 'placeholder': 'Email'}))
    height          = forms.IntegerField(min_value=10, max_value=500, widget=forms.NumberInput(
                                        attrs={'class':'form__input', 'placeholder': 'height(cm)'}))                  
    weight          = forms.FloatField(min_value=10, max_value=500, widget=forms.NumberInput(
                                        attrs={'class': 'form__input', 'placeholder': 'weight'}))

class ProfileForm(ModelForm):
    # email           = forms.EmailField(label="Email", max_length=150, widget=forms.EmailInput(
                                        # attrs={'class': 'form__input', 'placeholder': 'Email'}))
    class Meta:
        model = Profile_user
        fields = '__all__'
        exclude = ['user', 'favourite_foods']
        widgets = {
            'email': forms.EmailInput(attrs={'class':'form__input'}),
            'first_name': forms.TextInput(attrs={'class':'form__input'}),
            'last_name': forms.TextInput(attrs={'class':'form__input'}),
            'weight': forms.NumberInput(attrs={'class':'form__input'}),
            'height': forms.NumberInput(attrs={'class':'form__input'}),
            'age': forms.NumberInput(attrs={'class':'form__input'}),
            'weight_goal': forms.NumberInput(attrs={'class':'form__input'}),
        }