import os

def clonar_wordpress(dominio, plantilla):
    dominio = dominio + ".hawkins.es"

    os.system(f"rm -rf /var/www/vhosts/hawkins.es/{dominio}")

    os.system(f"""
        rsync -avz \
        /var/www/vhosts/hawkins.es/{plantilla}/ \
        /var/www/vhosts/hawkins.es/{dominio}/
    """)