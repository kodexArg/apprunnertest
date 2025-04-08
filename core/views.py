from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
# from django.contrib.auth.models import User
# from django.db import connection
import os



class HelloWorldView(View):
    def get(self, request):
        # # Obtener información de la base de datos
        # db_info = {
        #     'db_name': connection.settings_dict['NAME'],
        #     'db_host': connection.settings_dict['HOST'],
        #     'db_port': connection.settings_dict['PORT'],
        #     'db_user': connection.settings_dict['USER'],
        # }
        
        # # Obtener usuarios de la base de datos
        # users = User.objects.all()
        # users_list = "\n".join([f"- {user.username} ({user.email})" for user in users])
        
        # # Obtener el valor de PING
        ping_value = os.getenv('PING', 'No disponible')
        
        # Construir respuesta
        response = f"""
        <h1>Hello World</h1>
        
        <h2>Valor de PING:</h2>
        <pre>{ping_value}</pre>
        
        <h2>Estado del Sistema:</h2>
        <pre>
        Base de datos: Deshabilitada temporalmente
        Modo: Desarrollo
        </pre>
        """
        
        return HttpResponse(response)
