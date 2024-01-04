# comanda_app/urls.py
from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrar_cliente/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('comandas/', views.clientes, name='clientes'),
    path('cadastrar_produto/', views.cadastrar_produto, name='cadastrar_produto'),
    path('associar_produto/<int:cliente_id>/', views.associar_produto, name='associar_produto'),
    path('produtos/', views.listar_produtos, name='listar_produtos'),
    path("delete/<cliente_id>/", views.delete, name="delete"),
    path("comanda_individual/<int:cliente_id>/", views.comanda_individual, name="comanda_individual"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)