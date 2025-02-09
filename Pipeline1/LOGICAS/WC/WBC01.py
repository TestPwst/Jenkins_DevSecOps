from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Pipeline1.VariablesGral import Configuracion, Log

import time  # Ayuda a crear una pausa entre cada ejecución, decidiendo el tiempo de espera en esa pausa

driver = webdriver.Chrome()  # se crea el objeto webdriver
wait = WebDriverWait(driver, 60)
action = ActionChains(driver)


class WBC01:  # clase del código
    try:
        driver.get("https://client.assist.com.uy/")  # ingresa a la URL de Client assist
        driver.maximize_window()  # Maximiza la ventana de windows
        time.sleep(3)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar al ambiente assist {e}")
        raise

    try:
        usuario = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.ingreso_usuario)))
        usuario.send_keys(Configuracion.usuariowc)
        time.sleep(1)

        # Se ingresa una contraseña incorrecta para validar que muestre el error en pantalla
        contra = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.ingreso_contrasena)))
        contra.send_keys(Configuracion.contrasena_error)
        time.sleep(1)

        iniciar_sesion = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_ingresar)))
        time.sleep(1)
        iniciar_sesion.click()
        Log().info("Se valida que el ingreso al sistema es correcto")
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar el usuario ni la contraseña, validar el error: {e}")
        raise

    try:
        cerrar_error = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar_error)))
        time.sleep(2)
        cerrar_error.click()
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo cerrar el mensaje de error, revisar el error: {e}")
        raise

    try:
        # Se ingresa la contraseña correcta para validar que muestre el error en pantalla
        contrasena = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.ingreso_contrasena)))
        action \
            .double_click(contrasena) \
            .pause(1) \
            .send_keys(Configuracion.contrasena_ok) \
            .release()
        action.perform()
        time.sleep(1)

        """Boton Ingresar"""
        # Click en el boton de ingresar
        inicio_sesion = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_ingresar)))
        inicio_sesion.click()
        time.sleep(5)
        Log().info("Se valida que el ingreso a la base de datos es correcto")

        time.sleep(3)
        driver.close()
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar a Web client, validar el error: {e}")
        raise
