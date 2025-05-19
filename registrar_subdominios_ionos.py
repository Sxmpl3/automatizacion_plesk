import time
import requests
import threading
import tkinter as tk
from tkinter import messagebox

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

url = "https://my.ionos.es/subdomains/herasoft.ai?linkId=ct.tab.domainlist.subdomains"

# Usuario y contraseña de IONOS
user = "i-pointsite.com"
passwd = "R4t420223!"

ids = {
    "Web 1": 631,  # maquetacionweb1.hawkins.es
    "Web 2": 674,  # maquetacionweb02.hawkins.es
    "Web 3": 635,  # maquetacionweb03.hawkins.es
    "Web 4": 634,  # maquetacionweb04.hawkins.es
    "Web 5": 671,  # maquetacionweb05.hawkins.es
    "Web 6": 712,  # maquetacion6.hawkins.es
    "Web 7": 669,  # maquetacionweb06.hawkins.es
    "Web 8": 677,  # maquetacionweb07.hawkins.es
    "Web 9": 678,  # maquetacionweb08.hawkins.es

    "Eccommerce 1": 617,  # maquetacion1.hawkins.es
    "Eccommerce 2": 618,  # maquetacion2.hawkins.es
    "Eccommerce 3": 620,  # maquetacion3.hawkins.es
    "Eccommerce 4": 623,  # maquetacion4.hawkins.es
    "Eccommerce 5": 619,  # maquetacion5.hawkins.es
    "Eccommerce 6": 712,  # maquetacion6.hawkins.es
    "Eccommerce 7": 626,  # maquetacion7.hawkins.es
    "Eccommerce 8": 627,  # maquetacion8.hawkins.es
}

def login():
    options = Options()
    options.add_argument('--headless')  # Ejecutar en modo headless
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage') 

    driver = webdriver.Chrome()
    driver.get(url)

    # Ingresamos usuarios y le damos a continuar
    campo_email =  WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'username'))
    )
    campo_email.send_keys(user)

    button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'button--with-loader'))
    )
    button.click()

    # Ingresamos contraseña y le damos a continuar

    campo_password =  WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'password'))
    )
    campo_password.send_keys(passwd)

    button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'button--with-loader'))
    )
    button.click()

    return driver

def create_subdomain(driver, domain):
    # Espera a que el botón de crear subdominio esté presente y haz clic
    create_subdomain_button = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "tableheader.addSubdomain"))
    )
    create_subdomain_button.click()

    iframe = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    )
    driver.switch_to.frame(iframe)

    # Si el modal está presente, interactúa con el campo de texto para el subdominio
    subdomain_text = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "createSubdomain"))
    )
    subdomain_text.send_keys(f"{domain}")

    # Interactúa con el botón de enviar
    submit_btn = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "button.createSubdomain"))
    )
    submit_btn.click()

    print("Subdominio creado con éxito.")
    
def change_dns(driver, domain):
    try:
        url_dns = f"https://my.ionos.es/domain-dns-settings/herasoft.ai?linkId=ct.tab.domainlist.dns&from=subdomains%2Fherasoft.ai&filter.host={domain}.herasoft.ai&page.sort=service%2Casc&page.size=10&page.page=0"

        driver.get(url_dns)

        # Esperar que el select sea visible (no solo presente)
        select_element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "table-filter-property"))
        )

        # Usar Select para interactuar con opciones
        select = Select(select_element)
        for option in select.options:
            if option.get_attribute("value") == f"{domain}.herasoft.ai":
                option.click()
            break

        links = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'link'))
        )
        
        for link in links:
            if link.text == "A":
                link.click()
                break

        # Cambiar IP del DNS
        change_dns = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "recordValue"))
        )
        change_dns.clear()
        change_dns.send_keys("82.223.118.182")

        try:
            www_record = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "toggle-record-for-www"))
            )
            if www_record.text() == "Editar registro DNS para www":
                www_record.click()

            save_changes = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "button-primary"))
            )
            save_changes.click()

            try:
                save_changes = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "button-primary"))
                )
                save_changes.click()
            except:
                pass
        except:
            save_changes = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "button-primary"))
            )
            save_changes.click()

            driver.get("https://my.ionos.es/add-dns-record/herasoft.ai?record.type=A&linkId=ct.txt.dns.add-record.type-A")

            input_domain = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "recordHost"))
            )
            input_domain.clear()
            input_domain.send_keys(f"www.{domain}")

            # Cambiar IP del DNS
            change_dns = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "recordValue"))
            )
            change_dns.clear()
            change_dns.send_keys("82.223.118.182")

            save_changes = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "button-primary"))
            )
            save_changes.click()
            

            try:
                save_changes = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "button-primary"))
                )
                save_changes.click()
            except:
                pass

    except Exception as e:
        print(f"Error al cambiar el DNS: {e}")

def wait_for_http(domain, timeout=600):
    url = f"http://{domain}.herasoft.ai"
    print(f"Esperando a que {domain}.herasoft.ai esté disponible vía HTTP...")
    for _ in range(timeout):
        try:
            r = requests.get(url, timeout=5)
            if r.status_code in [200, 301, 302]:
                print(f"{domain}.herasoft.ai responde correctamente.")
                return True
        except:
            pass
        time.sleep(1)
    print(f"{domain}.herasoft.ai no respondió en el tiempo esperado.")
    return False

def clone_web(template_id, domain):
    data = {
        "domain": domain,
        "template": template_id,
    }

    try:
        requests.post("https://conversacioneshera.hawkins.es/api/proxy.php", json=data, timeout=600)
    except requests.exceptions.Timeout:
        print("La solicitud tardó demasiado y fue cancelada.")
    except Exception as e:
        print("Error al enviar la solicitud:", e)

def run_process(domain, template_id, status_label, root):
    try:
        status_label.config(text="Iniciando sesión en IONOS...")
        driver = login()
        status_label.config(text="Creando subdominio...")
        create_subdomain(driver, domain)

        wait_time = 600
        for i in range(wait_time, 0, -1):
            minutos = i // 60
            segundos = i % 60
            status_label.config(
                text=f"Esperando {minutos}:{segundos:02d} minutos a que aparezca el subdominio en Ionos..."
            )
            root.update()
            time.sleep(1)

        status_label.config(text="Cambiando DNS...")
        change_dns(driver, domain)
        status_label.config(text="Subdominio creado y DNS cambiados con éxito.")
        driver.quit()
        messagebox.showinfo("Éxito", "Subdominio creado y DNS cambiados con éxito.")

        bool_http = wait_for_http(domain)

        if bool_http:
            try:
                clone_web(template_id, domain)
                messagebox.showinfo("Éxito", "Plantilla clonada con éxito.")
                time.sleep(5)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "El subdominio no está disponible vía HTTP.")

    except Exception as e:
        status_label.config(text=f"Error: {e}")
        messagebox.showerror("Error", str(e))
        driver.quit()

def start_process(entry, selected_template, status_label, root):
    domain = entry.get().strip()
    template_name = selected_template.get()

    if not domain:
        messagebox.showwarning("Advertencia", "Introduce un subdominio.")
        return
    if not template_name:
        messagebox.showwarning("Advertencia", "Selecciona una plantilla.")
        return

    template_id = ids[template_name]
    thread = threading.Thread(target=run_process, args=(domain, template_id, status_label, root))
    thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Registrar subdominio IONOS")
    root.geometry("500x250")

    tk.Label(root, text="Introduce el subdominio (ej: testsubdomain):").pack(pady=5)
    entry = tk.Entry(root, width=30)
    entry.pack(pady=5)

    tk.Label(root, text="Selecciona una plantilla:").pack(pady=5)
    selected_template = tk.StringVar()
    template_menu = tk.OptionMenu(root, selected_template, *ids.keys())
    template_menu.pack(pady=5)

    status_label = tk.Label(root, text="")
    status_label.pack(pady=10)

    start_btn = tk.Button(root, text="Crear subdominio", command=lambda: start_process(entry, selected_template, status_label, root))
    start_btn.pack(pady=10)

    root.mainloop()