import requests
import warnings

# Ignorar advertencias de InsecureRequestWarning cuando verify=False
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

url_twitter = "https://twitter.com"
url_google = "https://www.google.com" # Para comparar

def test_connection(url):
    print(f"\n--- Probando conexión a: {url} ---")
    # Prueba 1: Con verificación SSL (comportamiento normal)
    print(f"Intentando GET a {url} CON verificación SSL...")
    try:
        response = requests.get(url, timeout=10)
        print(f"  ÉXITO con verificación SSL. Status: {response.status_code}")
    except requests.exceptions.SSLError as e:
        print(f"  FALLÓ con verificación SSL: {e}")
    except Exception as e:
        print(f"  OTRO ERROR con verificación SSL: {e}")

    # Prueba 2: SIN verificación SSL (¡INSEGURO, solo para diagnóstico!)
    print(f"Intentando GET a {url} SIN verificación SSL (¡INSEGURO!)...")
    try:
        response_no_verify = requests.get(url, timeout=10, verify=False)
        print(f"  ÉXITO sin verificación SSL. Status: {response_no_verify.status_code}")
    except requests.exceptions.SSLError as e_no_verify:
        print(f"  FALLÓ incluso sin verificación SSL: {e_no_verify}")
    except Exception as e_general_no_verify:
        print(f"  OTRO ERROR sin verificación SSL: {e_general_no_verify}")

test_connection(url_twitter)
test_connection(url_google) # Probar con otro sitio grande