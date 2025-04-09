from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.db import connection
from django.conf import settings
import os
import json
from .models import UDN



class HelloWorldView(View):
    def get(self, request):
        # Obtener información de la base de datos
        try:
            db_info = {
                'db_name': connection.settings_dict['NAME'],
                'db_host': connection.settings_dict['HOST'],
                'db_port': connection.settings_dict['PORT'],
                'db_user': connection.settings_dict['USER'],
                'db_engine': connection.settings_dict['ENGINE'],
                'db_options': connection.settings_dict.get('OPTIONS', {}),
            }
            db_status = "Conectada"
        except Exception as e:
            db_info = {
                'error': str(e)
            }
            db_status = "Error de conexión"
        
        # Obtener UDNs de la base de datos con información detallada
        try:
            udns = UDN.objects.prefetch_related('permission_group', 'groups').all()
            udns_list = []
            for udn in udns:
                permission_groups = [group.name for group in udn.permission_group.all()]
                associated_groups = [group.name for group in udn.groups.all()]
                udn_info = f"""
                - {udn.name}
                  Grupos de Permisos: {', '.join(permission_groups) if permission_groups else 'Ninguno'}
                  Grupos Asociados: {', '.join(associated_groups) if associated_groups else 'Ninguno'}
                """
                udns_list.append(udn_info)
            udns_text = "\n".join(udns_list) if udns_list else "No hay UDNs registradas"
            udns_count = len(udns_list)
        except Exception as e:
            udns_text = f"Error al obtener UDNs: {str(e)}"
            udns_count = 0
        
        # Obtener el valor de PING del secreto
        ping_secret = os.getenv('PING', '{}')
        try:
            ping_data = json.loads(ping_secret)
            ping_value = ping_data.get('PING', 'No disponible')
        except json.JSONDecodeError:
            ping_value = 'Error al decodificar el secreto'
        
        # Construir respuesta
        response = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                pre {{ background-color: #f5f5f5; padding: 10px; border-radius: 5px; }}
                h1, h2 {{ color: #333; }}
                .status-ok {{ color: green; }}
                .status-error {{ color: red; }}
            </style>
        </head>
        <body>
            <h1>Hello World</h1>
            
            <h2>Información de la Base de Datos:</h2>
            <pre>
            {'Error: ' + db_info.get('error', '') if 'error' in db_info else f'''
            Nombre: {db_info['db_name']}
            Host: {db_info['db_host']}
            Puerto: {db_info['db_port']}
            Usuario: {db_info['db_user']}
            Motor: {db_info['db_engine']}
            Opciones: {db_info['db_options']}
            '''}
            </pre>
            
            <h2>UDNs en la Base de Datos ({udns_count}):</h2>
            <pre>{udns_text}</pre>
            
            <h2>Valor de PING:</h2>
            <pre>{ping_value}</pre>
            
            <h2>Estado del Sistema:</h2>
            <pre>
            Base de datos: <span class="{'status-ok' if db_status == 'Conectada' else 'status-error'}">{db_status}</span>
            Modo: {settings.DEBUG and 'Desarrollo' or 'Producción'}
            Django: {settings.DJANGO_VERSION}
            </pre>
        </body>
        </html>
        """
        
        return HttpResponse(response)
