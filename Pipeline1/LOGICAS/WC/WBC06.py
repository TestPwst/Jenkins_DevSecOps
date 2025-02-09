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

Log_usuario = "Se busca el usuario en el sistema"


class WBC06:  # clase del código

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
        usuario_wbc6 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.ingreso_usuario)))
        usuario_wbc6.send_keys(Configuracion.usuariowc)
        time.sleep(1)

        contras_wbc6 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.ingreso_contrasena)))
        contras_wbc6.send_keys(Configuracion.contrasena_ok)
        time.sleep(1)

        iniciar_sesion_wbc6 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_ingresar)))
        time.sleep(1)
        iniciar_sesion_wbc6.click()
        time.sleep(1)
        Log().info("Se valida que el ingreso al sistema es correcto")
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar el usuario y/o la contraseña, validar el error: {e}")
        raise

    try:
        usuarios_wbc6 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_usuarios)))
        usuarios_wbc6.click()
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo encontrar el campo para ingresar el usuario, revisar el error {e}")
        raise

    try:
        buscar_usuario_wbc6 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_buscar)))
        #   BuscarUsuario.send_keys(Configuracion.id_usuario) #-> Configuración Web client ( awsqa)
        buscar_usuario_wbc6.send_keys(Configuracion.usuario_assist)  # -> Configuración assist
        buscar_usuario_wbc6.send_keys(Keys.ENTER)
        Log().info(Log_usuario)
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar el usuario para buscarlo en la base, revisar el error {e}")
        raise

    try:
        usuario_existe_wbc6 = driver.find_element(By.XPATH, "//td[text()='xcsautest1']")
        if usuario_existe_wbc6.is_displayed():
            try:
                action \
                    .move_to_element(usuario_existe_wbc6) \
                    .pause(0) \
                    .release()
                action.perform()
                Log().info(" Se da clic en el registro creado, para proceder a eliminarlo.")

                elimina_wbc6 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_elimina)))
                time.sleep(0.5)
                elimina_wbc6.click()
                Log().info(" Se presiona el boton 'Eliminar', para eliminar el registro.")

                confirma_elimina_wbc6 = wait.until(
                    EC.presence_of_element_located((By.XPATH, Configuracion.btn_confirmar)))
                time.sleep(0.5)
                confirma_elimina_wbc6.click()
                Log().info(" Se confirma el eliminado del registro")

                cerrar_wbc6 = wait.until(
                    EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_pantalla_wc)))
                cerrar_wbc6.click()
                Log().info(" Se presiona el boton 'Refrescar', para crear un nuevo registro igual al anterior.")
                time.sleep(2)

                usuarios_wbc6_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_usuarios)))
                usuarios_wbc6_1.click()
                time.sleep(1)

                buscar_usuario_wbc6_1 = wait.until(
                    EC.presence_of_element_located((By.XPATH, Configuracion.campo_buscar)))
                #   BuscarUsuario.send_keys(Configuracion.id_usuario) #-> Configuración Web client ( awsqa)
                buscar_usuario_wbc6_1.send_keys(Configuracion.usuario_assist)  # -> Configuración assist
                buscar_usuario_wbc6_1.send_keys(Keys.ENTER)
                Log().info(Log_usuario)
                time.sleep(1)

            except Exception as e:  # pragma: no cover
                Log().error(f"No se pudo encontrar el XPATH. Validar el error: {e}")
                raise
    except NoSuchElementException:  # pragma: no cover
        pass

    try:
        nuevo_usuario_wbc6 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, Configuracion.btn_nuevowc)))
        action \
            .move_to_element(nuevo_usuario_wbc6) \
            .pause(1) \
            .click(nuevo_usuario_wbc6) \
            .pause(1) \
            .release()
        action.perform()
        Log().info(" Se presiona el boton 'Nuevo', para crear un nuevo registro.")
    except ElementNotInteractableException as e:  # pragma: no cover
        Log().error(f"No se pudo interactuar con el botón: {e}")

    try:
        time.sleep(2)
        id_usuario_wbc6 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, Configuracion.campo_idusu)))
        id_usuario_wbc6.click()
        #   IDUsuario.send_keys(Configuracion.id_usuario) #-> Configuración Web client ( awsqa)
        id_usuario_wbc6.send_keys(Configuracion.usuario_assist)  # -> Configuración assist
        time.sleep(1)

        nom_usuario_wbc6 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_nomusu)))
        nom_usuario_wbc6.send_keys(Configuracion.nombre_usuario)
        time.sleep(1)

        grupo_usuario_wbc6 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_grupo)))
        grupo_usuario_wbc6.click()
        time.sleep(1)

        grupo_wbc6 = wait.until(
            EC.presence_of_element_located((By.XPATH, Configuracion.campo_grupoxcs)))  # -> Configuración assist
        grupo_wbc6.click()
        time.sleep(1)

        guardar_registro_wbc6 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_guardar)))
        guardar_registro_wbc6.click()
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo guardar el registro, favor de validar el error: {e}")
        raise

    try:
        cerrar_pantalla_wbc6 = wait.until(
            EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_pantalla_wc)))
        cerrar_pantalla_wbc6.click()
        time.sleep(1)

        usuarios_wbc6_2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_usuarios)))
        usuarios_wbc6_2.click()
        time.sleep(1)

        # Se ingresará aqui una validación para duplicar el usuario (Esperar a que funcione esa opción en WC)

        buscar_usuario_wbc6_2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_buscar)))
        # BuscarUsuario.send_keys(Configuracion.id_usuario) # -> Configuración awsqa
        buscar_usuario_wbc6_2.send_keys(Configuracion.usuario_assist)  # -> Configuración assist
        buscar_usuario_wbc6_2.send_keys(Keys.ENTER)
    except Exception as e:  # pragma: no cover
        Log().error(f" La validación del usuario no fue correcta, revisar el error: {e}")
        raise

    try:
        habilitar_wbc6 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_habilitar_cuenta)))
        habilitar_wbc6.click()
        time.sleep(1)

        aceptar_habilitar_wbc6 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar_error)))
        aceptar_habilitar_wbc6.click()
        time.sleep(1)

        registro_wbc6 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.buscar_usu_assist)))
        action \
            .move_to_element(registro_wbc6) \
            .pause(1) \
            .release()
        action.perform()

        reseteo_contras_wbc6 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_rest_contra)))
        reseteo_contras_wbc6.click()
        time.sleep(1)

        nueva_contras_wbc6 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_newpass2)))
        nueva_contras_wbc6.send_keys(Configuracion.contrasena_ok)
        time.sleep(1)

        valida_contras_wbc6 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_validarpass2)))
        valida_contras_wbc6.send_keys(Configuracion.contrasena_ok)
        time.sleep(1)

        cambiar_contras_wbc6 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar_error)))
        cambiar_contras_wbc6.click()
        time.sleep(1)

        cerrar_sesion_wbc6 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_sesion)))
        cerrar_sesion_wbc6.click()
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo cambiar la contraseña, favor de validar el siguiente error: {e}")
        raise

    try:
        usuario_wbc6_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.ingreso_usuario)))
        usuario_wbc6_1.send_keys(Configuracion.usuario_assist)
        time.sleep(1)

        contras_wbc6_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.ingreso_contrasena)))
        contras_wbc6_1.send_keys(Configuracion.contrasena_ok)
        time.sleep(1)

        iniciar_sesion_wbc6_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_ingresar)))
        time.sleep(1)
        iniciar_sesion_wbc6_1.click()
        time.sleep(2)

        cerrar_sesion_wbc6_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_sesion2)))
        cerrar_sesion_wbc6_1.click()
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar a la sesión, validar el error: {e}")
        raise

    try:
        usuario_wbc6_2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.ingreso_usuario)))
        usuario_wbc6_2.send_keys(Configuracion.usuariowc)
        time.sleep(1)

        contras_wbc6_2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.ingreso_contrasena)))
        contras_wbc6_2.send_keys(Configuracion.contrasena_ok)
        time.sleep(1)

        iniciar_sesion_wbc6_2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_ingresar)))
        time.sleep(1)
        iniciar_sesion_wbc6_2.click()
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudieron ingresar los datos para el inicio de sesión: {e}")
        raise

    try:
        usuarios_wbc6_3 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_usuarios)))
        usuarios_wbc6_3.click()
        time.sleep(1)

        buscar_usuario_wbc6_3 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_buscar)))
        #   BuscarUsuario.send_keys(Configuracion.id_usuario) #-> Configuración Web client ( awsqa)
        buscar_usuario_wbc6_3.send_keys(Configuracion.usuario_assist)  # -> Configuración assist
        buscar_usuario_wbc6_3.send_keys(Keys.ENTER)
        Log().info(Log_usuario)
        time.sleep(1)

        usuario_existe_wbc6_1 = driver.find_element(By.XPATH, "//td[text()='xcsautest1']")
        action \
            .move_to_element(usuario_existe_wbc6_1) \
            .pause(0) \
            .release()
        action.perform()
        Log().info(" Se da clic en el registro creado, para proceder a eliminarlo.")

        elimina_wbc6_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_elimina)))
        time.sleep(0.5)
        elimina_wbc6_1.click()
        Log().info(" Se presiona el boton 'Eliminar', para eliminar el registro.")

        confirma_elimina_wbc6_1 = wait.until(
            EC.presence_of_element_located((By.XPATH, Configuracion.btn_confirmar)))
        time.sleep(1)
        confirma_elimina_wbc6_1.click()
        time.sleep(1)
        Log().info(" Se confirma el eliminado del registro")

        time.sleep(1)
        driver.close()
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo encontrar el campo para ingresar el usuario, revisar el error {e}")
        raise
