import os
import requests
import urllib3
import xml.etree.ElementTree as ET

from requests.auth import HTTPBasicAuth

urllib3.disable_warnings() # Desactivar advertencias de SSL

plesk_host = 'https://server-host-performance.agenciahawkins.com:8443'

def registrar_subdominio(subdomain):
    xml_payload = f'''<?xml version="1.0" encoding="UTF-8"?>
<packet>
    <subdomain>
        <add>
            <parent>herasoft.ai</parent>
            <name>{subdomain}</name>
            <property>
                <name>www_root</name>
                <value>{subdomain}</value>
            </property>
            <property>
                <name>ssi</name>
                <value>true</value>
            </property>
        </add>
    </subdomain>
</packet>'''

    headers = {
        "Content-Type": "text/xml",
        "HTTP_AUTH_LOGIN": "root", 
        "HTTP_AUTH_PASSWD": "!KwP&8&9D1"
    }

    response = requests.post(
        f"{plesk_host}/enterprise/control/agent.php",
        data=xml_payload.encode("utf-8"),
        headers=headers,
        verify=False
    )

    # Parseamos el XML para obtener el ID del subdominio creado
    root = ET.fromstring(response.text)
    try:
        subdomain_id = root.find('.//id').text
        print(f"✅ Subdominio creado con ID: {subdomain_id}")

        return subdomain_id
    except AttributeError:
        print("❌ No se pudo extraer el ID del subdominio.")
        print(response.text)

        return None

def instalar_ssl(dominio):
    os.system(f"""plesk bin extension --exec letsencrypt cli.php \
      -d {dominio}.herasoft.ai \
      -d www.{dominio}.herasoft.ai \
      -m dani.mefle@lchawkins.com \
      --agree-tos
    """)
