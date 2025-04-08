from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db import connection

# Create your views here.

class HelloWorldView(View):
    def get(self, request):
        # Obtener información de la base de datos
        db_info = {
            'db_name': connection.settings_dict['NAME'],
            'db_host': connection.settings_dict['HOST'],
            'db_port': connection.settings_dict['PORT'],
            'db_user': connection.settings_dict['USER'],
        }
        
        # Obtener usuarios de la base de datos
        users = User.objects.all()
        users_list = "\n".join([f"- {user.username} ({user.email})" for user in users])
        
        # Construir respuesta
        response = f"""
        <h1>Hello World</h1>
        
        <h2>Información de la Base de Datos:</h2>
        <pre>
        Nombre: {db_info['db_name']}
        Host: {db_info['db_host']}
        Puerto: {db_info['db_port']}
        Usuario: {db_info['db_user']}
        </pre>
        
        <h2>Usuarios en la Base de Datos:</h2>
        <pre>{users_list}</pre>
        """
        
        return HttpResponse(response)
