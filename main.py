import time

from flask import Flask, request, jsonify
from utils.registrar_ionos import login, create_subdomain, change_dns
from utils.registrar_dominio import registrar_subdominio, instalar_ssl
from utils.clonar_wordpress import clonar_wordpress

app = Flask(__name__)  # Inicializar la app

@app.route('/', methods=['POST'])
def handle_post():
    try:
        data = request.get_json()
        domain = data.get('domain')
        template = data.get('template')

        driver = login()
        create_subdomain(driver, domain)
        time.sleep(900)
        change_dns(driver, domain)

        subdomain_id = registrar_subdominio(domain)
        instalar_ssl(domain)
        clonar_wordpress(subdomain_id, template)

        return jsonify({
            'status': 'success',
            'message': 'Dominio añadido a plesk y plantilla clonada correctamente'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error en el servidor: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8787, debug=True)
