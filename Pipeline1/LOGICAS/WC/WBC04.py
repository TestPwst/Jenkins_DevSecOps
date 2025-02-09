from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from Pipeline1.VariablesGral import Configuracion, Log

import time

driver = webdriver.Chrome()  # se crea el objeto webdriver
wait = WebDriverWait(driver, 60)
action = ActionChains(driver)


class WBC04:  # clase del código

    """Ingreso al navegador"""
    try:
        driver.get("https://client.assist.com.uy/")  # ingresa a la URL de Client assist
        driver.maximize_window()  # Maximiza la ventana de windows
        time.sleep(3)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar al ambiente assist {e}")
        raise

    """Inicio de Sesión"""
    try:
        usuario_wbc4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.ingreso_usuario)))
        usuario_wbc4.send_keys(Configuracion.usuariowc)
        time.sleep(1)

        contra_wbc4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.ingreso_contrasena)))
        contra_wbc4.send_keys(Configuracion.contrasena_ok)
        time.sleep(1)

        iniciar_sesion_wbc4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_ingresar)))
        time.sleep(1)
        iniciar_sesion_wbc4.click()
        time.sleep(1)
        Log().info("Se valida que el ingreso al sistema es correcto")
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar el usuario y/o la contraseña, validar el error: {e}")
        raise

    try:
        usuarios_wbc4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_usuarios)))
        usuarios_wbc4.click()
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo encontrar el campo para ingresar el usuario, revisar el error {e}")
        raise

    try:
        buscar_usuario_wbc4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_buscar)))
        #   BuscarUsuario.send_keys(Configuracion.id_usuario) #-> Configuración Web client ( awsqa)
        buscar_usuario_wbc4.send_keys(Configuracion.usuario_assist_modif)  # -> Configuración assist
        buscar_usuario_wbc4.send_keys(Keys.ENTER)
        Log().info("Se busca el usuario en el sistema")
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar el usuario para buscarlo en la base, revisar el error {e}")
        raise

    try:
        usuario_wbc4_1 = driver.find_element(By.XPATH, Configuracion.txt_buscar_assist)
        action \
            .move_to_element(usuario_wbc4_1) \
            .pause(0) \
            .double_click(usuario_wbc4_1) \
            .release()
        action.perform()
        Log().info(" Se da clic en el registro creado, para proceder a eliminarlo.")

        nom_usuario_wbc4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_nomusu)))
        action \
            .double_click(nom_usuario_wbc4) \
            .send_keys(Keys.DELETE) \
            .double_click(nom_usuario_wbc4) \
            .send_keys(Keys.DELETE) \
            .double_click(nom_usuario_wbc4) \
            .pause(0) \
            .send_keys(Configuracion.nombre_cambio) \
            .release()
        action.perform()
        time.sleep(1)

        perfilusuario_wbc4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_perfil)))
        perfilusuario_wbc4.click()
        time.sleep(1)

        perfilaut_wbc4 = wait.until(
            EC.presence_of_element_located((By.XPATH, Configuracion.campo_perfil_assist)))  # Configuracion assist
        perfilaut_wbc4.click()
        time.sleep(1)

        guardarregistro_wbc4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_guardar)))
        guardarregistro_wbc4.click()
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo guardar el registro, revisar el error {e}")
        raise

    try:
        cerrar_pantalla_wbc4 = wait.until(
            EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_pantalla_wc)))
        cerrar_pantalla_wbc4.click()
        time.sleep(1)

        usuarios_wbc4_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_usuarios)))
        usuarios_wbc4_1.click()
        time.sleep(1)

        buscar_usuario_wbc4_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_buscar)))
        # BuscarUsuario.send_keys(Configuracion.id_usuario) # -> Configuración awsqa
        buscar_usuario_wbc4_1.send_keys(Configuracion.usuario_assist_modif)  # -> Configuración assist
        buscar_usuario_wbc4_1.send_keys(Keys.ENTER)
        time.sleep(2)

        cerrarsesion_wbc4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_sesion)))
        cerrarsesion_wbc4.click()
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f" La validación del usuario no fue correcta, revisar el error: {e}")
        raise

    try:
        usuario_wbc4_2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.ingreso_usuario)))
        usuario_wbc4_2.send_keys(Configuracion.usuario_assist_modif)
        time.sleep(1)

        contra_wbc4_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.ingreso_contrasena)))
        contra_wbc4_1.send_keys(Configuracion.contrasena_error)
        time.sleep(1)

        iniciar_sesion_wbc4_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_ingresar)))
        time.sleep(1)
        iniciar_sesion_wbc4_1.click()
        time.sleep(1)
        Log().info("Se inicia sesión en la cuenta recien creada")
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar a la sesión, validar el error: {e}")
        raise

    try:
        cerrar_sesion_wbc4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_sesion2)))
        time.sleep(1)
        cerrar_sesion_wbc4.click()
        time.sleep(1)
        Log().info("Se cierra la sesión de la cuenta")

        usuario_wbc4_3 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.ingreso_usuario)))
        usuario_wbc4_3.send_keys(Configuracion.usuariowc)
        time.sleep(1)

        contra_wbc4_2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.ingreso_contrasena)))
        contra_wbc4_2.send_keys(Configuracion.contrasena_ok)
        time.sleep(1)

        iniciar_sesion_wbc4_2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_ingresar)))
        time.sleep(1)
        iniciar_sesion_wbc4_2.click()
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo iniciar sesión, revisar error {e}")
        raise

    try:
        usuarios_wbc4_2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_usuarios)))
        usuarios_wbc4_2.click()
        time.sleep(1)

        buscar_usuario_wbc4_2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_buscar)))
        #   BuscarUsuario.send_keys(Configuracion.id_usuario) #-> Configuración Web client ( awsqa)
        buscar_usuario_wbc4_2.send_keys(Configuracion.usuario_assist_modif)  # -> Configuración assist
        buscar_usuario_wbc4_2.send_keys(Keys.ENTER)
        Log().info("Se busca el usuario en el sistema")
        time.sleep(1)

        usuario_wbc4_4 = driver.find_element(By.XPATH, Configuracion.txt_buscar_assist)
        action \
            .move_to_element(usuario_wbc4_4) \
            .pause(0) \
            .double_click(usuario_wbc4_4) \
            .release()
        action.perform()
        Log().info(" Se da clic en el registro creado, para modificarlo")

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo encontrar el campo para ingresar el usuario, revisar el error {e}")
        raise

    try:
        nom_usuario_wbc4_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_nomusu)))
        action \
            .double_click(nom_usuario_wbc4_1) \
            .send_keys(Keys.DELETE) \
            .double_click(nom_usuario_wbc4_1) \
            .send_keys(Keys.DELETE) \
            .double_click(nom_usuario_wbc4_1) \
            .send_keys(Keys.DELETE) \
            .pause(1) \
            .send_keys(Configuracion.nombre_cambio2) \
            .release()
        action.perform()
        time.sleep(1)

        perfilusuario_wbc4_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_perfil)))
        perfilusuario_wbc4_1.click()
        time.sleep(1)

        perfilaut_wbc4_1 = wait.until(
            EC.presence_of_element_located((By.XPATH, Configuracion.campo_perfil_nada)))  # Configuracion assist
        perfilaut_wbc4_1.click()
        time.sleep(1)

        guardarregistro_wbc4_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_guardar)))
        guardarregistro_wbc4_1.click()
        time.sleep(2)
        Log().info("Se modifica el usuario dejandolo de manera predeterminada")

        driver.close()
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo guardar el registro del usuario, revisar el error {e}")
        raise
