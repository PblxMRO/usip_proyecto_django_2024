from rest_framework import serializers
from .models import Paciente, Medico, Horario, Area 

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'

class MedicoSerializer(serializers.ModelSerializer):
    area_trabajo = serializers.CharField(source='area.nombre', read_only=True)
    class Meta:
        model = Medico
        fields = (
           'id', 'id',
           'nombres', 'nombres',
           'apellidos', 'apellidos',
           'correo', 'correo',
           'celular', 'celular',
           'area_trabajo', 'area_trabajo',
        )

class HorarioSerializer(serializers.ModelSerializer):
    descripcion = serializers.CharField(source='__str__', read_only=True)
    class Meta:
        model = Horario
        fields = (
           'descripcion', 'descripcion',
           'ingreso', 'ingreso',
           'salida', 'salida',
        )

class ReporteHorariosSerializer(serializers.Serializer):
    cantidad = serializers.IntegerField()
    horarios = HorarioSerializer(many=True)
   