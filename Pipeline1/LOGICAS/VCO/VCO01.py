import unittest

from Pipeline1.FuncionesGral import *
from Pipeline1.VariablesGral import *

Log_aceptar = "Se presiona el boton 'Aceptar', para ingresar el articulo y la cantidad."
Log_cantidad = "Se ingresa la cantidad del articulo = 1."
Log_refrescar = "Se presiona el boton 'Refrescar', para mostrar la informacion filtrada."


# ----------------------------- Funciones Unicas para VCO01--------------------------------------
def validar_articulos():
    try:

        articulo1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_codart)))
        articulo1.send_keys(Configuracion.codigo_art1)
        Log().info("Ingresa el codigo del articulo FA01001")
        time.sleep(1)

        refresca_art1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_refresca)))
        refresca_art1.click()
        Log().info(Log_refrescar)
        time.sleep(2)

        art1 = driver.find_element(By.XPATH, Configuracion.articulo1)
        action \
            .double_click(art1) \
            .pause(0) \
            .release()
        action.perform()
        time.sleep(3)

        cerrar_articulo_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_ventana1)))
        cerrar_articulo_1.click()
        time.sleep(2)
        # ---------------------- Inicia la validación del articulo 2 --------------------------------------
        articulo2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_codart)))
        articulo2.click()
        articulo2.send_keys(Configuracion.codigo_art4)
        time.sleep(1)

        refresca_4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_refresca)))
        refresca_4.click()
        time.sleep(2)

        art2 = driver.find_element(By.XPATH, Configuracion.articulo4)
        action \
            .double_click(art2) \
            .pause(0) \
            .release()
        action.perform()
        time.sleep(3)

        cerrar_articulo_4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_ventana1)))
        cerrar_articulo_4.click()
        time.sleep(2)

        # ---------------------- Inicia la validación del articulo 3 --------------------------------------
        articulo3 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_codart)))
        articulo3.click()
        articulo3.send_keys(Configuracion.codigo_art5)
        time.sleep(1)

        refresca_5 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_refresca)))
        refresca_5.click()
        time.sleep(2)

        art3 = driver.find_element(By.XPATH, Configuracion.articulo5)
        action \
            .double_click(art3) \
            .pause(0) \
            .release()
        action.perform()
        time.sleep(3)

        cerrararticulo_5 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_ventana1)))
        cerrararticulo_5.click()
        time.sleep(2)

        cierra_ventana_articulos = wait.until(
            EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_ventana)))
        cierra_ventana_articulos.click()

    except Exception as e:  # pragma: no cover
        Log().error(f"No se validaron los articulos {e}")
        raise


def validacion_precios():
    try:
        tablas = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_tablas)))
        action \
            .move_to_element(tablas) \
            .pause(0) \
            .release()
        action.perform()

        tabla_lista_precios = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_lista_pre)))
        action \
            .move_to_element(tabla_lista_precios) \
            .pause(0) \
            .release()
        action.perform()

        menu_precios = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_precios)))
        action \
            .click(menu_precios) \
            .release()
        action.perform()
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f" El ingreso para a la pantalla de precios no fue correcto. {e}")
        time.sleep(2)
        return False

    # Ingreso al filtro de articulos
    try:
        c_filtro = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.filtro_art)))
        c_filtro.click()
        time.sleep(1)

        buscar_cod = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.buscar_cod)))
        action \
            .click(buscar_cod) \
            .send_keys("C") \
            .send_keys("C") \
            .pause(0) \
            .release()
        action.perform()
        time.sleep(1)

        filtrocodarticulo = driver.find_element(By.XPATH, Configuracion.filtro_codart)
        action \
            .double_click(filtrocodarticulo) \
            .pause(0) \
            .release()
        action.perform()
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar al filtro {e}")
        time.sleep(2)
        return False

    try:
        # Ingreso de articulo
        c_codigo_articulo_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_codart)))
        c_codigo_articulo_1.send_keys(Configuracion.codigo_art1)
        time.sleep(1)

        # Bajamos hasta el filtro
        filtrocodigoarticulo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.filtro_codart)))
        action \
            .click(filtrocodigoarticulo) \
            .pause(0) \
            .send_keys("L") \
            .send_keys("L") \
            .pause(0) \
            .release()
        action.perform()

        # Desplegamos el filtro
        filtrolistaprecios = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.filtro_listaprecios)))
        action \
            .double_click(filtrolistaprecios) \
            .pause(0) \
            .send_keys(Keys.SPACE) \
            .release()
        action.perform()
        time.sleep(1)

        # Seleccionamos filtro codigo de lista de precios
        filtrocodigolistaprecios = driver.find_element(By.XPATH, Configuracion.filtro_codigo_listaprecios)
        action \
            .double_click(filtrocodigolistaprecios) \
            .pause(0) \
            .release()
        action.perform()
        time.sleep(1)

        # se agrega la lista de precios
        c_codigo_lista_precios = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_codlp)))
        c_codigo_lista_precios.click()
        c_codigo_lista_precios.send_keys(Configuracion.lista_precio)
        time.sleep(1)

        refresca_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_refresca)))
        refresca_1.click()
        time.sleep(1)

        ordenarcfecha = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.columna_fecha)))
        action \
            .click(ordenarcfecha) \
            .pause(0) \
            .double_click(ordenarcfecha) \
            .pause(0) \
            .release()
        action.perform()
        Log().info("Se realiza la validación del precio del artículo FA01001 en la pantalla precios")
        time.sleep(2)

        c_codigo_articulo_4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_codart)))
        c_codigo_articulo_4.click()
        time.sleep(0.5)
        c_codigo_articulo_4.send_keys(Configuracion.codigo_art4)
        time.sleep(1)

        refresca_2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_refresca)))
        refresca_2.click()
        time.sleep(1)

        c_codigo_articulo_5 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_codart)))
        c_codigo_articulo_5.click()
        c_codigo_articulo_5.send_keys(Configuracion.codigo_art5)
        time.sleep(1)

        refresca_3 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_refresca)))
        refresca_3.click()
        time.sleep(1)

        cierra_ventana = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_ventana)))
        cierra_ventana.click()
    except Exception as e:  # pragma: no cover
        Log().error(f"No se encontraron los articulos ingresados {e}")
        raise


def datos_vco():
    try:
        cliente = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cliente)))
        cliente.send_keys(Configuracion.cuenta1)
        time.sleep(1)
        Log().info("Se agregar al cliente 0010051428 para realizar la venta de contado por packing")

        observaciones1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_obs1)))
        observaciones1.send_keys(Configuracion.i_observaciones1)
        time.sleep(1)

        observaciones2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_obs2)))
        observaciones2.send_keys(Configuracion.i_observaciones_vc1)
        time.sleep(1)

        agrega_item = wait.until(EC.element_to_be_clickable((By.XPATH, Configuracion.btn_agrega_item)))
        agrega_item.click()
        agrega_item.click()

        articulo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        articulo.send_keys(Configuracion.codigo_art1)
        Log().info(f"Ingresa articulo {Configuracion.codigo_art1}")
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar los datos al documento Venta de contado {e}")
        raise

    try:
        try:
            atributo_precio = WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.XPATH, Configuracion.precio_venta)))

            if atributo_precio.is_displayed():
                Log().info("El precio unitario está en pantalla")

        except Exception as e:  # pragma: no cover
            Log().error(f"El precio unitario no aparece en pantalla {e}")
            # Configura el atributo
            try:
                agrega_atributo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_atributos)))
                time.sleep(1)
                agrega_atributo.click()
                time.sleep(1)

                atributo_precio_unitario = wait.until(
                    EC.presence_of_element_located((By.XPATH, Configuracion.atributo_precio)))
                time.sleep(1)
                atributo_precio_unitario.click()
                time.sleep(1)

                cerrar_atributo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar2)))
                time.sleep(1)
                cerrar_atributo.click()
                time.sleep(1)

            except Exception as e:  # pragma: no cover
                Log().error(f"No se logró agregar el atributo precio unitario, error {e}")

    except Exception as e:  # pragma: no cover
        Log().error(f"No se encontró el atributo precio unitario {e}")
        time.sleep(2)
        driver.quit()
        return False

    try:
        c_cantidad_vco_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        time.sleep(1)
        c_cantidad_vco_1.click()
        time.sleep(1)
        c_cantidad_vco_1.send_keys(Configuracion.cantidad1)
        Log().info(Log_cantidad)

        aceptar_vco_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        time.sleep(1)
        aceptar_vco_1.click()
        Log().info(Log_aceptar)
        time.sleep(2)

        # ----------------------------------- Ingreso articulo 2 -------------------------------------------
        articulo_vco_4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        time.sleep(1)
        articulo_vco_4.send_keys(Configuracion.codigo_art4)
        Log().info(f"Ingresa articulo {Configuracion.codigo_art4}")
        time.sleep(1)

        c_cantidad_vco_4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        time.sleep(1)
        c_cantidad_vco_4.click()
        time.sleep(1)
        c_cantidad_vco_4.send_keys(Configuracion.cantidad1)
        Log().info(Log_cantidad)

        aceptar_vco_4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        time.sleep(1)
        aceptar_vco_4.click()
        Log().info(Log_aceptar)
        time.sleep(2)

        # ------------------------------------- Ingreso articulo 3 -----------------------------------------
        articulo_vco_5 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        time.sleep(1)
        articulo_vco_5.send_keys(Configuracion.codigo_art5)
        Log().info(f"Ingresa articulo {Configuracion.codigo_art5}")
        time.sleep(1)

        c_cantidad_vco_5 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        c_cantidad_vco_5.click()
        time.sleep(1)
        c_cantidad_vco_5.send_keys(Configuracion.cantidad1)
        Log().info(Log_cantidad)

        aceptar_vco_5 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        time.sleep(1)
        aceptar_vco_5.click()
        Log().info(Log_aceptar)
        time.sleep(2)

        cancelar_vco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cancelar)))
        time.sleep(1)
        cancelar_vco.click()
        Log().info("Se presiona el boton 'Cancelar', para mostrar la informacion del reporte.")
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudieron ingresar correctamente los 3 artículos: FA01001, FA01005 y FA01009. {e}")
        raise


def impuesto_venta(self):
    try:
        info_venta = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_info_art)))
        info_venta.click()
        Log().info("Se da click a la información a detalle de la venta de contado")
        time.sleep(2)

        valida_importe = wait.until(
            EC.presence_of_element_located((By.XPATH, Configuracion.importe_venta_contado1))).text
        self.assertEqual("1,575.90", valida_importe, "El Importe es correcto")
        Log().info("El Importe de la venta es correcto")
        time.sleep(1)

        valida_iva = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.iva_venta_contado1))).text
        self.assertEqual("252.14", valida_iva, "El IVA es correcto")
        Log().info("El IVA de la venta es correcto")
        time.sleep(1)

        valida_total = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.total_venta_contado1))).text
        self.assertEqual("1,828.04", valida_total, "El total es correcto")
        Log().info("El total de la venta es correcto")
        time.sleep(1)

        cerrar_info = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar)))
        cerrar_info.click()
        Log().info("Se cierra información a detalle de la venta de contado")

        # Guarda el documento venta de contado
        guarda = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_guarda)))
        time.sleep(1)
        guarda.click()
        Log().info("Se da clic en el boton Guardar y se emite el documento.")

    except Exception as e:  # pragma: no cover
        Log().error(f"El detalle del cálculo del documento no coincide {e}")
        raise


def documento_emitido():
    try:
        busqueda_docemitido = wait.until(
            EC.presence_of_element_located((By.XPATH, Configuracion.busqueda_odocemitido)))
        action \
            .click(busqueda_docemitido) \
            .pause(0) \
            .double_click(busqueda_docemitido) \
            .pause(1) \
            .double_click(busqueda_docemitido) \
            .release()
        action.perform()
        Log().info("Se encontró el documento emitido ")
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo abrir documentos emitidos {e}")
        raise

    # Obtiene valores de numero de serie y numero de documento
    try:
        valores_documento = wait.until(
            EC.presence_of_element_located((By.XPATH, f"({Configuracion.titulo_pantalla})[3]"))).text
        time.sleep(1)
        valores_documento_separados = valores_documento.split()

        global numero_serie, numero_documento
        numero_serie = valores_documento_separados[-2]
        numero_documento = valores_documento_separados[-1]
    except Exception as e:  # pragma: no cover
        Log().error(f"No se obtuvieron los valores del documento emitido {e}")
        raise

    try:
        doc_emitido = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.info_doc)))
        action \
            .click(doc_emitido) \
            .pause(0) \
            .send_keys(Keys.ARROW_DOWN) \
            .pause(0) \
            .send_keys(Keys.ARROW_DOWN) \
            .pause(0) \
            .release()
        action.perform()
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se visualizó correctamente la información del documento emitido {e}")
        raise

    try:
        cierra_todo1 = wait.until(EC.presence_of_element_located
                                  ((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[3]")))
        cierra_todo1.click()
        Log().info("Se presiona el boton 'Cerrar', para cerrar el documento de venta.")
        time.sleep(2)

        cierra_todo = wait.until(EC.presence_of_element_located
                                 ((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[2]")))
        cierra_todo.click()
        Log().info("Se presiona el boton 'Cerrar', para cerrar pantalla de documentos emitidos.")
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se cerraron correctamente las ventanas {e}")
        raise


def num_doc():
    try:
        c_numero_doc = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_numero_doc)))
        c_numero_doc.send_keys(numero_documento)
        Log().info("Ingresa el numero de documento ")
        time.sleep(1)

        ver = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_ver)))
        ver.click()
        Log().info("Se presiona el boton 'Ver', para mostrar la informacion del reporte.")
        time.sleep(4)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar el número de documento. {e}")
        raise


# ---------------------------------- Inicio de la automatización VCO01---------------------------------------------
class Test(unittest.TestCase):

    def test_000(self):
        """Ingreso a Chrome"""
        return ingreso_chrome()

    def test_001(self):
        """Ingreso a Power Street"""
        return funciones.ingresologin(self)

    def test_002(self):
        """Ingreso a articulos"""
        menu_tablas = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_tablas)))
        menu_tablas.click()
        return funciones.ingreso_tabla_articulos(self)

    def test_003(self):
        """Validación de articulos"""

        return validar_articulos()

    def test_004(self):
        """Validación de precios"""
        return validacion_precios()

    def test_005(self):
        """Ingreso a Reportes DZ"""
        return funciones.ingresoreportes_dz(self)

    def test_006(self):
        """Ingreso Venta de Contado"""
        return funciones.venta_contado(self)

    def test_007(self):
        """Ingreso de datos en venta de contado"""
        return datos_vco()

    def test_008(self):
        """Validar precios en el articulo"""
        return impuesto_venta(self)

    def test_009(self):
        """Reingreso a reportes DZ"""
        return funciones.reingreso_reporte_dz(self)

    def test_011(self):
        """Se ingresa a documentos emitidos"""
        return funciones.documentos_emitidos(self)

    def test_012(self):
        """Se abre el documento emitido"""
        return documento_emitido()

    def test_013(self):
        """Se ingresa al reporte Docarti"""
        return funciones.tabla_docarti_vco(self)

    def test_014(self):
        """Se ingresa el número de documento"""
        return num_doc()
