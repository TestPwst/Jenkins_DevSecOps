from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.common.by import By
from Pipeline1.VariablesGral import *

import time
import re

driver = webdriver.Chrome()  # se crea el objeto webdriver
wait = WebDriverWait(driver, 60)
action = ActionChains(driver)


class WBC29:  # clase del código

    """Ingreso al navegador"""
    global nueva_version
    try:
        driver.get("https://client.assist.com.uy/")  # ingresa a la URL de Client assist
        driver.maximize_window()  # Maximiza la ventana de windows
        time.sleep(3)
    except Exception as e:
        Log().error(f"No se pudo ingresar al ambiente assist {e}")  # pragma: no cover
        raise

    """Inicio de Sesión"""
    try:
        usuario = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.ingreso_usuario)))
        usuario.send_keys(Configuracion.usuariowc)
        time.sleep(1)

        contra = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.ingreso_contrasena)))
        contra.send_keys(Configuracion.contrasena_ok)
        time.sleep(1)

        iniciar_sesion = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_ingresar)))
        time.sleep(1)
        iniciar_sesion.click()
        time.sleep(1)
        Log().info(" Se valida que el ingreso al sistema es correcto")
    except Exception as e:
        Log().error(f"No se pudo ingresar el usuario y/o la contraseña, validar el error: {e}")  # pragma: no cover
        raise

    driver.execute_script("document.body.style.zoom='80%'")

    """Ingreso a Versiones"""
    try:
        usuarios_wbc28 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_versiones)))
        usuarios_wbc28.click()
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo encontrar el campo para ingresar la versión, revisar el error {e}")
        raise
    """Buscar Version 4"""
    try:
        buscar_usuario_wbc2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_buscar)))
        #   BuscarUsuario.send_keys(Configuracion.id_usuario) #-> Configuración Web client ( awsqa)
        buscar_usuario_wbc2.send_keys(Configuracion.buscar_v4)  # -> Configuración assist
        buscar_usuario_wbc2.send_keys(Keys.ENTER)
        Log().info(" Se busca la versión 4 en el sistema")
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f" No se pudo ingresar la versión para buscarla en la base, revisar el error {e}")
        raise

    """Localizar la version mas actual"""
    try:
        versiones = driver.find_elements(By.XPATH, Configuracion.elementos)
        todas_las_versiones = []

        for elem in versiones:
            texto = elem.text.strip()
            match = re.search(r'\b\d+\.\d+\.\d+\.\d+\b', texto)
            if match:
                version = match.group()
                Log().info(f" Versión encontrada: {version}")
                todas_las_versiones.append(version)  # Aseguramos que sean strings

            # Encontrar la versión más alta
            try:
                ultima_version = max(todas_las_versiones, key=lambda v: [int(x) for x in v.split(".")])
            except Exception as e:
                Log().info(f"Error al calcular la versión más alta: {str(e)}")
                ultima_version = None

            if ultima_version:
                # Incrementar el último número de la versión
                partes = ultima_version.split(".")
                partes[-1] = str(int(partes[-1]) + 1)
                nueva_version = ".".join(partes)

                Log().info(f" Nueva versión creada: {nueva_version}")

                """Creación de nueva versión"""
                try:
                    nueva_version_wc28 = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, Configuracion.btn_nuevowc)))
                    action \
                        .move_to_element(nueva_version_wc28) \
                        .pause(1) \
                        .click(nueva_version_wc28) \
                        .pause(1) \
                        .release()
                    action.perform()
                    Log().info(" Se presiona el boton 'Nuevo', para crear una nueva versión.")

                except ElementNotInteractableException as e:  # pragma: no cover
                    Log().error(f"No se pudo interactuar con el botón y crear uno nuevo: {e}")

                campo_input = driver.find_element(By.XPATH, Configuracion.identificador_wc28)
                campo_input.clear()
                campo_input.send_keys(str(nueva_version))
                time.sleep(1)

                campo_description = driver.find_element(By.XPATH, Configuracion.descripcion__wc28)
                campo_description.clear()
                campo_description.send_keys(str(nueva_version))

                campo_id_clickonce = driver.find_element(By.XPATH, Configuracion.id_version_clickonce)
                campo_id_clickonce.clear()
                campo_id_clickonce.send_keys(str(nueva_version))

                campo_id_powerstreet = driver.find_element(By.XPATH, Configuracion.id_version_powerstreet)
                campo_id_powerstreet.clear()
                campo_id_powerstreet.send_keys(str(nueva_version))

                campo_id_mobileeal = driver.find_element(By.XPATH, Configuracion.id_version_mobile)
                campo_id_mobileeal.clear()
                campo_id_mobileeal.send_keys(str(nueva_version))

                campo_id_mobilevm = driver.find_element(By.XPATH, Configuracion.id_version_mobile_vm)
                campo_id_mobilevm.clear()
                campo_id_mobilevm.send_keys(str(nueva_version))

                campo_activa = driver.find_element(By.XPATH, Configuracion.activa)
                campo_activa.click()
                time.sleep(1)

                """Guardar version y cerrar ventana de versiones"""
                try:
                    guardar_registro_wbc28 = wait.until(
                        EC.presence_of_element_located((By.XPATH, Configuracion.btn_guardar)))
                    guardar_registro_wbc28.click()
                    time.sleep(1)
                except Exception as e:
                    Log().error(f"No se pudo guardar correctamente la versión {e}")
                    raise
                try:
                    cerrar_pantalla_wbc28 = wait.until(
                        EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_pantalla_wc)))
                    cerrar_pantalla_wbc28.click()
                    time.sleep(1)
                except Exception as e:
                    Log().error(f"No se pudo cerrar la ventana de versiones {e}")
                    raise
            else:
                print("No se encontraron números en la página.")

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudieron ingresar los datos de la versión, se debe al error: {e}")
        raise

    # driver.quit()

    """Abrir grupo y buscar au3 para 5"""
    try:
        grupos_wbc28 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_grupos)))
        grupos_wbc28.click()
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo encontrar el campo para ingresar el usuario, revisar el error {e}")
        raise
    try:
        buscar_usuario_wbc2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_buscar)))
        buscar_usuario_wbc2.send_keys(Configuracion.grupo_v4)  # -> Configuración assist
        buscar_usuario_wbc2.send_keys(Keys.ENTER)
        Log().info(" Se busca la versión 4 con pex en el sistema")
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f" No se pudo ingresar el usuario para buscarlo en la base, revisar el error {e}")
        raise

    try:
        codigo_pex = driver.find_element(By.XPATH, Configuracion.pex)
        action \
            .move_to_element(codigo_pex) \
            .pause(1) \
            .double_click(codigo_pex) \
            .pause(1) \
            .release()
        action.perform()
        Log().info(" Ingresa al código pex.")
        time.sleep(1)
    except Exception as e:
        Log().error(f"No se pudo abrir el grupo de pex para la versión 4, {e}")
        raise

    """Agregamos la version en 'Servidor y Version'"""
    try:
        menu_servidor_version = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.serv_version)))
        action \
            .move_to_element(menu_servidor_version) \
            .pause(1) \
            .click(menu_servidor_version) \
            .pause(1) \
            .release()
        action.perform()
        Log().info(" Ingresa al menú Servidor y Versión.")
        time.sleep(1)
    except Exception as e:
        Log().error(f"No se pudo dar click en el manú Servidor y Versión {e}")

    try:
        version_servidoryversion = wait.until(EC.presence_of_element_located((
            By.XPATH, Configuracion.menu_desplegable_serv_version)))
        action \
            .move_to_element(version_servidoryversion) \
            .pause(1) \
            .click(version_servidoryversion) \
            .pause(1) \
            .release()
        action.perform()
        Log().info(" Se dio click correctamente en el desplegable")
        time.sleep(1)
    except Exception as e:
        Log().error(f"No se pudo abrir el desplegable para cambiar a la versión más reciente, {e}")
        raise

    try:
        version_actual = driver.find_elements(By.XPATH, Configuracion.elementos)
        todas_las_versiones = []

        for elem in version_actual:
            texto = elem.text.strip()
            match = re.search(r'\b4\.0\.0\.\d+\b', texto)
            if match:
                Log().info(f" Versión actual: {version}")
                # ultima_version = version  # Guardamos la última versión encontrada
                todas_las_versiones.append(version)  # Aseguramos que sean strings

                # Encontrar la versión más alta
                try:
                    ultima_version = max(todas_las_versiones, key=lambda v: [int(x) for x in v.split(".")])
                    element = driver.find_element(By.XPATH,
                                                  "//option[@value='5.0.0.50']/preceding-sibling::option[2]")
                    element.click()
                    Log().info(f" Nueva versión creada: {nueva_version}")

                except Exception as e:
                    Log().info(f"Error al calcular la versión más alta: {str(e)}")
                    ultima_version = None
            else:
                Log().error("No se encontraron versiones en el desplegable")

            """Guardar version"""
            try:
                guardar_version_wbc28 = wait.until(
                    EC.presence_of_element_located((By.XPATH, Configuracion.btn_guardar)))
                guardar_version_wbc28.click()
                time.sleep(1)
            except Exception as e:  # pragma: no cover
                Log().error(f"No se pudo guardar correctamente la versión {e}")
                raise
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo agregar la versión más reciente, {e}")
        raise
    """Actualizamos la base de datos"""
    try:
        # Esperar que el botón para actualizar la base de datos esté presente
        actualizar_bd = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, Configuracion.actualizar_base_version)))

        # Ejecutar el clic sobre el botón de actualización
        action \
            .move_to_element(actualizar_bd) \
            .pause(1) \
            .click(actualizar_bd) \
            .pause(1) \
            .release()
        action.perform()
        Log().info(" Se actualiza la BD de la nueva versión")

    except ElementNotInteractableException as e:
        Log().error(f"No se pudo interactuar con el botón de actualizar BD: {e}")

    # Intentamos hacer clic en el botón para aceptar la actualización
    try:
        # Esperar que el botón 'Aceptar' para actualizar esté presente
        aceptar_actualizar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, Configuracion.aceptar_bd)))

        # Ejecutar el clic sobre el botón de aceptación
        action \
            .move_to_element(aceptar_actualizar) \
            .pause(1) \
            .click(aceptar_actualizar) \
            .pause(1) \
            .release()
        action.perform()
        time.sleep(5)
        Log().info(" Se acepta la actualización de la BD de la nueva versión")
        """Detectar la ventana 1 de navegador (actualizacion)"""
        try:
            time.sleep(2)
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(1)
        except TimeoutException as e:
            Log().error("No se pudo cambiar a la ventana de PowerStreet")

        # Esperar que la página cargue completamente
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Obtener el contenido de la página
        contenido_pagina = driver.find_element(By.TAG_NAME, "body").get_attribute("innerText")
        print("Contenido de la página", contenido_pagina)

        # *Verificar si hay un error 403*
        if "403" in contenido_pagina or "Forbidden" in contenido_pagina:
            Log().error(f"ERROR 403 DETECTADO: You don't have permission to access /{nueva_version}/dbupdate.ashx on this server.")
            actual = driver.current_url
            titulo = driver.title
            print("Página:", actual)
            print("Titulo: ", titulo)
        else:
            actual = driver.current_url
            titulo = driver.title
            print("Página:", actual)
            print("Titulo: ", titulo)
            Log().info("No se detectó bloqueo de acceso, se continúa con la validación.")

            # if "dbupdate.ashx?action=updatedb&dbid=pex" in actual:
            #     Log().info(f"Se está actualizando la base de datos en la URL: {actual}")
            #     raise Exception("Interrupción: URL de actualización detectada")

            try:
                finalizado_texto = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[text()='Finalizado '")))
                Log().info("Actualización de la base de datos finalizada con éxito")
            except:
                Log().warning("No se encontró un mensaje de 'Finalizado'.")

            # Buscar errores en la actualización
            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//onresults")))
                try:
                    onresults_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/onresults")))
                    print("El elemento <onresults> está presente en el DOM.")
                except:
                    print("El elemento <onresults> NO se encuentra en el DOM.")
                time.sleep(10)  # Esperar 10 segundos antes de buscar el elemento
                contenido_pagina = driver.page_source
                if "<onresults>" in contenido_pagina:
                    print("El elemento <onresults> ya está en el DOM.")
                else:
                    print("El elemento <onresults> aún no se ha cargado.")

                if "<error-count>" in contenido_pagina:
                    print("El elemento error-count está en el HTML.")
                else:
                    print("El elemento error-count no está en el HTML.")

                error_count_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//onresults/error-count")))
                print(error_count_element)
                error_text = error_count_element.text

                match = re.search(r"(\d+) errores", error_text)
                errores = int(match.group(1)) if match else 0

                if errores > 0:
                    Log().warning(f"La base de datos se actualizó pero con {errores} errores.")
                else:
                    Log().info("La base de datos se actualizó sin errores.")
            except Exception as e:
                Log().error(f"No se pudo obtener el estado de la actualización de la base de datos: {e}")
                raise

            try:
                cerrar_pantalla = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_pantalla_wc)))
                cerrar_pantalla.click()
                time.sleep(1)
            except Exception as e:
                Log().error(f"No se pudo cerrar la ventana de versiones: {e}")
                raise
        try:
            cerrar_pantalla = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_pantalla_wc)))
            cerrar_pantalla.click()
            time.sleep(1)
        except Exception as e:
            Log().error(f"No se pudo cerrar la ventana de versiones: {e}")
            raise

    except ElementNotInteractableException as e:
        Log().error(f"No se pudo interactuar con el botón de aceptación para actualizar BD: {e}")

    # """PRIMERA VEZ QUE REGRESA A LA VERSION CORRECTA"""
    #     """PRIMERA VEZ QUE REGRESA A LA VERSION CORRECTA"""
    """Regresar a la ventana PowerStreet"""
    try:
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)
    except TimeoutException as e:
        Log().error("No se pudo cambiar a la ventana de PowerStreet")

    """Actualizar nuevamente la siguiente versión nuevamente"""
    """Ingreso a Versiones"""
    try:
        usuarios_wbc28 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_versiones)))
        usuarios_wbc28.click()
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo encontrar el campo para ingresar la versión, revisar el error {e}")
        raise
    """Buscar Version 4"""
    try:
        buscar_usuario_wbc2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_buscar)))
        #   BuscarUsuario.send_keys(Configuracion.id_usuario) #-> Configuración Web client ( awsqa)
        buscar_usuario_wbc2.send_keys(Configuracion.buscar_v4)  # -> Configuración assist
        buscar_usuario_wbc2.send_keys(Keys.ENTER)
        Log().info(" Se busca la versión 4 en el sistema")
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f" No se pudo ingresar la versión para buscarla en la base, revisar el error {e}")
        raise

    """Localizar la version mas actual"""
    try:
        versiones = driver.find_elements(By.XPATH, Configuracion.elementos)
        todas_las_versiones = []

        for elem in versiones:
            texto = elem.text.strip()
            match = re.search(r'\b\d+\.\d+\.\d+\.\d+\b', texto)
            if match:
                version = match.group()
                Log().info(f" Versión encontrada: {version}")
                todas_las_versiones.append(version)  # Aseguramos que sean strings

            # Encontrar la versión más alta
            try:
                ultima_version = max(todas_las_versiones, key=lambda v: [int(x) for x in v.split(".")])
            except Exception as e:
                Log().info(f"Error al calcular la versión más alta: {str(e)}")
                ultima_version = None

            if ultima_version:
                # Incrementar el último número de la versión
                partes = ultima_version.split(".")
                partes[-1] = str(int(partes[-1]) + 1)
                nueva_version = ".".join(partes)

                Log().info(f" Nueva versión creada: {nueva_version}")

                """Creación de nueva versión"""
                try:
                    nueva_version_wc28 = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, Configuracion.btn_nuevowc)))
                    action \
                        .move_to_element(nueva_version_wc28) \
                        .pause(1) \
                        .click(nueva_version_wc28) \
                        .pause(1) \
                        .release()
                    action.perform()
                    Log().info(" Se presiona el boton 'Nuevo', para crear una nueva versión.")

                except ElementNotInteractableException as e:  # pragma: no cover
                    Log().error(f"No se pudo interactuar con el botón y crear uno nuevo: {e}")

                campo_input = driver.find_element(By.XPATH, Configuracion.identificador_wc28)
                campo_input.clear()
                campo_input.send_keys(str(nueva_version))
                time.sleep(1)

                campo_description = driver.find_element(By.XPATH, Configuracion.descripcion__wc28)
                campo_description.clear()
                campo_description.send_keys(str(nueva_version))

                campo_id_clickonce = driver.find_element(By.XPATH, Configuracion.id_version_clickonce)
                campo_id_clickonce.clear()
                campo_id_clickonce.send_keys(str(nueva_version))

                campo_id_powerstreet = driver.find_element(By.XPATH, Configuracion.id_version_powerstreet)
                campo_id_powerstreet.clear()
                campo_id_powerstreet.send_keys(str(nueva_version))

                campo_id_mobileeal = driver.find_element(By.XPATH, Configuracion.id_version_mobile)
                campo_id_mobileeal.clear()
                campo_id_mobileeal.send_keys(str(nueva_version))

                campo_id_mobilevm = driver.find_element(By.XPATH, Configuracion.id_version_mobile_vm)
                campo_id_mobilevm.clear()
                campo_id_mobilevm.send_keys(str(nueva_version))

                campo_activa = driver.find_element(By.XPATH, Configuracion.activa)
                campo_activa.click()
                time.sleep(1)

                """Guardar version y cerrar ventana de versiones"""
                try:
                    guardar_registro_wbc28 = wait.until(
                        EC.presence_of_element_located((By.XPATH, Configuracion.btn_guardar)))
                    guardar_registro_wbc28.click()
                    time.sleep(1)
                except Exception as e:
                    Log().error(f"No se pudo guardar correctamente la versión {e}")
                    raise
                try:
                    cerrar_pantalla_wbc28 = wait.until(
                        EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_pantalla_wc)))
                    cerrar_pantalla_wbc28.click()
                    time.sleep(1)
                except Exception as e:
                    Log().error(f"No se pudo cerrar la ventana de versiones {e}")
                    raise
            else:
                print("No se encontraron números en la página.")

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudieron ingresar los datos de la versión, se debe al error: {e}")
        raise

    # driver.quit()

    """Abrir grupo y buscar au3 para 5"""
    try:
        grupos_wbc28 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_grupos)))
        grupos_wbc28.click()
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo encontrar el campo para ingresar el usuario, revisar el error {e}")
        raise
    try:
        buscar_usuario_wbc2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_buscar)))
        buscar_usuario_wbc2.send_keys(Configuracion.grupo_v4)  # -> Configuración assist
        buscar_usuario_wbc2.send_keys(Keys.ENTER)
        Log().info(" Se busca la versión 4 con pex en el sistema")
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f" No se pudo ingresar el usuario para buscarlo en la base, revisar el error {e}")
        raise

    try:
        codigo_pex = driver.find_element(By.XPATH, Configuracion.pex)
        action \
            .move_to_element(codigo_pex) \
            .pause(1) \
            .double_click(codigo_pex) \
            .pause(1) \
            .release()
        action.perform()
        Log().info(" Ingresa al código pex.")
        time.sleep(1)
    except Exception as e:
        Log().error(f"No se pudo abrir el grupo de pex para la versión 4, {e}")
        raise

    """Agregamos la version en 'Servidor y Version'"""
    try:
        menu_servidor_version = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.serv_version)))
        action \
            .move_to_element(menu_servidor_version) \
            .pause(1) \
            .click(menu_servidor_version) \
            .pause(1) \
            .release()
        action.perform()
        Log().info(" Ingresa al menú Servidor y Versión.")
        time.sleep(1)
    except Exception as e:
        Log().error(f"No se pudo dar click en el manú Servidor y Versión {e}")

    try:
        version_servidoryversion = wait.until(EC.presence_of_element_located((
            By.XPATH, Configuracion.menu_desplegable_serv_version)))
        action \
            .move_to_element(version_servidoryversion) \
            .pause(1) \
            .click(version_servidoryversion) \
            .pause(1) \
            .release()
        action.perform()
        Log().info(" Se dio click correctamente en el desplegable")
        time.sleep(1)
    except Exception as e:
        Log().error(f"No se pudo abrir el desplegable para cambiar a la versión más reciente, {e}")
        raise

    try:
        version_actual = driver.find_elements(By.XPATH, Configuracion.elementos)
        todas_las_versiones = []

        for elem in version_actual:
            texto = elem.text.strip()
            match = re.search(r'\b4\.0\.0\.\d+\b', texto)
            if match:
                Log().info(f" Versión actual: {version}")
                # ultima_version = version  # Guardamos la última versión encontrada
                todas_las_versiones.append(version)  # Aseguramos que sean strings

                # Encontrar la versión más alta
                try:
                    ultima_version = max(todas_las_versiones, key=lambda v: [int(x) for x in v.split(".")])
                    element = driver.find_element(By.XPATH,
                                                  "//option[@value='5.0.0.50']/preceding-sibling::option[1]")
                    element.click()
                    Log().info(f" Nueva versión creada: {nueva_version}")

                except Exception as e:
                    Log().info(f"Error al calcular la versión más alta: {str(e)}")
                    ultima_version = None
            else:
                Log().error("No se encontraron versiones en el desplegable")

            """Guardar version"""
            try:
                guardar_version_wbc28 = wait.until(
                    EC.presence_of_element_located((By.XPATH, Configuracion.btn_guardar)))
                guardar_version_wbc28.click()
                time.sleep(1)
            except Exception as e:  # pragma: no cover
                Log().error(f"No se pudo guardar correctamente la versión {e}")
                raise
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo agregar la versión más reciente, {e}")
        raise
    """Actualizamos la base de datos"""
    try:
        # Esperar que el botón para actualizar la base de datos esté presente
        actualizar_bd = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, Configuracion.actualizar_base_version)))

        # Ejecutar el clic sobre el botón de actualización
        action \
            .move_to_element(actualizar_bd) \
            .pause(1) \
            .click(actualizar_bd) \
            .pause(1) \
            .release()
        action.perform()
        Log().info(" Se actualiza la BD de la nueva versión")

    except ElementNotInteractableException as e:
        Log().error(f"No se pudo interactuar con el botón de actualizar BD: {e}")

    # Intentamos hacer clic en el botón para aceptar la actualización
    try:
        # Esperar que el botón 'Aceptar' para actualizar esté presente
        aceptar_actualizar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, Configuracion.aceptar_bd)))

        # Ejecutar el clic sobre el botón de aceptación
        action \
            .move_to_element(aceptar_actualizar) \
            .pause(1) \
            .click(aceptar_actualizar) \
            .pause(1) \
            .release()
        action.perform()
        time.sleep(5)
        Log().info(" Se acepta la actualización de la BD de la nueva versión")

        # Esperar que la página cargue completamente
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Obtener el contenido de la página
        # contenido_pagina = driver.find_element(By.TAG_NAME, "body").get_attribute("innerText")
        contenido_pagina = driver.page_source

        # *Verificar si hay un error 403*
        if "403" in contenido_pagina or "Forbidden" in contenido_pagina:
            if "Finalizado" not in contenido_pagina and "error-count" not in contenido_pagina:
                Log().error(
                    f"ERROR 403 DETECTADO: You don't have permission to access /{nueva_version}/dbupdate.ashx on this server.")
        else:
            Log().info("No se detectó bloqueo de acceso, se continúa con la validación.")

            try:
                finalizado_texto = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, "//*[text()='Finalizado '")))
                Log().info("Actualización de la base de datos finalizada con éxito")
            except:
                Log().warning("No se encontró un mensaje de 'Finalizado'.")

            # Buscar errores en la actualización
            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//onresults")))
                try:
                    onresults_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "/html/body/onresults")))
                    print("El elemento <onresults> está presente en el DOM.")
                except:
                    print("El elemento <onresults> NO se encuentra en el DOM.")
                time.sleep(10)  # Esperar 10 segundos antes de buscar el elemento
                contenido_pagina = driver.page_source
                if "<onresults>" in contenido_pagina:
                    print("El elemento <onresults> ya está en el DOM.")
                else:
                    print("El elemento <onresults> aún no se ha cargado.")

                contenido_pagina = driver.page_source
                if "<error-count>" in contenido_pagina:
                    print("El elemento error-count está en el HTML.")
                else:
                    print("El elemento error-count no está en el HTML.")

                error_count_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//onresults/error-count")))
                print(error_count_element)
                error_text = error_count_element.text

                match = re.search(r"(\d+) errores", error_text)
                errores = int(match.group(1)) if match else 0

                if errores > 0:
                    Log().warning(f"La base de datos se actualizó pero con {errores} errores.")
                else:
                    Log().info("La base de datos se actualizó sin errores.")
            except Exception as e:
                Log().error(f"No se pudo obtener el estado de la actualización de la base de datos: {e}")
                raise

            try:
                cerrar_pantalla = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_pantalla_wc)))
                cerrar_pantalla.click()
                time.sleep(1)
            except Exception as e:
                Log().error(f"No se pudo cerrar la ventana de versiones: {e}")
                raise
        try:
            cerrar_pantalla = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_pantalla_wc)))
            cerrar_pantalla.click()
            time.sleep(1)
        except Exception as e:
            Log().error(f"No se pudo cerrar la ventana de versiones: {e}")
            raise

    except ElementNotInteractableException as e:
        Log().error(f"No se pudo interactuar con el botón de aceptación para actualizar BD: {e}")

    # """SEGUNDA VEZ QUE REGRESA A LA VERSION CORRECTA"""
