"""
URL configuration for Pasteleria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Vistas import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

        # URL para la página de inicio
    path('', views.inicio, name='inicio'),
    path('obtener_descripcion_pastel/', views.obtener_descripcion_pastel, name='obtener_descripcion_pastel'),
    path('obtener_ingredientes_pastel/', views.obtener_ingredientes_pastel, name='obtener_ingredientes_pastel'),
    path('obtener_pasteles_disponibles/', views.obtener_pasteles_disponibles, name='obtener_pasteles_disponibles'),
    path('cocinar_pastel/', views.cocinar_pastel, name='cocinar_pastel'),
    path('aplicar_rebaja/', views.aplicar_rebaja, name='aplicar_rebaja'),

    path('procesar_pedido/', views.procesar_pedido, name='procesar_pedido'),
    path('control_precio/', views.control_precio, name='control_precio'),
    path('realizar_pedido/', views.realizar_pedido, name='realizar_pedido'),
    # Definir más URL según tus vistas
]