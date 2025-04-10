import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

domain = "testizan"

url = "https://my.ionos.es/subdomains/herasoft.ai?linkId=ct.tab.domainlist.subdomains"
url_subdomain = f"https://my.ionos.es/domain-details/{domain}.herasoft.ai"

# Usuario y contraseña de IONOS
user = "i-pointsite.com"
passwd = "R4t420223!"

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

def create_subdomain(driver):
    try:
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
        subdomain_text.send_keys("testizan")

        # Interactúa con el botón de enviar
        submit_btn = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "button.createSubdomain"))
        )
        submit_btn.click()

        print("Subdominio creado con éxito.")
    except Exception as e:
        print("Error al crear el subdominio:", e)
    
def change_dns(driver):
    # Accedemos a la URL del subdominio
    driver.get(url_subdomain)
    
    # Hacemos click a la ventana de configuracion de DNS
    dns_tab = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "domain-tab.dns"))
    )
    dns_tab.click()

    # Accemos click en editar el registro A
    edit_A_record = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/main/div[2]/section[2]/div/form/div[2]/table/tbody/tr[10]/td[6]/a[1]"))
    )
    edit_A_record.click()

    # Cambiar IP del DNS
    change_dns = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "recordValue"))
    )
    change_dns.clear()
    change_dns.send_keys("212.227.169.132")

    # Cambiamos tambien el del subdominio www
    edit_www_record = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/main/div[2]/div[3]/div/form/section[2]/fieldset/ul/li[2]/div[2]/div/p/a[2]"))
    )

    if edit_www_record.text =="Editar registro DNS para www":
        edit_www_record.click()

    # Guardamos el cambio en el registro A
    save_changes = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "button-primary"))
    )
    save_changes.click()

    try:           
        # Guardamos el cambio en el registro A de nuevo
        save_changes = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "button-primary"))
        )
        save_changes.click()
    except:
        pass