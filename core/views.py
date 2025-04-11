from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.db import connection
from django.conf import settings
import os
import json
import django
import logging
from .models import UDN

logger = logging.getLogger(__name__)


class HelloWorldView(View):
    def get(self, request):
        return HttpResponse("Hello World")


class PingView(View):
    def get(self, request):
        ping_secret = os.getenv('PING', '{}')
        try:
            ping_data = json.loads(ping_secret)
            ping_value = ping_data.get('PING', 'Pong')
            return HttpResponse(ping_value)
        except json.JSONDecodeError:
            return HttpResponse("Pong")


class DbView(View):
    def get(self, request):
        logger.info("Iniciando verificación de conexión a base de datos")
        try:
            logger.debug("Intentando establecer conexión con la base de datos")
            with connection.cursor() as cursor:
                logger.debug("Conexión establecida, ejecutando consulta de prueba")
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                logger.info(f"Consulta de prueba exitosa. Resultado: {result}")
                
                # Obtener información de la conexión
                db_settings = connection.settings_dict
                logger.debug(f"Configuración de base de datos: {db_settings}")
                
                # Verificar si hay UDNs en la base de datos
                udn_count = UDN.objects.count()
                logger.info(f"Número de UDNs en la base de datos: {udn_count}")
                
            # Obtener la variable DJANGO_SECRET_KEY
            django_secret_key = os.getenv('DJANGO_SECRET_KEY', 'No disponible')
            secret_key_source = "apprunner.yaml (secrets)"
                
            response = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    pre {{ background-color: #f5f5f5; padding: 10px; border-radius: 5px; }}
                    .secret-info {{ margin-top: 20px; }}
                </style>
            </head>
            <body>
                <h2>Estado de la Base de Datos:</h2>
                <pre>Conectado</pre>
                
                <div class="secret-info">
                    <h2>DJANGO_SECRET_KEY:</h2>
                    <pre>Valor: {django_secret_key}
Origen: {secret_key_source}</pre>
                </div>
            </body>
            </html>
            """
            return HttpResponse(response)
        except Exception as e:
            logger.error(f"Error al conectar con la base de datos: {str(e)}", exc_info=True)
            return HttpResponse(f"Error: {str(e)}")


class DatabaseInfoView(View):
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                db_version = cursor.fetchone()[0]
            
            db_info = {
                'db_name': connection.settings_dict.get('NAME', 'No disponible'),
                'db_host': connection.settings_dict.get('HOST', 'No disponible'),
                'db_port': connection.settings_dict.get('PORT', 'No disponible'),
                'db_user': connection.settings_dict.get('USER', 'No disponible'),
                'db_engine': connection.settings_dict.get('ENGINE', 'No disponible'),
                'db_options': connection.settings_dict.get('OPTIONS', {}),
                'db_version': db_version,
                'connection_string': os.getenv('WELPDESK_DB_CONNECTOR', 'No disponible')
            }
            db_status = "Conectada"
        except Exception as e:
            db_info = {
                'error': str(e),
                'connection_string': os.getenv('WELPDESK_DB_CONNECTOR', 'No disponible')
            }
            db_status = "Error de conexión"
        
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
            Versión: {db_info['db_version']}
            Opciones: {db_info['db_options']}
            Cadena de conexión: {db_info['connection_string']}
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
            Django: {django.get_version()}
            </pre>
        </body>
        </html>
        """
        
        return HttpResponse(response)
