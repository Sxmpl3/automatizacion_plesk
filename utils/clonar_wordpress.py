import os

ids =  {
    "Web 1": 617,
    "Web 2": 618
}

def clonar_wordpress(subdomain_id, plantilla):
    plantilla = ids[plantilla]
    os.system(f"plesk ext wp-toolkit --clone -source-instance-id {plantilla} -target-domain-id {subdomain_id}")