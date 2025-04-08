import re

from flask import Flask, request, jsonify
from utils.registrar_dominio import registrar_subdominio, instalar_ssl
from utils.clonar_wordpress import clonar_wordpress

app = Flask(__name__)  # Inicializar la app

def valid_domain(domain):
    patron = r'^https:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}$'
    return re.match(patron, domain) is not None

@app.route('/', methods=['POST'])
def handle_post():
    try:
        data = request.get_json()
        domain = data.get('domain')
        template = data.get('template')

        if not domain or not valid_domain(domain):
            return jsonify({
                'status': 'error',
                'message': 'Dominio no válido, usa formato https://tudominio.com'
            }), 400
        
                
        registrar_subdominio(domain)
        instalar_ssl(domain)
        clonar_wordpress(domain, template)

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
    app.run(host='0.0.0.0', port=9000, debug=True)
