from django import forms
from django.forms import ModelForm
from django.forms.widgets import DateInput
from django.contrib.auth.models import User
from .models import Student, Profesor, Pay_method, Document, Post_file 

#ClassForms
class SignupForm(forms.Form):
    """Sign up form."""

    username = forms.CharField(min_length=4, max_length=50,         
       widget=forms.TextInput(attrs={'class': 'form-control'}),
       label='Usuario'
       )

    password = forms.CharField(
        max_length=70,
        widget=forms.PasswordInput(    
            attrs={
            'class': 'form-control'
        }),
        label='Contraseña'
    )
    password_confirmation = forms.CharField(
        max_length=70,
        widget=forms.PasswordInput(        
            attrs={
                'class': 'form-control'
        }),
        label='Confirmar Contraseña'

    )

    first_name = forms.CharField(min_length=2, max_length=50, 
        widget=forms.TextInput(
            attrs={
            'class': 'form-control'
        }),
        label='Nombre'
    )
    last_name = forms.CharField(min_length=2, max_length=50, 
        widget=forms.TextInput(
            attrs={
            'class': 'form-control'
        }),
        label='Apellido'
    )
    email = forms.CharField(
        min_length=6,
        max_length=70,
        widget=forms.EmailInput(
            attrs={
            'class': 'form-control'
        }),
        label='Correo Electronico'
    )

    def clean_username(self):
        """Username must be unique."""
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError('Username is already in use.')
        return username

    def clean(self):
        """Verify password confirmation match."""
        data = super().clean()

        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Passwords do not match.')

        return data

    def save(self):
        """Create user and profile."""
        data = self.cleaned_data
        data.pop('password_confirmation')

        user = User.objects.create_user(**data)
        employee_saved = user
        employee_saved.save()


class UserUpdateForm(forms.ModelForm):
    """Form definition for User."""

    class Meta:
        """Meta definition for Userform."""
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )
        exclude = [
        'password', 
        'groups', 
        'user_permissions', 
        'is_staff', 
        'is_active',
        'is_superuser',
        'last_login', 
        'date_joined',
        ]

        lable = {
            'username': 'Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Email',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
        }
        

#ModelForms
class StudentForm(forms.ModelForm):
    """Form definition for Student."""

    class Meta:
        """Meta definition for Studentform."""

        model = Student
        fields = (
            'picture',
            'birthday',
            'university',
            'carrer',
            'description',
            'studing',
        )

        lable = {
            'birthday':'Fecha de nacimiento',
            'university':'Nombre de la institución',
            'carrer':'Carrera',
            'description':'Descripción',
            'studing':'Año cursante de la carrera',
        }

        widgets = {
            'birthday': DateInput(format=('%m/%d/%Y'), attrs={'placeholder':'Selecciona La Fecha', 'type':'date','class':'form-control'}),
            'university': forms.TextInput(attrs={'class':'form-control'}),
            'carrer': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'studing': forms.TextInput(attrs={'class':'form-control'}),
            'picture': forms.FileInput(attrs={'class':'form-control', 'id':'formFile'}),
        }


class ProfesorForm(forms.ModelForm):
    """Form definition for Profesor."""

    class Meta:
        """Meta definition for Profesorform."""

        model = Profesor
        fields = (
            'picture',
            'birthday',
            'university',
            'carrer',
            'description',
            'visibility',
        )

        lable = {
            'birthday': 'Fecha de nacimiento',
            'university': 'Nombre de la institución',
            'carrer': 'Carrera',
            'description': 'Descripción',
            'visibility': 'Perfil Publico',
        }
        widgets = {
            'birthday': DateInput(format=('%m/%d/%Y'), attrs={'placeholder':'Select a date', 'type':'date'}),
            'university': forms.TextInput(attrs={'class':'form-control'}),
            'carrer': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'visibility': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'picture': forms.FileInput(attrs={'class':'form-control', 'id':'formFile'}),
        }


class Pay_methodForm(forms.ModelForm):
    """Form definition for Pay_method."""

    class Meta:
        """Meta definition for Pay_methodform."""

        model = Pay_method
        fields = (
            'first_name',
            'last_name',
            'card_number',
            'card_date',
            'security_num',
        )
        exclude = ['student',]
        lable = {
            'first_name': 'Nombre del Propietario',
            'last_name': 'Apellido del Propietario',
            'card_number': 'Numero de la tarjeta',
            'card_date': 'Fecha de vencimiento',
            'security_num': 'Numero de seguridad',
        }
        widgets = {
            'card_date': DateInput(format=('%m/%d/%Y'), attrs={'placeholder':'Select a date', 'type':'date'}),
        }


class DocumentForm(forms.ModelForm):
    """Form definition for Document."""

    class Meta:
        """Meta definition for Documentform."""

        model = Document
        fields = (
            'doc_path', 
            'doc_img',
            'file_name',  
            'file_type',
            'file_desc',
            #'stu_rel',
        )
        exclude = ['stu_rel']

        widgets = {
            'doc_path': forms.FileInput(attrs={'class':'form-control', 'id':'formFile'}),
            'doc_img': forms.FileInput(attrs={'class':'form-control', 'id':'formFile'}),
            'file_name': forms.TextInput(attrs={'class':'form-control'}),
            'file_type': forms.TextInput(attrs={'class':'form-control'}),
            'file_desc': forms.Textarea(attrs={'class':'form-control'}),
            #'stu_rel': forms.HiddenInput(),
        }

class Post_fileForm(forms.ModelForm):
    """Form definition for Post_file."""

    class Meta:
        """Meta definition for Post_fileform."""

        model = Post_file
        fields = (
            'file_rel',
            'post_title',
            'post_desc'
        )
        exclude = ['is_active', 'created', 'user_rel',]

        widgets = {
            #'user_rel': forms.Select(),
            'file_rel': forms.Select(attrs={'class':'form-control'}),
            'post_title': forms.TextInput(attrs={'class':'form-control'}),
            'post_desc': forms.Textarea(attrs={'class':'form-control'}),
        }

