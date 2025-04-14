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
