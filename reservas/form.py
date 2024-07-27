from django import forms
from .models import Paciente


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'ci': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'placeholder':'DD/MM/YYYY'}),
        }
    def clean(self):
        cleaned_data = super(PacienteForm, self).clean()
        user_exists = (Paciente.objects.filter(ci = cleaned_data.get('ci')).count() > 0)
        if user_exists:
            self.add_error('ci', 'El C.I. ya esta registrado')

