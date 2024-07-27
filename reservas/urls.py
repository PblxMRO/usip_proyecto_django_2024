from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/pacientes', views.PacientesViewSet)
router.register(r'api/areas', views.AreasViewSet)

urlpatterns = [
    path('app/', views.inicio, name='inicio'),
    path('areas/', views.areas, name='areas'),
    path('medicos/', views.medicos, name='medicos'),
    path('horarios/', views.horarios, name='horarios'),
    path('pacientes/', views.pacientes, name='pacientes'),
    path('citas/', views.citas, name='citas'),
    path('', include(router.urls)),
    path('api/medicos/listar/', views.MedicosCreateView.as_view()),
    path('api/citas/reporte/', views.total_reservas),
    path('api/horarios/reporte/', views.reporte_horarios),
]