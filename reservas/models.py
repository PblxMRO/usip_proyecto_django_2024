from django.db import models
from .validators import validar_letras, validar_correo_coorporativo, validar_mayusculas

# Create your models here.

class sexo(models.TextChoices):
    MASCULINO = 'M', 'Masculino'
    FEMENINO = 'F', 'Femenino'

class tiempo(models.IntegerChoices):
    DIEZ = 10, '10 minutos'
    QUINCE = 15, '15 minutos'
    VEINTE = 20, '20 minutos'
    TREINTA = 30, '30 minutos'
    
class dia(models.IntegerChoices):
    LUNES = 1, 'Lunes'
    MARTES = 2, 'Martes'
    MIERCOLES = 3, 'Miercoles'
    JUEVES = 4, 'Jueves'
    VIERNES = 5, 'Viernes'
    SABADO = 6, 'Sabado'
    DOMINGO = 7, 'Domingo'

class Area(models.Model):
    nombre = models.CharField(max_length=100, unique=True, validators=[validar_letras, validar_mayusculas])
    estado = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "area"
        verbose_name_plural = "areas"
        db_table = "areas"
    
    def __str__(self):
       return  self.nombre

class Medico(models.Model):
    nombres = models.CharField(max_length=30, validators=[validar_letras])
    apellidos = models.CharField(max_length=50, validators=[validar_letras])
    correo = models.EmailField(unique=True, validators=[validar_correo_coorporativo])
    celular = models.CharField(max_length=12)
    sexo = models.CharField(max_length=1, choices=sexo.choices)
    area = models.ForeignKey(Area, on_delete=models.RESTRICT)
    consultorio = models.CharField(max_length=10)
    planta = models.SmallIntegerField()
    estado = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
    
    class Meta:
        verbose_name = "medico"
        verbose_name_plural = "medicos"
        ordering = ['-created']
        db_table = "medicos"

    def __str__(self):
        text = "Dr." if self.sexo == 'M' else "Dra."
        return f'{text} {self.nombres} {self.apellidos}'

class Horario(models.Model):
    medico =models.ForeignKey(Medico, on_delete=models.CASCADE)
    lunes = models.BooleanField(default=False)
    martes = models.BooleanField(default=False)
    miercoles = models.BooleanField(default=False)
    jueves = models.BooleanField(default=False)
    viernes = models.BooleanField(default=False)
    sabado = models.BooleanField(default=False)
    domingo = models.BooleanField(default=False)
    ingreso = models.TimeField(verbose_name="Hora de ingreso")
    salida = models.TimeField(verbose_name="Hora de salida")
    tiempo_consulta = models.IntegerField(choices=tiempo.choices) 
    estado = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        db_table = "horarios"

    def __str__(self):
        return f'{self.medico.area} - {self.medico}'    
    
class Paciente(models.Model):
    nombres = models.CharField(max_length=30, validators=[validar_letras])
    apellidos = models.CharField(max_length=50, validators=[validar_letras])
    sexo = models.CharField(max_length=1, choices=sexo.choices)
    ci = models.CharField(max_length=15, unique=True)
    correo = models.EmailField(unique=True)
    celular = models.CharField(max_length=12)
    fecha_nacimiento = models.DateField()
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
        
    class Meta:
        verbose_name = "paciente"
        verbose_name_plural = "pacientes"
        db_table = "pacientes"
       
    def __str__(self):
       return  self.nombres + ' ' + self.apellidos

class Cita(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.RESTRICT)
    paciente = models.ForeignKey(Paciente, on_delete=models.RESTRICT)
    dia = models.IntegerField(choices=dia.choices)
    fecha = models.DateField()
    hora = models.TimeField()
    numero_ficha = models.SmallIntegerField()
    estado = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")
    
    class Meta:
        verbose_name = "cita"
        verbose_name_plural = "citas"
        db_table = "citas"
    
    def __str__(self):
       return  f'Paciente: {self.paciente.nombres} {self.paciente.apellidos} - Médico: {self.medico} - Area: {self.medico.area}'  

