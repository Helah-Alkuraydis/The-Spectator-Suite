from django import forms

class VIPRegistrationForm(forms.Form):
    full_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Full Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'email@luxury.com'}))
    favorite_sport = forms.ChoiceField(choices=[('Tennis', 'Tennis'), ('Football', 'Football')])
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Tell us about your spectator style...', 'rows': 3}))