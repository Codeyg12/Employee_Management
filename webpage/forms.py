from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Employee, Role, Department

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = ''

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

        
class AddDepartmentForm(forms.ModelForm):
    department_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Department Name', "class": 'form-control'}), label='')

    class Meta:
        model = Department
        exclude = ('user',)

class AddRoleForm(forms.ModelForm):
    title = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control'}), label='')
    salary = forms.IntegerField(required=True, widget=forms.widgets.NumberInput(attrs={'placeholder': 'Salary', 'class': 'form-control'}), label='')
    role_department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True, widget=forms.widgets.Select(attrs={'class': 'form-control text-muted'}), empty_label='Select Department Name', label='')

    class Meta:
        model = Role
        exclude = ('user',)
