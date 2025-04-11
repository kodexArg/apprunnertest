from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
import os
import json
import django
import logging
from django.db import connection
from django.conf import settings
from .models import UDN

logger = logging.getLogger(__name__)


class HelloWorldView(View):
    def get(self, request):
        return render(request, 'home.html')


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
                
                # Verificar si hay UDNs en la base de datos
                udn_count = UDN.objects.count()
                logger.info(f"Número de UDNs en la base de datos: {udn_count}")
                
            response = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    pre {{ background-color: #f5f5f5; padding: 10px; border-radius: 5px; }}
                </style>
            </head>
            <body>
                <h2>Estado de la Base de Datos:</h2>
                <pre>Conectado</pre>
                
                <h2>Información General:</h2>
                <pre>Número de UDNs: {udn_count}</pre>
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
                'db_engine': connection.settings_dict.get('ENGINE', 'No disponible'),
                'db_version': db_version,
            }
            db_status = "Conectada"
        except Exception as e:
            db_info = {
                'error': str(e),
            }
            db_status = "Error de conexión"
        
        try:
            udns_count = UDN.objects.count()
        except Exception as e:
            udns_count = 0
        
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
            <h1>Información del Sistema</h1>
            
            <h2>Información de la Base de Datos:</h2>
            <pre>
            {'Error: ' + db_info.get('error', '') if 'error' in db_info else f'''
            Motor: {db_info['db_engine']}
            Versión: {db_info['db_version']}
            '''}
            </pre>
            
            <h2>UDNs en la Base de Datos:</h2>
            <pre>Total: {udns_count}</pre>
            
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
