import time
import unittest

from Pipeline1.FuncionesGral import *
from Pipeline1.VariablesGral import *
global numero_serie
global numero_documento


# ----------------------------- Funciones Unicas para VCO01--------------------------------------
def ingreso(self):
    try:
        ingreso_chrome()
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar correctamente a Chrome, favor de validar el error: {e}")
        raise
    try:
        funciones.ingresologin(self)
    except Exception as e:  # pragma: no cover
        Log().error(f" El ingreso al loggin no fue correcto, favor de validar el siguiente error: {e}")
        raise


def validar_articulos(self):
    try:
        tablas = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_tablas)))
        tablas.click()
    except Exception as e:  # pragma: no cover
        Log().error(f"No se ingreso al menú tablas, revisar el error: {e}")
        raise
    try:
        funciones.ingreso_tabla_articulos(self)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se ingreso a la tabla articulos, validar el error: {e}")
        raise
    try:

        articulo1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_codart)))
        articulo1.send_keys(Configuracion.codigo_art1_vco)
        Log().info(" Ingresa el codigo del articulo ")
        time.sleep(1)

        refresca = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_refresca)))
        refresca.click()
        Log().info(" Se presiona el boton 'Refrescar', para mostrar la informacion filtrada.")
        time.sleep(2)

        art1 = driver.find_element(By.XPATH, Configuracion.articulo1)
        action \
            .double_click(art1) \
            .pause(0) \
            .release()
        action.perform()
        time.sleep(3)

        cerrararticulo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_ventana1)))
        cerrararticulo.click()
        time.sleep(2)
        # ---------------------- Inicia la validación del articulo 2 --------------------------------------
        articulo2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_codart)))
        articulo2.click()
        articulo2.send_keys(Configuracion.codigo_art2_vco)
        Log().info(" Ingresa el codigo del articulo ")
        time.sleep(1)

        refresca = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_refresca)))
        refresca.click()
        Log().info(" Se presiona el boton 'Refrescar', para mostrar la informacion filtrada.")
        time.sleep(2)

        art2 = driver.find_element(By.XPATH, Configuracion.articulo2)
        action \
            .double_click(art2) \
            .pause(0) \
            .release()
        action.perform()
        time.sleep(3)

        cerrararticulo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_ventana1)))
        cerrararticulo.click()
        time.sleep(2)

        # ---------------------- Inicia la validación del articulo 3 --------------------------------------
        articulo3 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_codart)))
        articulo3.click()
        articulo3.send_keys(Configuracion.codigo_art3_vco)
        Log().info(" Ingresa el codigo del articulo ")
        time.sleep(1)

        refresca = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_refresca)))
        refresca.click()
        Log().info(" Se presiona el boton 'Refrescar', para mostrar la informacion filtrada.")
        time.sleep(2)

        art3 = driver.find_element(By.XPATH, Configuracion.articulo3)
        action \
            .double_click(art3) \
            .pause(0) \
            .release()
        action.perform()
        time.sleep(3)

        cerrar_articulo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_ventana1)))
        cerrar_articulo.click()
        time.sleep(2)

        cierra_ventana = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_ventana)))
        cierra_ventana.click()
        time.sleep(2)
        Log().info(" Se presiona el boton 'Cerrar', para cerrar la ventana")

    except Exception as e:  # pragma: no cover
        Log().error(f"No se validaron los articulos, favor de validar el error: {e}")
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

        precios = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_precios)))
        action \
            .click(precios) \
            .release()
        action.perform()
        Log().info("Ingresa a la pantalla de precios para realizar validación")
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().info(f" El ingreso para a la pantalla de precios no fue correcto, "
                   f"favor de validar el siguiente error: {e}")
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

        filtrocodigoarticulo = driver.find_element(By.XPATH, Configuracion.filtro_codart)
        action \
            .double_click(filtrocodigoarticulo) \
            .pause(0) \
            .release()
        action.perform()
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar al filtro, validar que la acción anterior haya finalizado: {e}")
        time.sleep(2)
        return False

    try:
        # Ingreso de articulo
        c_codigo_articulo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_codart)))
        c_codigo_articulo.send_keys(Configuracion.codigo_art1)
        Log().info(" Ingresa el codigo del articulo ")
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
        Log().info(" Se encontro y se dio clic en el filtro deseado")
        time.sleep(1)

        # Seleccionamos filtro codigo de lista de precios
        filtrocodigolistaprecios = driver.find_element(By.XPATH, Configuracion.filtro_codigo_listaprecios)
        action \
            .double_click(filtrocodigolistaprecios) \
            .pause(0) \
            .release()
        action.perform()
        Log().info(" Se encontro y se dio clic en el filtro deseado")
        time.sleep(1)

        # se agrega la lista de precios
        c_codigo_lista_precios = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_codlp)))
        c_codigo_lista_precios.click()
        c_codigo_lista_precios.send_keys(Configuracion.lista_precio)
        Log().info(" Ingresa el codigo de la lista de precios")
        time.sleep(1)

        refresca = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_refresca)))
        refresca.click()
        Log().info(" Se presiona el boton 'Refrescar', para mostrar la informacion filtrada.")
        time.sleep(1)

        ordenarcfecha = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.columna_fecha)))
        action \
            .click(ordenarcfecha) \
            .pause(1) \
            .click(ordenarcfecha) \
            .pause(0) \
            .release()
        action.perform()
        Log().info("Se realiza la validación del precio del artículo FA01001 en la pantalla precios")
        time.sleep(2)

        c_codigo_articulo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_codart)))
        c_codigo_articulo.click()
        time.sleep(0.5)
        c_codigo_articulo.send_keys(Configuracion.codigo_art1_vco)
        Log().info(" Ingresa el codigo del articulo ")
        time.sleep(1)

        refresca = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_refresca)))
        refresca.click()
        time.sleep(1)

        c_codigo_articulo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_codart)))
        c_codigo_articulo.click()
        c_codigo_articulo.send_keys(Configuracion.codigo_art2_vco)
        Log().info(" Ingresa el codigo del articulo ")
        time.sleep(1)

        refresca = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_refresca)))
        refresca.click()
        time.sleep(1)

        c_codigo_articulo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_codart)))
        c_codigo_articulo.click()
        c_codigo_articulo.send_keys(Configuracion.codigo_art3_vco)
        # Log().info(" Ingresa el codigo del articulo ")
        time.sleep(1)

        refresca = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_refresca)))
        refresca.click()
        time.sleep(1)

        cierra_todo = wait.until(EC.presence_of_element_located
                                 ((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[1]")))
        cierra_todo.click()
        Log().info(" Se presiona el boton 'Cerrar', para cerrar pantalla de documentos emitidos.")
        time.sleep(2)
        Log().info(" Se presiona el boton 'Cerrar', para cerrar la ventana")
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudieron validar correctamente los precios, favor de validar el error: {e}")
        raise


def validacion_dz1(self):
    try:
        funciones.ingresoreportes_dz(self)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar a reportes DZ, validar el error: {e}")
        raise

    try:
        # El elemento deseado está dentro de un <iframe> por lo que hay que:
        # Inducir al WebDriverWait para que el frame deseado esté disponible y cambiar a él.

        wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, Configuracion.frame_reporte1)))

        # Obtiene tabla de reporte de stock
        tablareporte = driver.find_element(By.XPATH, Configuracion.tabla_reporte1).get_attribute('outerHTML')
        stocktable_df = pd.read_html(StringIO(tablareporte))[0]

        # Hace una copia de la tabla, obteniendo solo las columnas de Codigo y Saldo
        df_stock = stocktable_df[['Codigo', 'Saldo']].copy()
        # Limpia la tabla
        df_stock = df_stock.dropna()
        df_stock = df_stock.drop(0)

        # Filtra por codigo de articulo
        stock_inicial = df_stock[(df_stock['Codigo'] == Configuracion.codigo_art22_vco)
                                 | (df_stock['Codigo'] == Configuracion.codigo_art4_vco)
                                 | (df_stock['Codigo'] == Configuracion.codigo_art6_vco)]

        # Resetea los index
        stock_inicial = stock_inicial.reset_index(drop=True)

        # Imprime el stock
        Log().info(f"El stock inicial de los articulos es: {stock_inicial}")

        # Regresamos a la ventana principal
        driver.switch_to.default_content()

    except Exception as e:  # pragma: no cover
        Log().error(f"No se obtuvo datos, favor de validar el error: {e}")   # pragma: no cover
        time.sleep(2)
        return False


def validacion_dz2():
    try:
        refresh_reporte1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_actualizareporte)))
        time.sleep(1)
        refresh_reporte1.click()
        time.sleep(5)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo actualizar el reporte DZ, validar el error: {e}")
        raise
    try:
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, Configuracion.frame_reporte1)))

        # Obtiene tabla de reporte de stock
        tabla_reporte2 = driver.find_element(By.XPATH, Configuracion.tabla_reporte1).get_attribute('outerHTML')
        stocktable_df = pd.read_html(StringIO(tabla_reporte2))[0]

        # Hace una copia de la tabla, obteniendo solo las columnas de Codigo y Saldo
        df_stock = stocktable_df[['Codigo', 'Saldo']].copy()
        # Limpia la tabla
        df_stock = df_stock.dropna()
        df_stock = df_stock.drop(0)

        # Filtra por codigo de articulo
        stock = df_stock[(df_stock['Codigo'] == Configuracion.codigo_art1_vco)
                         | (df_stock['Codigo'] == Configuracion.codigo_art2_vco)
                         | (df_stock['Codigo'] == Configuracion.codigo_art3_vco)]

        # Resetea los index
        stock = stock.reset_index(drop=True)

        # Imprime el stock
        Log().info(f"El stock de los articulos despues de la venta de contado es: {stock}")
        # print(stock)

        # Regresamos a la ventana principal
        driver.switch_to.default_content()
        time.sleep(1)

        cierra_reporte = wait.until(EC.presence_of_element_located
                                    ((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[1]")))
        cierra_reporte.click()
        Log().info(" Se presiona el boton 'Cerrar'")
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se obtuvo datos, validar el error: {e}")
        time.sleep(2)
        return False


def datos_vco(self):
    try:
        funciones.venta_contado(self)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo acceder al documento venta de contado: {e}")
        raise
    try:
        cliente = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cliente)))
        cliente.send_keys(Configuracion.cuenta1)
        time.sleep(1)
        Log().info("Se agregar al cliente 0010051428 para realizar la venta de contado por packing")

        observaciones1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_obs1)))
        observaciones1.send_keys(Configuracion.i_observaciones1)
        time.sleep(1)
        Log().info("Se ingresa la observación al documento")

        observaciones2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_obs2)))
        observaciones2.send_keys(Configuracion.i_observaciones_vc1)
        time.sleep(1)
        Log().info("Se ingresa la observación al documento")

        agrega_item = wait.until(EC.element_to_be_clickable((By.XPATH, Configuracion.btn_agrega_item)))
        agrega_item.click()
        agrega_item.click()

        articulo1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        articulo1.send_keys(Configuracion.codigo_art1_vco)
        Log().info(" Ingresa articulo 1")
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar los datos al documento Venta de contado, validar el error: {e}")
        raise

    try:
        try:
            # AtributoPrecio = self.driver.find_elements(By.XPATH, Configuracion.precio_venta).is_displayed()
            atributo_precio = WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.XPATH, Configuracion.precio_venta)))

            if atributo_precio.is_displayed():
                Log().info("El precio unitario está en pantalla")

        except Exception as e:  # pragma: no cover
            Log().error(f"No se encontro el precio unitario {e}")
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
                Log().info("Se agrega el atributo precio unitario")

            except Exception as e:  # pragma: no cover
                Log().info(f"No se logro agregar el atributo precio unitario, error {e}")
                pass

    except Exception as e:  # pragma: no cover
        Log().info(f"No se encontró el atributo precio unitario, favor de validar el error: {e}")
        time.sleep(2)
        driver.quit()
        return False

    try:
        c_cantidad1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        time.sleep(1)
        c_cantidad1.click()
        time.sleep(1)
        c_cantidad1.send_keys(Configuracion.cantidad_art1)
        Log().info(" Ingresa la cantidad del articulo ")

        aceptar1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        time.sleep(1)
        aceptar1.click()
        Log().info(" Se presiona el boton 'Aceptar', para ingresar el articulo y la cantidad.")
        time.sleep(2)

        # ----------------------------------- Ingreso articulo 2 -------------------------------------------
        articulo2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        time.sleep(1)
        articulo2.send_keys(Configuracion.codigo_art2_vco)
        Log().info(" Ingresa articulo 2")
        time.sleep(1)

        c_cantidad2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        time.sleep(1)
        c_cantidad2.click()
        time.sleep(1)
        c_cantidad2.send_keys(Configuracion.cantidad_art1)
        Log().info(" Ingresa la cantidad del articulo ")

        aceptar2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        time.sleep(1)
        aceptar2.click()
        Log().info(" Se presiona el boton 'Aceptar', para ingresar el articulo y la cantidad.")
        time.sleep(2)

        # ------------------------------------- Ingreso articulo 3 -----------------------------------------
        articulo3 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        time.sleep(1)
        articulo3.send_keys(Configuracion.codigo_art3_vco)
        Log().info(" Ingresa articulo 3")
        time.sleep(1)

        c_cantidad3 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        c_cantidad3.click()
        time.sleep(1)
        c_cantidad3.send_keys(Configuracion.cantidad_art1)
        Log().info(" Ingresa la cantidad del articulo ")

        aceptar3 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        time.sleep(1)
        aceptar3.click()
        Log().info(" Se presiona el boton 'Aceptar', para ingresar el articulo y la cantidad.")
        time.sleep(2)

        cancelar = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cancelar)))
        time.sleep(1)
        cancelar.click()
        Log().info(" Se presiona el boton 'Cancelar', para mostrar la informacion del reporte.")
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar la cantidad al atributo, favor de validar el error: {e}")
        raise


def impuesto_venta(self):
    try:
        info_venta = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_info_art)))
        info_venta.click()
        Log().info("Se da click a la información a detalle de la venta de contado")
        time.sleep(2)

        valida_iva = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.iva_venta_contado1))).text
        self.assertEqual("252.14", valida_iva, "El IVA es correcto")
        Log().info("El IVA de la venta es correcto: 252.14")
        time.sleep(1)

        valida_total = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.total_venta_contado1))).text
        self.assertEqual("1,828.04", valida_total, "El total es correcto")
        Log().info("El total de la venta es correcto: 1,828.04")
        time.sleep(1)

        cerrar_info = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar)))
        cerrar_info.click()
        Log().info("Se cierra información a detalle de la venta de contado")

        # Guarda el documento venta de contado
        guarda = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_guarda)))
        time.sleep(1)
        guarda.click()
        Log().info(" Se da clic en el boton Guardar; se emite el documento.")

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar al impuesto de venta del documento, validar el error: {e}")
        raise


def documento_emitido(self):
    try:
        funciones.documentos_emitidos(self)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logro ejecutar la funcion documentos_emitidos {e}")
        raise
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
        Log().info(" Se encontro y abrio el documento emitido ")
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().info(f"No se encontro el documento emitido {e}")
        raise

    # Obtiene valores de numero de serie y numero de documento
    try:
        valores_documento = wait.until(
            EC.presence_of_element_located((By.XPATH, f"({Configuracion.titulo_pantalla})[2]"))).text
        time.sleep(1)
        valores_documento_separados = valores_documento.split()

        global numero_serie, numero_documento
        numero_serie = valores_documento_separados[-2]
        numero_documento = valores_documento_separados[-1]
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudieron obtener los datos del documento, validar el error: {e}")
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
        Log().info(" Se encontro y abrio el documento emitido ")
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo encontrar el documento emitido, favor de validar el error: {e}")
        raise

    try:
        cierra_todo = wait.until(EC.presence_of_element_located
                                 ((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[2]")))
        cierra_todo.click()
        Log().info(" Se presiona el boton 'Cerrar', para cerrar el documento emitido")
        time.sleep(2)

        cierra_todo = wait.until(EC.presence_of_element_located
                                 ((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[1]")))
        cierra_todo.click()
        Log().info(" Se presiona el boton 'Cerrar', para cerrar pantalla de documentos emitidos.")
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se encontró el botón 'Cerrar', favor de validar el error: {e}")
        raise


# ---------------------------------- Inicio de la automatización DCO01---------------------------------------------

class Test(unittest.TestCase):

    def test_000(self):
        """Ingreso a Chrome"""
        return ingreso(self)

    def test_001(self):
        """Validación de articulos"""
        return validar_articulos(self)

    def test_002(self):
        """Validación de precios"""
        return validacion_precios()

    def test_003(self):
        """Validación del reporte DZ"""
        return validacion_dz1(self)

    def test_004(self):
        """Ingreso de datos en venta de contado"""
        return datos_vco(self)

    def test_005(self):
        """Validar precios en el articulo"""
        return impuesto_venta(self)

    def test_006(self):
        """Validación de reporte DZ"""
        return validacion_dz2()

    def test_007(self):
        """Se abre el documento emitido"""
        return documento_emitido(self)
