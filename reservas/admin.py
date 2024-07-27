from django.contrib import admin

# Register your models here.
from .models import Area, Medico, Horario, Paciente,Cita

class HorarioAdmin(admin.ModelAdmin):
    fields = ["medico",("lunes", "martes","miercoles","jueves","viernes"), ("sabado","domingo"), "ingreso","salida","tiempo_consulta","estado"]

class MedicoAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
         "correo",
        "celular",
        "area",
        "planta",
        "consultorio",
    )
    list_filter = (
        "area",
        "planta",
        "estado",
    )
    search_fields = ("apellidos",)
    ordering = ("apellidos",)


# Register your models here.
admin.site.register(Area)
admin.site.register(Medico, MedicoAdmin)
admin.site.register(Horario, HorarioAdmin)
admin.site.register(Paciente)


