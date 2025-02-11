import time
import os
import pandas as pd

from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from io import StringIO
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Pipeline1.VariablesGral import Log
from Pipeline1.VariablesGral import Configuracion

driver = webdriver.Chrome()  # se crea el objeto webdriver
wait = WebDriverWait(driver, 60)
action = ActionChains(driver)

Log_incorrect = "El ingreso para realizar un documento de venta de contado no fue correcto."
Argument_scroll = "arguments[0].scrollIntoView()"
Log_docarti = "Se ingresa a la Tabla Docarti para validar que la venta se guardó de forma correcta."
Log_cerrar_ventana = "No se dió click en Cerrar Ventana, validar que la acción anterior haya finalizado."


def ingreso_chrome():
    """Ingreso a Chrome"""

    driver.get("https://client.assist.com.uy/")  # ingresa a la URL de Client assist
    driver.maximize_window()  # Maximiza la ventana de windows
    time.sleep(3)


# ------------------------------------------Funciones Generales---------------------------------------------------
class funciones:

    # ------------------------------------------INGRESO LOGGIN---------------------------------------------------

    def ingresologin(self):

        # PROCESO DE INICIAR SESIÓN#
        # Ingresar usuario
        try:
            usuario = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.ingreso_usuario)))
            usuario.send_keys(Configuracion.usuario)
            time.sleep(1)
            # Log().info(" Escribe el usuario")

        except Exception as e:  # pragma: no cover
            Log().error(
                f"No se pudo encontrar el campo para ingresar el usuario, favor de revisar el error: {e}")
            raise

        # Ingresar contraseña
        try:
            contrasena = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.ingreso_contrasena)))
            contrasena.send_keys(Configuracion.contrasena)
            time.sleep(1)
            # Log().info(" Escribe la contraseña")

        except Exception as e:  # pragma: no cover
            Log().error(
                f"No se pudo encontrar el campo para ingresar la contraseña, favor de validar el error: {e}")
            raise

        """Boton_Ingresar"""
        # Click en el boton de ingresar
        try:
            iniciar_sesion = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_ingresar)))
            iniciar_sesion.click()
            Log().info("Se ingresó el usuario y contraseña correspondiente a la prueba para ingresar a la base")

        except Exception as e:  # pragma: no cover
            Log().error(
                f"No se pudo encontrar el boton para iniciar sesión, favor de validar el error: {e}")
            raise

        """Ingresar a PowerStreet Enterprise"""
        # Ejecuta Enterprise
        try:
            enterprise = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_enterprise)))
            enterprise.click()
            time.sleep(2)
        # Log().info(" Ejecutar Enterprise")

        except Exception as e:  # pragma: no cover
            Log().error(
                f"No se pudo encontrar el boton enterprise, favor de validar el error{e}")
            raise

        # Cambia de pestaña
        try:
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(10)
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(2)
            Log().info("Se hace el ingreso correcto a la base y se visualiza la pantalla principal de PWST 2.0")

        except Exception as e:  # pragma: no cover
            Log().error(
                f"No se pudo cambiar de ventana, favor de validar el error: {e}")
            raise

        try:
            btn_cierrasesionactiva = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, Configuracion.btn_cierrasesionactiva2)))

            if btn_cierrasesionactiva.is_displayed() and btn_cierrasesionactiva.is_enabled():
                btn_cierrasesionactiva.click()
                time.sleep(2)
            # Log().info("Se cierra sesión anterior")

        except Exception as e:  # pragma: no cover
            Log().error(
                f"No se pudo cambiar cerrar la sesión activa, favor de validar el error: {e}")
        pass

        # Cambio de menu
        try:
            tipo_menu = WebDriverWait(driver, 10).until(
                EC.visibility_of_all_elements_located((By.XPATH, Configuracion.menulateral)))
            cambiomenu = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_sandwich)))

            # Si esta activo el menu lateral entonces da clic al cambio de menuu
            if len(tipo_menu) > 0:
                cambiomenu.click()
                # Log().info(" Se dio clic para cambiar de menu ")
                time.sleep(1)
                driver.execute_script("document.body.style.zoom='80%'")
                time.sleep(1)
                # allure.attach(driver.get_screenshot_as_png(),name="Ingreso Enterprise",
                # attachment_type=AttachmentType.PNG)
            else:
                Log().info(" Se esta usando el menu horizontal ")

        except Exception as e:  # pragma: no cover
            Log().error(
                f"No se pudo cambiar el tipo de menu, validar el error: {e}")
            raise

        except NoSuchElementException as e:  # pragma: no cover
            Log().error(
                f"No se pudo cambiar de menu, el elemento no fue encontrado, revisar el error: {e}")
        pass

    # ----------------------------------TABLA ARTICULOS-----------------------------------------------------

    def ingreso_tabla_articulos(self):

        # Ingresa a la tabla artículos
        try:
            tablas_fg = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_tablas)))
            action \
                .move_to_element(tablas_fg) \
                .pause(0) \
                .release()
            action.perform()
            Log().info("Se ingresa al menú Tablas")
            time.sleep(2)

            # Ingresa a Articulos
            articulo_fg = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_articulos)))
            action \
                .move_to_element(articulo_fg) \
                .pause(0) \
                .release()
            action.perform()
            Log().info("Se ingresó al menú Articulos")
            time.sleep(2)

            articulos_fg = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.articulos)))
            articulos_fg.click()
            time.sleep(3)

        except Exception as e:  # pragma: no cover
            Log().error(f"El ingreso a la tabla artículos no fue correcto  {e}")
            time.sleep(2)
            return False

        try:
            filtroart_fg = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.filtro_art)))
            filtroart_fg.click()
            time.sleep(2)

            buscar_cod_fg = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.buscar_cod)))
            action \
                .click(buscar_cod_fg) \
                .send_keys("C") \
                .send_keys("C") \
                .pause(0) \
                .release()
            action.perform()
            time.sleep(1)

            filtrocodart_fg = driver.find_element(By.XPATH, Configuracion.filtro_codart)
            action \
                .double_click(filtrocodart_fg) \
                .pause(0) \
                .release()
            action.perform()
            time.sleep(1)

        except Exception as e:  # pragma: no cover
            Log().error(f"El ingreso al filtro no fue correcto {e}")
            time.sleep(2)
            driver.quit()
            return False

    # -----------------------------------------REPORTES DZ-----------------------------------------------------

    def ingresoreportes_dz(self):

        # Ingreso a reporte stock valorizado por deposito
        try:
            reportes_dz = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_report_dz)))
            action \
                .move_to_element(reportes_dz) \
                .pause(1) \
                .release()
            action.perform()
            time.sleep(1)

            stock = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.menu_stock)))  # Configuracion.Menu_Stock
            action \
                .move_to_element(stock) \
                .pause(0) \
                .release()
            action.perform()

            saldos = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.menu_saldos)))  # Configuracion.Menu_Saldos
            action \
                .move_to_element(saldos) \
                .pause(0) \
                .release()
            action.perform()

            stock_valorizado = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.menu_svd)))  # Configuracion.Menu_SVD
            action \
                .click(stock_valorizado) \
                .release()
            action.perform()
            Log().info(" Abre la pantalla del reporte Stock Valorizado por Deposito ")
            time.sleep(2)

            calmacen = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_almacen)))
            calmacen.send_keys(Configuracion.almacen)
            time.sleep(2)
            Log().info(" Ingresa el almacen ")

            ver = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_ver1)))
            ver.click()
            Log().info(" Se presiona el boton 'Ver', para mostrar la informacion del reporte.")
            time.sleep(4)

        except Exception as e:  # pragma: no cover
            Log().error(
                f" El ingreso para a la pantalla del reporte de stock no fue correcto, favor de validar el error: {e}")
            time.sleep(5)
            return False

    def reingreso_reporte_dz(self):

        try:
            refresh_reporte = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_actulizareporte)))
            time.sleep(1)
            refresh_reporte.click()
            time.sleep(5)

        except Exception as e:
            Log().error(f"No se pudo actualizar el reporte DZ {e}")
            raise

    def reingreso_reporte_dz2(self):

        try:
            refresh_reporte = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_actulizareporte)))
            time.sleep(1)
            refresh_reporte.click()
            time.sleep(5)

            cierra_todo1 = wait.until(
                EC.presence_of_element_located((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[1]")))
            cierra_todo1.click()
            time.sleep(2)

        except Exception as e:
            Log().error(f"No se pudo actualizar el reporte DZ, error: {e}")
            raise

    def ingreso_almacen_central(self):
        try:
            reportes_dz = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_report_dz)))
            action \
                .move_to_element(reportes_dz) \
                .pause(1) \
                .release()
            action.perform()
            time.sleep(1)

            stock = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.menu_stock)))  # Configuracion.Menu_Stock
            action \
                .move_to_element(stock) \
                .pause(0) \
                .release()
            action.perform()

            saldos = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.menu_saldos)))  # Configuracion.Menu_Saldos
            action \
                .move_to_element(saldos) \
                .pause(0) \
                .release()
            action.perform()

            stock_valorizado = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.menu_svd)))  # Configuracion.Menu_SVD
            action \
                .click(stock_valorizado) \
                .release()
            action.perform()
            Log().info(" Abre la pantalla del reporte Stock Valorizado por Deposito ")
            time.sleep(2)

            calmacen = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_almacen)))
            calmacen.send_keys(Configuracion.almacen_central)
            time.sleep(2)
            Log().info(" Ingresa el almacen ")

            clista_precio = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_lista_precio)))
            clista_precio.send_keys(Configuracion.lista_precio)
            time.sleep(2)
            Log().info("Se ingresa la lista precio")

            ver = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_ver1)))
            ver.click()
            Log().info(" Se presiona el boton 'Ver', para mostrar la informacion del reporte.")
            time.sleep(4)
        except Exception as e:
            Log().error(f"No permite ver el almacén central, {e}")
            raise

    # --------------------------------INGRESO VENTA CONTADO----------------------------------------------------
    def venta_contado(self):

        try:
            tabla_doc_fg_vc = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_documentos)))
            action \
                .move_to_element(tabla_doc_fg_vc) \
                .pause(1) \
                .release()
            action.perform()

            tabla_doccli_fg_vc = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_doc_clie)))
            action \
                .move_to_element(tabla_doccli_fg_vc) \
                .pause(0) \
                .release()
            action.perform()

            mas_doc_fg_vc = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_mas_doc)))
            action \
                .click(mas_doc_fg_vc) \
                .release()
            action.perform()

            doc_ventacont_fg_vc = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.doc_venta_contado)))
            action \
                .click(doc_ventacont_fg_vc) \
                .pause(0) \
                .release()
            action.perform()
            time.sleep(2)

        except Exception as e:  # pragma: no cover
            Log().error(f"Log_incorrect {e}")
            time.sleep(2)
            return False

    # ------------------------------------DOCUMENTOS EMITIDOS------------------------------------------------------

    def documentos_emitidos(self):

        # Ingreso a Documentos emitidos
        try:
            tabla_doc_fg_de = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_documentos)))
            action \
                .move_to_element(tabla_doc_fg_de) \
                .pause(0) \
                .release()
            action.perform()
            Log().info("Despliega el menú Documentos")

            tabla_docemit_fg_de = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.menu_doc_emitidos)))
            action \
                .move_to_element(tabla_docemit_fg_de) \
                .pause(0) \
                .click(tabla_docemit_fg_de) \
                .release()
            action.perform()
            Log().info("Ingresa a documentos emitidos")

        except Exception as e:  # pragma: no cover
            Log().error(f"Log_incorrect {e}")
            time.sleep(2)
            return False

        # Se ingresan los filtros para encontrar el documento emitido

        try:
            filtro_docemit_fg_de = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.filtro_doc_emit)))
            action \
                .double_click(filtro_docemit_fg_de) \
                .pause(0) \
                .release()
            action.perform()
            Log().info("Se dio clic en el filtro documentos")
            time.sleep(1)

            filtro_anulado_fg_de = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.filtro_anulado)))
            action \
                .click(filtro_anulado_fg_de) \
                .pause(0) \
                .send_keys("H") \
                .release()
            action.perform()
            time.sleep(1)

            filtro_hoy_fg_de = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.filtro_hoy)))
            action \
                .move_to_element(filtro_hoy_fg_de) \
                .pause(0) \
                .double_click(filtro_hoy_fg_de) \
                .release()
            action.perform()
            time.sleep(1)

            refresca_fg_de = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_refresca)))
            refresca_fg_de.click()
            time.sleep(2)

        except Exception as e:  # pragma: no cover
            Log().error(f'Log_incorrect {e}')
            time.sleep(2)
            return False

        # Ordena columnas por observaciones
        try:
            ordenarcobservaciones_fg_de = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.columna_observaciones)))
            ordenarcobservaciones_fg_de.click()
            time.sleep(2)

        except Exception as e:  # pragma: no cover
            Log().error(f"No se ordenó la columna observaciones {e}")
            time.sleep(2)
            return False

        try:
            ordenarcobservaciones2_fg_de = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.columna_observaciones)))
            ordenarcobservaciones2_fg_de.click()
            time.sleep(2)

        except Exception as e:  # pragma: no cover
            Log().error(f"No se ordenó correctamente la columna observaciones {e}")
            time.sleep(2)
            return False

    # ******************************* DOCUMENTOS PENDIENTES *****************************************************

    def documentos_pendientes(self):

        # Ingreso a Documentos pendientes
        try:
            documentos = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_documentos)))
            action \
                .move_to_element(documentos) \
                .pause(0) \
                .release()
            action.perform()

            documentos_pendientes = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.menu_doc_pendientes)))
            action \
                .click(documentos_pendientes) \
                .release()
            action.perform()
            Log().info(" Ingresa a documentos pendientes ")
            time.sleep(2)

        except (NoSuchElementException, TimeoutException) as e:
            Log().error(f" El ingreso para pantalla de documentos pendientes no fue correcto. {e}")
            time.sleep(5)
            return False

        # Ingreso al filtro de Documentos Pendientes
        try:
            cfiltro_docpendiente = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.filtro_doc_pend)))
            action \
                .double_click(cfiltro_docpendiente) \
                .pause(0) \
                .release()
            action.perform()

            # Bajamos hasta el filtro
            filtrobackorder = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.filtro_backorder)))
            action \
                .click(filtrobackorder) \
                .pause(0) \
                .send_keys("H") \
                .pause(0) \
                .release()
            action.perform()

            # Seleccionamos filtro Hoy
            filtrohoy = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.filtro_hoy)))
            action \
                .double_click(filtrohoy) \
                .pause(0) \
                .release()
            action.perform()

        except Exception as e:
            Log().error(f"No se pudo ingresar al filtro, error {e}")
            time.sleep(2)
            return False

        # Da clic en refrescar
        try:
            refresca = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_refresca)))
            refresca.click()
            time.sleep(2)

        except Exception as e:
            Log().error(f"No se dio click al botón Refrescar, validar error {e}")
            time.sleep(2)
            return False

        # Ordena por columna observaciones
        try:
            ordenarcobservaciones = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.columna_observaciones)))
            ordenarcobservaciones.click()
            time.sleep(2)
            Log().info("Se valida que la venta se encuentra en documentos pendientes")

        except Exception as e:
            Log().error(f"No se ordeno la columna observaciones, validar {e}")
            time.sleep(2)
            return False

        try:
            ordenarcobservaciones2 = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.columna_observaciones)))
            ordenarcobservaciones2.click()
            time.sleep(2)

        except Exception as e:
            Log().error(f"No se ordeno la columna observaciones, validar {e}")
            time.sleep(2)
            return False

    # -------------------------------INGRESO DEVOLUCIÓN DE CONTADO------------------------------------------------

    def devolucion_contado(self):
        # Ingreso a devolucion de contado
        try:
            tabla_doc_fg_dc = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_documentos)))
            action \
                .move_to_element(tabla_doc_fg_dc) \
                .pause(0) \
                .release()
            action.perform()

            tabla_doccli_fg_dc = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_doc_clie)))
            action \
                .move_to_element(tabla_doccli_fg_dc) \
                .pause(0) \
                .release()
            action.perform()

            doc_devcont_fg_dc = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.doc_dev_contado)))
            action \
                .click(doc_devcont_fg_dc) \
                .pause(0) \
                .release()
            action.perform()
            time.sleep(2)

        except Exception as e:  # pragma: no cover
            Log().error(f'Log_incorrect {e}')
            time.sleep(2)
            return False

    # ------------------------------------------ PREVENTA CONTADO -----------------------------------------------
    def preventa_contado(self):
        try:
            tabla_doc = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_documentos)))
            action \
                .move_to_element(tabla_doc) \
                .pause(1) \
                .release()
            action.perform()
            Log().info(" Selecciona el menú Documentos")

            tabla_doc_cli = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_doc_clie)))
            action \
                .move_to_element(tabla_doc_cli) \
                .pause(0) \
                .release()
            action.perform()
            Log().info(" Selecciona la opción de Clientes")

            mas_doc = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_mas_doc)))
            action \
                .click(mas_doc) \
                .release()
            action.perform()
            Log().info(" Selecciona la opción de más documentos")

            doc_preventa_cont = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.doc_preventa_contado)))
            action \
                .click(doc_preventa_cont) \
                .pause(0) \
                .release()
            action.perform()
            Log().info(" Abre el documento PreVenta Contado")
            time.sleep(2)

        except Exception as e:
            Log().info(f"El ingreso para realizar un documento de preventa de contado no fue correcto, {e}")
            time.sleep(2)
            return False

    # -------------------------------REPORTE DOCARTI DEVOLUCIÓN DE CONTADO---------------------------------------------

    def tabla_docarti_dco(self):
        # Ingreso a Herramientas -> Explorador de reportes
        try:
            herramientas_fg_docartidco = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.menu_herramientas)))
            action \
                .move_to_element(herramientas_fg_docartidco) \
                .pause(0) \
                .release()
            action.perform()

            explorador_reportes_fg_docartidco = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.menu_exp_reportes)))
            action \
                .click(explorador_reportes_fg_docartidco) \
                .release()
            action.perform()
            Log().info("Abre explorador de reportes ")
            time.sleep(1)

        except Exception as e:  # pragma: no cover
            Log().error(f"El ingreso explorador de reportes no fue correcto.  {e}")
            time.sleep(5)
            return False

        # Busca y abre el reporte docarti
        try:
            bdocarti_fg_docartidco = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.campo_busqueda)))
            bdocarti_fg_docartidco.send_keys(Configuracion.t_reporte_docarti)
            bdocarti_fg_docartidco.send_keys(Keys.ENTER)

            reporte_docarti_fg_docartidco = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.reporte_docarti)))
            action \
                .move_to_element(reporte_docarti_fg_docartidco) \
                .pause(0) \
                .double_click(reporte_docarti_fg_docartidco) \
                .pause(0) \
                .release()
            action.perform()
            Log().info("Abre reporte docarti")
            time.sleep(1)

            # Se ingresa tipo de documento
            ctipodoc_fg_docartidco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_tipodoc)))
            ctipodoc_fg_docartidco.send_keys(Configuracion.cod_tipo_doc_dco)
            Log().info("Ingresa el tipo de documento PM10")

            # Se ingresa la serie del documento
            cserie_fg_docartidco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_ayuda_serie)))
            cserie_fg_docartidco.click()

            bserie_fg_docartidco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.buscar_art)))
            bserie_fg_docartidco.send_keys(Configuracion.serie)
            time.sleep(2)

            bbusqueda_fg_docartidco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_busqueda)))
            bbusqueda_fg_docartidco.click()
            time.sleep(1)

            serie_fg_docartidco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.txt_serie)))
            action \
                .double_click(serie_fg_docartidco) \
                .pause(0) \
                .release()
            action.perform()
            time.sleep(2)

        except Exception as e:  # pragma: no cover
            Log().error(f"No se pudo abrir el reporte docarti {e}")
            time.sleep(2)
            return False

    # -----------------------------------REPORTE DOCARTI VENTA CONTADO---------------------------------------------

    def tabla_docarti_vco(self):

        # Ingreso a Herramientas -> Explorador de reportes
        try:
            herramientas_fg_docartivco = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.menu_herramientas)))
            action \
                .move_to_element(herramientas_fg_docartivco) \
                .pause(0) \
                .release()
            action.perform()

            explorador_reportes_fg_docartivco = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.menu_exp_reportes)))
            action \
                .click(explorador_reportes_fg_docartivco) \
                .release()
            action.perform()
            Log().info("Abre explorador de reportes")
            time.sleep(1)

        except Exception as e:  # pragma: no cover
            Log().error(f"El ingreso al explorador de reportes no fue correcto. {e}")
            time.sleep(5)
            return False

        # Busca y abre el reporte docarti
        try:
            bdocarti_fg_docartivco = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.campo_busqueda)))
            bdocarti_fg_docartivco.send_keys(Configuracion.t_reporte_docarti)
            bdocarti_fg_docartivco.send_keys(Keys.ENTER)

            reporte_docarti_fg_docartivco = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.reporte_docarti)))
            action \
                .move_to_element(reporte_docarti_fg_docartivco) \
                .pause(0) \
                .double_click(reporte_docarti_fg_docartivco) \
                .pause(0) \
                .release()
            action.perform()
            Log().info("Abre el reporte docarti")
            time.sleep(1)

            # Se ingresa tipo de documento
            ctipodoc_fg_docartivco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_tipodoc)))
            ctipodoc_fg_docartivco.send_keys(Configuracion.cod_tipo_doc_vco)
            Log().info("Ingresa el tipo de documento PM03")

            # Se ingresa la serie del documento
            cserie_fg_docartivco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_ayuda_serie)))
            cserie_fg_docartivco.click()

            bserie_fg_docartivco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.buscar_art)))
            bserie_fg_docartivco.send_keys(Configuracion.serie)
            time.sleep(2)

            bbusqueda_fg_docartivco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_busqueda)))
            bbusqueda_fg_docartivco.click()
            time.sleep(1)

            serie_fg_docartivco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.txt_serie)))
            action \
                .double_click(serie_fg_docartivco) \
                .pause(0) \
                .release()
            action.perform()
            time.sleep(2)

        except Exception as e:  # pragma: no cover
            Log().error(f"No se pudo abrir el reporte docarti de Venta de Contado {e}")
            time.sleep(2)
            return False

    # ------------------------------ Tabla Docartimpu -----------------------------------------

    def tabla_docartimpu(self):
        # Busca y abre el reporte docartimpu
        try:
            bdocartimpu_fg_docartimpu = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.campo_busqueda)))
            bdocartimpu_fg_docartimpu.click()
            bdocartimpu_fg_docartimpu.send_keys(Configuracion.t_reporte_docartimpu)
            bdocartimpu_fg_docartimpu.send_keys(Keys.ENTER)

            reporte_docartimpu_fg_docartimpu = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.reporte_docartimpu)))
            action \
                .move_to_element(reporte_docartimpu_fg_docartimpu) \
                .pause(0) \
                .double_click(reporte_docartimpu_fg_docartimpu) \
                .pause(0) \
                .release()
            action.perform()
            time.sleep(2)

        except Exception as e:  # pragma: no cover
            Log().error(f"No se pudo abrir el reporte docartimpu {e}")
            time.sleep(2)
            raise

        # Ingreso de las propiedades del reporte
        # Ingreso de la clave correlativa del documento
        try:
            ctipodoc_fg_docartimpu = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_tipodoc)))
            ctipodoc_fg_docartimpu.send_keys(Configuracion.cod_tipo_doc_vco)
            time.sleep(2)

        except Exception as e:  # pragma: no cover
            Log().error(f"No se pudo ingresar el código PM03 {e}")
            time.sleep(2)
            raise

        # Ingreso serie
        try:
            cserie_fg_docartimpu = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_ayuda_serie)))
            cserie_fg_docartimpu.click()

            bserie_fg_docartimpu = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.buscar_art)))
            bserie_fg_docartimpu.send_keys(Configuracion.serie)
            time.sleep(2)

            bbusqueda_fg_docartimpu = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_busqueda)))
            bbusqueda_fg_docartimpu.click()
            time.sleep(1)

            serie_fg_docartimpu = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.txt_serie)))
            action \
                .double_click(serie_fg_docartimpu) \
                .pause(0) \
                .release()
            action.perform()
            time.sleep(2)

        except Exception as e:  # pragma: no cover
            Log().error(f"No se pudo ingresar correctamente la serie {e}")
            time.sleep(2)
            raise

    # ---------------------------------TABLA DOCUMENTOS-----------------------------------------------------
    def tabla_documentos(self):
        # Ingreso a Herramientas -> Explorador de reportes
        try:
            herramientas_fg_documentos = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.menu_herramientas)))
            action \
                .move_to_element(herramientas_fg_documentos) \
                .pause(0) \
                .release()
            action.perform()

            explorador_reportes_fg_documentos = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.menu_exp_reportes)))
            action \
                .click(explorador_reportes_fg_documentos) \
                .release()
            action.perform()
            time.sleep(2)

        except Exception as e:  # pragma: no cover
            Log().error(f"El ingreso a explorador de reportes no fue correcto. {e}")
            time.sleep(5)

            driver.quit()
            return False

        # Busca y abre el reporte documentos
        try:
            bdocumentos_fg_documentos = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.campo_busqueda)))
            bdocumentos_fg_documentos.send_keys(Configuracion.t_rep_doc)
            bdocumentos_fg_documentos.send_keys(Keys.ENTER)

            reporte_documentos_fg_documentos = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.reporte_documentos)))
            action \
                .move_to_element(reporte_documentos_fg_documentos) \
                .pause(0) \
                .double_click(reporte_documentos_fg_documentos) \
                .pause(0) \
                .release()
            action.perform()
            time.sleep(2)

        except Exception as e:  # pragma: no cover
            Log().error(f"No se pudo abrir el reporte documentos {e}")
            time.sleep(2)
            raise

        # Ingreso de las propiedades del reporte
        # Ingreso de la clave correlativa del documento
        try:
            ctipodoc_fg_documentos = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_tipodoc)))
            ctipodoc_fg_documentos.send_keys(Configuracion.cod_tipo_doc_vco)
            time.sleep(2)

        except Exception as e:  # pragma: no cover
            Log().error(f"No se pudo ingresar el documento PM03 {e}")
            time.sleep(2)
            raise

        # Ingreso serie
        try:
            # Se ingresa la serie del documento
            cserie_fg_documentos = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_ayuda_serie)))
            cserie_fg_documentos.click()

            bserie_fg_documentos = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.buscar_art)))
            bserie_fg_documentos.send_keys(Configuracion.serie)
            time.sleep(2)

            bbusqueda_fg_documentos = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_busqueda)))
            bbusqueda_fg_documentos.click()
            time.sleep(2)

            serie_fg_documentos = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.txt_serie)))
            action \
                .double_click(serie_fg_documentos) \
                .pause(0) \
                .release()
            action.perform()
            time.sleep(2)

        except Exception as e:  # pragma: no cover
            Log().error(f"No se pudo ingresar la serie del documento {e}")
            time.sleep(2)
            raise

    # ---------------------------------- TABLA TIPO DE DOCUMENTOS -----------------------------------------------
    # Se ingresa a Tabla Tipos de documentos
    def tabla_tipo_documentos(self):
        try:
            tablas_fg_tipo_doc = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_tablas)))
            action \
                .click(tablas_fg_tipo_doc) \
                .pause(0) \
                .release()
            action.perform()

            tipos_doc_fg_tipo_doc = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_tipo_doc)))
            action \
                .move_to_element(tipos_doc_fg_tipo_doc) \
                .pause(0) \
                .release()
            action.perform()

            tipos_documentos_fg_tipo_doc = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.sub_menu_tipo_doc)))
            action \
                .click(tipos_documentos_fg_tipo_doc) \
                .release()
            action.perform()
            time.sleep(2)

        except Exception as e:  # pragma: no cover
            Log().error(f"El ingreso para Tipos de Documentos no fue correcto. {e}")
            raise

    # -----------------------------------TABLA RECARGO (TABLA DOCUMENTOS)------------------------------------------
    # Valida que la información del documento se encuentre en la tabla recargo
    def col_recargo(self):

        # Muestra el campo de recargo
        try:
            # El elemento deseado está dentro de un <iframe> por lo que hay que:
            # Inducir WebDriverWait para que el frame deseado esté disponible y cambiar a él.

            WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH, Configuracion.cambio_frame)))

            element_recargo = None
            xpathselector_recargo = Configuracion.columna_usuario  # Se ocupa la columna usuario para poder
            # visualizar la columna recargo

            if (not element_recargo) and (not xpathselector_recargo):
                return
            if xpathselector_recargo and (not element_recargo):
                element_recargo_1 = driver.find_element(By.XPATH, xpathselector_recargo)
                driver.execute_script(Argument_scroll, element_recargo_1)
            time.sleep(1)

            # Regresamos a la ventana principal
            driver.switch_to.default_content()

            Log().info(Log_docarti)

            time.sleep(1)

        except Exception as e:  # pragma: no cover
            Log().error(f"No se pudo encontrar el campo de recargo de Tabla Documentos {e}")
            time.sleep(2)
            raise

        # Cerrar ventana de reporte
        try:
            cierra_ventana_recargo = wait.until(
                EC.presence_of_element_located((By.XPATH, f"({Configuracion.btn_cerrar_ventana})[last()]")))
            cierra_ventana_recargo.click()
            time.sleep(1)

        except Exception as e:  # pragma: no cover
            Log().error(f'Log_cerrar_ventana {e}')
            time.sleep(2)
            raise

    # -----------------------------------TABLA DESCUENTO (TABLA DOCARTI)---------------------------------------
    # Valida que la información del documento se encuentre en la tabla recargo
    def col_descuento(self):

        # Muestra el campo de recargo
        try:
            # El elemento deseado está dentro de un <iframe> por lo que hay que:
            # Inducir WebDriverWait para que el frame deseado esté disponible y cambiar a él.

            WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH, Configuracion.cambio_frame)))

            element_descuento = None
            xpathselector_descuento = Configuracion.columna_combo  # Se ocupa la columna usuario para poder
            # visualizar la columna descuento

            if (not element_descuento) and (not xpathselector_descuento):
                return
            if xpathselector_descuento and (not element_descuento):
                element_descuento_1 = driver.find_element(By.XPATH, xpathselector_descuento)
                driver.execute_script(Argument_scroll, element_descuento_1)
            time.sleep(1)

            # Regresamos a la ventana principal
            driver.switch_to.default_content()

            Log().info(Log_docarti)

            time.sleep(1)

        except Exception as e:  # pragma: no cover
            Log().error(f"No se pudo encontrar el campo de recargo de Tabla Docarti {e}")
            time.sleep(2)
            raise

        # Cerrar ventana de reporte
        try:
            cierra_ventana_descuento = wait.until(
                EC.presence_of_element_located((By.XPATH, f"({Configuracion.btn_cerrar_ventana})[last()]")))
            cierra_ventana_descuento.click()
            time.sleep(1)

        except Exception as e:  # pragma: no cover
            Log().error(f"Log_cerrar_ventana {e}")
            time.sleep(2)
            raise

    # ---------------------------------TABLA CANTIDAD COMBO (TABLA DOCARTI)-----------------------------------
    # Valida que la información del documento se encuentre en la tabla recargo
    def col_combo(self):

        # Muestra el campo de recargo
        try:
            # El elemento deseado está dentro de un <iframe> por lo que hay que:
            # Inducir WebDriverWait para que el frame deseado esté disponible y cambiar a él.

            WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH, Configuracion.cambio_frame)))

            element_combo = None
            xpathselector_combo = Configuracion.columna_centro  # Se ocupa la columna centro costos para poder
            # visualizar la columna combo

            if (not element_combo) and (not xpathselector_combo):
                return
            if xpathselector_combo and (not element_combo):
                element_combo_1 = driver.find_element(By.XPATH, xpathselector_combo)
                driver.execute_script(Argument_scroll, element_combo_1)
            time.sleep(1)

            # Regresamos a la ventana principal
            driver.switch_to.default_content()

            Log().info(Log)

            time.sleep(1)

        except Exception as e:  # pragma: no cover
            Log().error(f"No se pudo encontrar el campo de recargo de Tabla Docarti combo {e}")
            time.sleep(2)
            raise

        # Cerrar ventana de reporte
        try:
            cierra_ventana_combo = wait.until(
                EC.presence_of_element_located((By.XPATH, f"({Configuracion.btn_cerrar_ventana})[last()]")))
            cierra_ventana_combo.click()
            time.sleep(1)

        except Exception as e:  # pragma: no cover
            Log().error(f'Log_cerrar_ventana {e}')
            time.sleep(2)
            raise

    # ---------------------------------PENDIENTE-------------------------------------------------------------

    def col_devolucion(self):
        # Muestra el campo de devolución
        try:
            # El elemento deseado está dentro de un <iframe> por lo que hay que:
            # Inducir WebDriverWait para que el frame deseado esté disponible y cambiar a él.
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, Configuracion.cambio_frame)))
            element = None
            xpathselector = Configuracion.columna_impofpag  # Se selecciona esta columna para visualizar devoluciones
            if (not element) and (not xpathselector):
                return
            if xpathselector and (not element):
                element = driver.find_element(By.XPATH, xpathselector)
                driver.execute_script('arguments[0].scrollIntoView()', element)
            time.sleep(1)

            # Regresamos a la ventana principal
            driver.switch_to.default_content()
        except Exception as e:
            Log().error(f" No se pudo acceder a la columna devolución del reporte docarti {e}")
            raise

        # Cerrar ventana de reporte
        try:
            cierra_ventana = wait.until(
                EC.presence_of_element_located((By.XPATH, f"({Configuracion.btn_cerrar_ventana})[last()]")))
            cierra_ventana.click()
            time.sleep(1)

        except Exception as e:
            Log().error(
                f"No se dio click al botón Cerrar de la ventana {e}")
            time.sleep(2)
            raise

    # ---------------------------------------- CANCELACIONES---------------------------------------------
    # Busca el menu de cancelaciones
    def cancelaciones(self):
        try:
            documentos_cancelaciones = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.menu_documentos)))
            action \
                .click(documentos_cancelaciones) \
                .pause(0) \
                .release()
            action.perform()

            cancelaciones = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_cancelaciones)))
            action \
                .click(cancelaciones) \
                .release()
            action.perform()
            time.sleep(2)
        except Exception as e:  # pragma: no cover
            Log().error(f"No se pudo ingresar a Cancelaciones {e}")
            raise

    # -------------------------------------RECIBO DE PAGO-----------------------------------------------
    # Busca el documento recibo de pago
    def recibo_pago(self):

        try:
            documentos_recibo_pago = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.menu_documentos)))
            action \
                .move_to_element(documentos_recibo_pago) \
                .pause(0) \
                .release()
            action.perform()

            clientes_recibo_pago = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_doc_clie)))
            action \
                .move_to_element(clientes_recibo_pago) \
                .pause(0) \
                .release()
            action.perform()

            mas_documentos_recibo_pago = wait.until(
                EC.presence_of_element_located((By.XPATH, Configuracion.menu_mas_doc)))
            action \
                .click(mas_documentos_recibo_pago) \
                .pause(0) \
                .release()
            action.perform()

            recibo_pago = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.doc_recibo_pago)))
            action \
                .click(recibo_pago) \
                .release()
            action.perform()
            time.sleep(2)
        except Exception as e:  # pragma: no cover
            Log().error(f"No se pudo ingresar a recibos de pago: {e}")
            raise
