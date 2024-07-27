from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
from urllib.parse import urlencode
from django.contrib import messages
import json
from rest_framework import viewsets, generics
from .serializers import PacienteSerializer, MedicoSerializer, ReporteHorariosSerializer, AreaSerializer
from .models import Horario, Area, Medico, Cita, Paciente
from .form import PacienteForm
from rest_framework.decorators import api_view

# Create your views here.

def inicio(request):
    return render(request, "principal.html")

def areas(request):
    if request.method == 'POST':
        post_nombre = request.POST.get("nombre")
        if post_nombre:
            q = Area(nombre=post_nombre)
            q.save()
        items = Area.objects.all()
        return render(request, 'areas.html' , {"areas": items, "mensaje":"Registro creado correctamente"})
    else:    
        items = Area.objects.all()
        return render(request, "areas.html", {"areas": items})

def medicos(request):
    filtro_area_id = request.POST.get("area_id")
    if filtro_area_id:
        medicos = list(Medico.objects.filter(area_id=int(filtro_area_id)).values('id', 'nombres', 'apellidos'))
        return HttpResponse(json.dumps(medicos), content_type="application/json") 
    else:    
        items = Medico.objects.all()
        return render(request, "medicos.html", {"medicos": items})

def horarios(request):
    areas = Area.objects.all()
    items = Horario.objects.all().select_related('medico') 
    fichas_atencion =[]
    for item in items: 
        d1 = item.ingreso
        d2 = item.salida  
        total_sec1 = d1.hour * 3600 + d1.minute * 60 + d1.second
        total_sec2 = d2.hour * 3600 + d2.minute * 60 + d2.second
        fichas_atencion.append(f"{((total_sec2-total_sec1)//60)//item.tiempo_consulta}")

    context = {
        'horarios': zip(items,fichas_atencion), 'areas': areas
    }    
    return render(request, 'horarios.html', context)

def pacientes(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente =form.save()
            paciente_id = paciente.id
            parameters = urlencode({'id': paciente_id})
            url = f'/reservas/pacientes/?{parameters}'
            return HttpResponseRedirect(url)
        else:
          for error in form.errors:
            messages.error(request, form.errors[error])
        """    messages.error(request,'El registro ya existe') """
    else:
        form = PacienteForm()      
    filtro_id = request.GET.get("id")    
    if filtro_id:
       item = Paciente.objects.get(id=filtro_id)
       edad = relativedelta(datetime.now(), item.fecha_nacimiento)
       context= {
        'mensaje':'Registro guardado correctamente',
        'paciente':item,
        'edad':edad.years,
        'form': form
        }
       return render(request, 'pacientes.html', context)
    filtro_buscar = request.GET.get("buscar")
    if filtro_buscar:
       items = Paciente.objects.filter(apellidos__contains=filtro_buscar)
       edades_list=[]
       for item in items:
            edad = relativedelta(datetime.now(), item.fecha_nacimiento)
            edades_list.append(edad.years)
       context = {
            'pacientes': zip(items,edades_list), "form": form
        }     
       return render(request, "pacientes.html", context)
    else:      
       return render(request, "pacientes.html",  {"form": form})

def citas(request):
    if request.method == 'POST':
        post_dia = request.POST.get("diaIdCita")
        post_fecha = request.POST.get("fechaCita")
        post_hora = request.POST.get("horaCita")
        post_ficha = request.POST.get("fichaCita")
        post_medicoId = request.POST.get("medIdCita")
        post_pacienteId = request.POST.get("pacienteIdCita")
        if post_dia and post_fecha and post_hora and post_ficha and post_medicoId and post_pacienteId:
            time_str = post_hora.strip()
            parsed_time = datetime.strptime(time_str,'%H:%M')
            cita= Cita(dia=post_dia, fecha=post_fecha, hora=parsed_time, numero_ficha=post_ficha, paciente_id=post_pacienteId, medico_id=post_medicoId)
            cita.save()
            fecha_actual = datetime.now()
            inicio_proxima_semana = fecha_actual + timedelta(days=(7 - fecha_actual.weekday()))
            fechas_proxima_semana =[inicio_proxima_semana + timedelta(days=i) for i in range(7)]
            reservas =  Cita.objects.filter(medico_id=int(post_medicoId)).filter(fecha__range=[fechas_proxima_semana[0], fechas_proxima_semana[6]]).filter(estado=True)
            items = Horario.objects.filter(medico_id=int(post_medicoId)).select_related('medico') 
            fichas_list=[]
            for item in items:
                ficha_hora =[]
                d1 = item.ingreso  
                d2 = item.salida  
                total_sec1 = d1.hour * 3600 + d1.minute * 60 + d1.second
                total_sec2 = d2.hour * 3600 + d2.minute * 60 + d2.second
                fichas = ((total_sec2-total_sec1)//60)//item.tiempo_consulta
                d3= timedelta(hours=d1.hour, minutes=d1.minute)
                ficha_hora.append(f"{str((d3.seconds // 3600)).zfill(2)}:{str((d3.seconds % 3600) // 60).zfill(2)}")
                for i in range(fichas-1):
                    d2 = timedelta(minutes=item.tiempo_consulta)
                    d3 = d3 + d2
                    ficha_hora.append(f"{str((d3.seconds // 3600)).zfill(2)}:{str((d3.seconds % 3600) // 60).zfill(2)}")
                fichas_list.append(ficha_hora)        
            context = {
                'horarios': zip(items,fichas_list), 'fechas': fechas_proxima_semana, 'reservas': reservas, 'mensaje':'Registro guardado correctamente'
            }        
            return render(request, 'citas.html', context)
    filtro_ci = request.GET.get("ci")   
    filtro_medId = request.GET.get("medId")     
    if filtro_ci and filtro_medId:
       paciente = Paciente.objects.get(ci=filtro_ci)
       fecha_actual = datetime.now()
       inicio_proxima_semana = fecha_actual + timedelta(days=(7 - fecha_actual.weekday()))
       fechas_proxima_semana =[inicio_proxima_semana + timedelta(days=i) for i in range(7)]
       reservas =  Cita.objects.filter(medico_id=int(filtro_medId)).filter(fecha__range=[fechas_proxima_semana[0], fechas_proxima_semana[6]]).filter(estado=True)
       items = Horario.objects.filter(medico_id=int(filtro_medId)).select_related('medico') 
       fichas_list=[]
       for item in items:
            ficha_hora =[]
            d1 = item.ingreso  
            d2 = item.salida  
            total_sec1 = d1.hour * 3600 + d1.minute * 60 + d1.second
            total_sec2 = d2.hour * 3600 + d2.minute * 60 + d2.second
            fichas = ((total_sec2-total_sec1)//60)//item.tiempo_consulta
            d3= timedelta(hours=d1.hour, minutes=d1.minute)
            ficha_hora.append(f"{str((d3.seconds // 3600)).zfill(2)}:{str((d3.seconds % 3600) // 60).zfill(2)}")
            for i in range(fichas-1):
                d2 = timedelta(minutes=item.tiempo_consulta)
                d3 = d3 + d2
                ficha_hora.append(f"{str((d3.seconds // 3600)).zfill(2)}:{str((d3.seconds % 3600) // 60).zfill(2)}")
            fichas_list.append(ficha_hora)        
       context = {
            'horarios': zip(items,fichas_list), 'fechas': fechas_proxima_semana, 'reservas': reservas, 'paciente':paciente
        }        
       return render(request, "citas.html",  context)
    filtro_medico_id = request.GET.get("medico_id")
    if filtro_medico_id:  
        fecha_actual = datetime.now()
        inicio_proxima_semana = fecha_actual + timedelta(days=(7 - fecha_actual.weekday()))
        fechas_proxima_semana =[inicio_proxima_semana + timedelta(days=i) for i in range(7)]
        reservas =  Cita.objects.filter(medico_id=int(filtro_medico_id)).filter(fecha__range=[fechas_proxima_semana[0], fechas_proxima_semana[6]]).filter(estado=True)
        items = Horario.objects.filter(medico_id=int(filtro_medico_id)).select_related('medico') 
        fichas_list=[]
        for item in items:
            ficha_hora =[]
            d1 = item.ingreso  
            d2 = item.salida  
            total_sec1 = d1.hour * 3600 + d1.minute * 60 + d1.second
            total_sec2 = d2.hour * 3600 + d2.minute * 60 + d2.second
            fichas = ((total_sec2-total_sec1)//60)//item.tiempo_consulta
            d3= timedelta(hours=d1.hour, minutes=d1.minute)
            ficha_hora.append(f"{str((d3.seconds // 3600)).zfill(2)}:{str((d3.seconds % 3600) // 60).zfill(2)}")
            for i in range(fichas-1):
                d2 = timedelta(minutes=item.tiempo_consulta)
                d3 = d3 + d2
                ficha_hora.append(f"{str((d3.seconds // 3600)).zfill(2)}:{str((d3.seconds % 3600) // 60).zfill(2)}")
            fichas_list.append(ficha_hora)        
        context = {
            'horarios': zip(items,fichas_list), 'fechas': fechas_proxima_semana, 'reservas': reservas
        }        
        return render(request, "citas.html",  context)
    

class AreasViewSet(viewsets.ModelViewSet):
    queryset =  Area.objects.all()
    serializer_class = AreaSerializer

class PacientesViewSet(viewsets.ModelViewSet):
    queryset =  Paciente.objects.all()
    serializer_class = PacienteSerializer

class MedicosCreateView(generics.CreateAPIView, generics.ListAPIView):
    queryset =  Medico.objects.all()
    serializer_class = MedicoSerializer
    http_method_names = ['get']

@api_view(["GET"])
def total_reservas(request):
    
    """ Muestra el total de reservas para citas de la proxima semana """
    try:
        fecha_actual = datetime.now()
        inicio_proxima_semana = fecha_actual + timedelta(days=(7 - fecha_actual.weekday()))
        fechas_proxima_semana =[inicio_proxima_semana + timedelta(days=i) for i in range(7)]
        reservas =  Cita.objects.filter(fecha__range=[fechas_proxima_semana[0], fechas_proxima_semana[6]]).filter(estado=True).count()  
        return JsonResponse({"total_reservas":reservas} ,safe=False, status=200)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=400)
        
@api_view(["GET"])
def reporte_horarios(request):
    
    """ Muestra el total de reservas para citas de la proxima semana """
    try:
        horarios = Horario.objects.all()
        cantidad = horarios.count()
        return JsonResponse(
            ReporteHorariosSerializer({
                "cantidad": cantidad,
                "horarios": horarios
            }).data,
            safe=False,
            status=200,
        )
    except Exception as e:
        return JsonResponse(
            {
                "error": str(e)
            },
            safe=False,
            status=400
        )
    



