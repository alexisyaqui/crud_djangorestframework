from django.urls import path
from node_api.views import Notas, NotaDetalle

urlpatterns = [
    path('', Notas.as_view()),
    path('<str:pk>', NotaDetalle.as_view())
]