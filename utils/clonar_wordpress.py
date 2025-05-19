import os

def clonar_wordpress(subdomain_id, plantilla):
    os.system(f"plesk ext wp-toolkit --clone -source-instance-id {plantilla} -target-domain-id {subdomain_id}")