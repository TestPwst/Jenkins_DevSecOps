import unittest

from Pipeline1.FuncionesGral import *
from Pipeline1.VariablesGral import *

emitido = " Se encontró y abrió el documento emitido "
log_aceptar = " Se presiona el boton 'aceptar', para ingresar el articulo y la cantidad."
log_observaciones = "Se ingresa la observación al documento"

# ----------------------------- Funciones Unicas para DCO05--------------------------------------

def validacion_dz():
    # Obtiene datos del saldo del reporte de stock de los articulos
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Configuracion.frame_reporte1)))
        # Obtiene tabla de reporte de stock
        tabla_reporte = driver.find_element(By.XPATH, Configuracion.tabla_reporte1).get_attribute('outerHTML')
        stocktable_df = pd.read_html(StringIO(tabla_reporte))[0]

        # Hace una copia de la tabla, obteniendo solo las columnas de Codigo y Saldo
        df_stock = stocktable_df[['Codigo', 'Saldo']].copy()

        # Limpia la tabla
        df_stock = df_stock.dropna()
        df_stock = df_stock.drop(0)

        # Filtra por codigo de articulo
        stock_inicial = df_stock[(df_stock['Codigo'] == Configuracion.codigo_art1_vco) |
                                 (df_stock['Codigo'] == Configuracion.codigo_art22_vco)]

        # Resetea los index
        stockinicial = stock_inicial.reset_index(drop=True)

        # Imprime el stock
        Log().info("El stock inicial de los articulos es:")
        print(stockinicial)

        # Regresamos a la ventana principal
        driver.switch_to.default_content()

    except Exception as e:  # pragma: no cover
        Log().error(f"No se obtuvo datos. : {e}")
        time.sleep(2)
        return False


def datos_vco():
    # Ingreso de informacion a la venta
    # Ingreso cliente
    try:
        ccliente = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cliente)))
        ccliente.send_keys(Configuracion.cuenta)
        time.sleep(2)
        Log().info("Se agregar al cliente 125H000057 para realizar la venta de contado por combo componente")

        observaciones1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_obs1)))
        observaciones1.send_keys(Configuracion.i_observaciones1)
        time.sleep(1)
        Log().info(log_observaciones)

        observaciones2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_obs2)))
        observaciones2.send_keys(Configuracion.i_observaciones_vc5)
        time.sleep(1)
        Log().info(log_observaciones)

        # Da clic en agregar

        agrega_item = wait.until(EC.element_to_be_clickable((By.XPATH, Configuracion.btn_agrega_item)))
        agrega_item.click()
        agrega_item.click()
        # Ingreso articulo 1

        carticulo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        carticulo.send_keys(Configuracion.codigo_art1_vco)
        Log().info(f" Ingresa articulo {Configuracion.codigo_art1_vco} ")
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar el articulo: {e}")
        time.sleep(2)
        raise

    try:
        try:
            atributo_precio = WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.XPATH, Configuracion.precio_venta)))

            if atributo_precio.is_displayed():
                Log().info("El precio unitario está en pantalla")

        except Exception as e:  # pragma: no cover
            Log().error(f"No se pudo validar el precio: {e}")
            # Configura el atributo
            try:
                agrega_atributo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_atributos)))
                agrega_atributo.click()
                time.sleep(1)

                atributo_precio_unitario = wait.until(
                    EC.presence_of_element_located((By.XPATH, Configuracion.atributo_precio)))
                atributo_precio_unitario.click()
                time.sleep(1)

                cerrar_atributo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar2)))
                cerrar_atributo.click()
                time.sleep(1)
            # Log().info("Se agrega el atributo precio unitario")

            except Exception as e:  # pragma: no cover
                Log().error(f"No se logro agregar el atributo precio unitario, error: {e}")
                pass

    except Exception as e:  # pragma: no cover
        Log().error(f"No se encontró el atributo precio unitario: {e}")
        time.sleep(2)
        raise

    # Ingreso de cantidad del articulo
    try:
        ccantidad = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        ccantidad.click()
        time.sleep(1)
        ccantidad.send_keys(Configuracion.cantidad_art1)
        Log().info(f"Cantidad del artículo {Configuracion.cantidad_art1}")

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar la cantidad del articulo, verificar error: {e}")
        time.sleep(2)
        raise

    # Da clic en aceptar
    try:
        aceptar = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        aceptar.click()
        Log().info(log_aceptar)
        time.sleep(3)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se dio click al botón aceptar, verificar error: {e}")
        time.sleep(2)
        raise

    # ingreso de articulo 2
    try:
        carticulo2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        carticulo2.send_keys(Configuracion.codigo_art22_vco)
        Log().info(f" Ingresa articulo {Configuracion.codigo_art22_vco} ")
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"Error al ingresar el articulo: {e}")
        time.sleep(2)
        raise

    # Ingreso de cantidad del articulo
    try:
        ccantidad2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        ccantidad2.click()
        time.sleep(2)
        ccantidad2.send_keys(Configuracion.cantidad_art1)
        Log().info(f"Cantidad del artículo {Configuracion.cantidad_art1}")

    except Exception as e:  # pragma: no cover
        Log().error(f"Error al ingresar cantidad de artículo: {e}")
        time.sleep(2)
        raise

    # Da clic en aceptar
    try:
        aceptar2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        aceptar2.click()
        Log().info(log_aceptar)
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"Error en click al botón aceptar: {e}")
        time.sleep(2)
        raise

    # ingreso de articulo 3
    try:
        carticulo3 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        carticulo3.send_keys(Configuracion.codigo_art_combo)
        Log().info(f" Ingresa articulo {Configuracion.codigo_art_combo} ")
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se ingresó el articulo, validar error: {e}")
        time.sleep(2)
        raise

    # Ingreso de cantidad del articulo
    try:
        ccantidad3 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        ccantidad3.click()
        time.sleep(1)
        ccantidad3.send_keys(Configuracion.cantidad_art1)
        Log().info(" Ingresa la cantidad del articulo ")

    except Exception as e:  # pragma: no cover
        Log().error(f"Error al ingresar la cantidad del articulo, validar erorr: {e}")
        time.sleep(2)
        raise

    # Da clic en aceptar
    try:
        aceptar3 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        aceptar3.click()
        Log().info(log_aceptar)
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se dio click al botón aceptar, validar error: {e}")
        time.sleep(2)
        raise

    # Da clic en cancelar para cerrar el ingreso de articulos
    try:
        cancelar = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cancelar)))
        cancelar.click()
        Log().info(" Se presiona el boton 'cancelar', para mostrar la informacion del reporte.")
        time.sleep(3)

    except Exception as e:  # pragma: no cover
        Log().error(f"Error en click al botón cancelar {e}")
        time.sleep(2)
        raise


def impuesto_venta(self):
    # Se abre el detalle del calculo del documento
    try:
        info_venta = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_info_art)))
        info_venta.click()
        Log().info("Se da click a la información a detalle de la venta356")
        time.sleep(2)

        valida_iva = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.ivaventadev))).text
        self.assertEqual("299.89", valida_iva, "El IVA es correcto")
        Log().info("El IVA de la venta es correcto")
        time.sleep(1)

        valida_total = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.totalventadev))).text
        self.assertEqual("2,174.19", valida_total, "El total es correcto")
        Log().info("El total de la venta es correcto")
        time.sleep(1)

        cerrar_info = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar)))
        cerrar_info.click()
        Log().info("Se cierra información a detalle de la venta de contado")

        guarda = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_guarda)))
        time.sleep(1)
        guarda.click()
        Log().info(" Se da clic en el boton Guardar; se emite el documento.")
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"Error en click al botón Guardar: {e}")
        raise


def documento_emitido():
    try:
        busqueda_docemitido = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.busqueda_odocemitido)))
        action \
            .click(busqueda_docemitido) \
            .pause(0) \
            .double_click(busqueda_docemitido) \
            .pause(1) \
            .double_click(busqueda_docemitido) \
            .release()
        action.perform()
        Log().info(emitido)
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se encontró el documento emitido, verificar error {e}")
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
        Log().info(emitido)
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se encontró el documento emitido, validar: {e}")
        raise

    try:
        cierra_todo1 = wait.until(EC.presence_of_element_located
                                  ((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[3]")))
        cierra_todo1.click()
        Log().info(" Se presiona el boton 'Cerrar', para cerrar el documento de venta.")
        time.sleep(2)
        #
        # Cierra_todo = wait.until(EC.presence_of_element_located
        # 						 ((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[2]")))
        # Cierra_todo.click()
        # Log().info(" Se presiona el boton 'Cerrar', para cerrar pantalla de documentos emitidos 423.")
        # time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se encontraron ventanas a cerrar: {e}")
        raise


def documento_emitido2():
    try:
        busqueda_docemitido2 = wait.until(
            EC.presence_of_element_located((By.XPATH, Configuracion.busqueda_odocemitido2)))
        action \
            .click(busqueda_docemitido2) \
            .pause(0) \
            .double_click(busqueda_docemitido2) \
            .pause(1) \
            .double_click(busqueda_docemitido2) \
            .release()
        action.perform()
        Log().info(emitido)
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo encontrar documento, favor de validar el error: {e}")
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
        Log().error(f"No se pudo obtener valores, favor de validar el error: {e}")
        raise

    try:
        doc_emitido2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.info_doc)))
        action \
            .click(doc_emitido2) \
            .pause(0) \
            .send_keys(Keys.ARROW_DOWN) \
            .pause(0) \
            .send_keys(Keys.ARROW_DOWN) \
            .pause(0) \
            .release()
        action.perform()
        Log().info(emitido)
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se encontro doc emitido, favor de validar el error: {e}")
        raise

    try:
        cierra_todo2 = wait.until(EC.presence_of_element_located
                                  ((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[3]")))
        cierra_todo2.click()
        Log().info(" Se presiona el boton 'Cerrar', para cerrar el documento de venta")
        time.sleep(2)

        cierra_todo_em2 = wait.until(EC.presence_of_element_located
                                     ((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[2]")))
        cierra_todo_em2.click()
        Log().info(" Se presiona el boton 'Cerrar', para cerrar pantalla de documentos emitidos.")
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"Error al cerrar, favor de validar el error: {e}")
        raise


def devolucion_contado():
    # Busca el documento que creamos y abre el menú
    try:
        busqueda_docemitido_dc = wait.until(
            EC.presence_of_element_located((By.XPATH, Configuracion.busqueda_odocemitido)))
        busqueda_docemitido_dc.click()
        action \
            .click(busqueda_docemitido_dc) \
            .pause(0) \
            .context_click(busqueda_docemitido_dc) \
            .pause(0) \
            .release()
        action.perform()
        Log().info(" Se encontró el documento de venta ")
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se encontró/abrió el menú: {e}")
        time.sleep(2)
        raise

    # Da clic en Generar nuevo documento
    try:
        generar_nuevo_doc = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_generar_nuevo_doc)))
        time.sleep(1)
        generar_nuevo_doc.click()

    except Exception as e:  # pragma: no cover
        Log().error(f"No se dio clic en generar nuevo documento: {e}")
        time.sleep(2)
        raise

    # Ingresa el tipo de documento a generar
    try:
        ctipo_doc = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_tipodoc_generar)))
        time.sleep(2)
        ctipo_doc.send_keys(Configuracion.cod_tipo_doc_dco)
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar el tipo de documento: {e}")
        time.sleep(2)
        raise

    # Da clic en aceptar
    try:
        aceptar_dc = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        aceptar_dc.click()
        aceptar_dc.click()
        Log().info(" Genera nuevo Documento Venta Contado a partir de la Venta Pendiente y lo emite")
        time.sleep(4)

        doc_emitido_dc = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.info_doc)))
        doc_emitido_dc.click()
        doc_emitido_dc.click()
        Log().info("click en documento de venta")
        time.sleep(2)

        observaciones1_dc = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_obs1)))
        observaciones1_dc.clear()
        observaciones1_dc.send_keys(Configuracion.i_observaciones2)
        time.sleep(1)
        Log().info(log_observaciones)

        observaciones2_dc = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_obs2)))
        observaciones2_dc.clear()
        observaciones2_dc.send_keys(Configuracion.i_observaciones_dco5)
        time.sleep(1)
        Log().info(log_observaciones)

        tab_items = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.items_doc)))
        tab_items.click()
        Log().info("se dió clic en items")

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró dar click en el botón aceptar: {e}")
        time.sleep(2)
        raise


def num_doc():
    try:
        cnumerodoc = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_numero_doc)))
        cnumerodoc.send_keys(numero_documento)
        Log().info(" Ingresa el numero de documento ")
        time.sleep(1)

        ver = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_ver1)))
        ver.click()
        Log().info(" Se presiona el boton 'ver', para mostrar la informacion del reporte.")
        time.sleep(5)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se colocaron datos en reporte / click en ver {e}")
        raise

    # Muestra el campo de combo
    try:
        # El elemento deseado está dentro de un <iframe> por lo que hay que:
        # Inducir WebDriverWait para que el frame deseado esté disponible y cambiar a él.
        WebDriverWait(driver, 60).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, Configuracion.cambio_frame)))
        element = None
        xpathselector = Configuracion.columna_combo
        if (not element) and (not xpathselector):
            return
        if xpathselector and (not element):
            element = driver.find_element(By.XPATH, xpathselector)
            driver.execute_script('arguments[0].scrollIntoView()', element)
        time.sleep(1)

        # Regresamos a la ventana principal
        driver.switch_to.default_content()
        Log().info("Se ingresa a la tabla docarti para validar que el articulo sea combo")
        time.sleep(4)

    except Exception as e:  # pragma: no cover
        Log().error(
            f"No se pudo encontrar el campo de combo, validar que la acción anterior haya finalizado,"
            f" que el xpath sea el correcto o que la página no presente lentitud: {e}")
        return False


def validacion_dz_c():
    try:
        cierra_reporte = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrarreporte)))
        cierra_reporte.click()
        Log().info(" Se presiona el boton 'Cerrar', para cerrar reporte")
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo realizar la validacion: {e}")
        raise


def documentos_emitidos_r():
    try:
        refresca = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_refresca)))
        refresca.click()
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"se refresa pantalla documentos {e}")
        time.sleep(2)
        return False

    # Ordena columnas por observaciones
    try:
        ordenarcobservaciones = wait.until(
            EC.presence_of_element_located((By.XPATH, Configuracion.columna_observaciones)))
        ordenarcobservaciones.click()
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se ordeno la columna observaciones, {e}")
        time.sleep(2)
        return False

    try:
        ordenarcobservaciones2 = wait.until(
            EC.presence_of_element_located((By.XPATH, Configuracion.columna_observaciones)))
        ordenarcobservaciones2.click()
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se ordeno la columna observaciones, {e}")
        time.sleep(2)
        return False


# ---------------------------------- Inicio de la automatización DCO05---------------------------------------------


class Test(unittest.TestCase):

    def test_000(self):
        """Ingreso a Chrome"""
        return ingreso_chrome()

    def test_001(self):
        """Ingreso a Power Street"""
        return funciones.ingresologin(self)

    def test_002(self):
        """Ingreso a Reportes DZ"""
        tablas = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_report_dz)))
        tablas.click()
        return funciones.ingresoreportes_dz(self)

    def test_003(self):
        """Ingreso Venta de Contado"""
        return funciones.venta_contado(self)

    def test_004(self):
        """Ingreso de datos en venta de contado"""
        return datos_vco()

    def test_005(self):
        """Validar precios en el articulo"""
        return impuesto_venta(self)

    def test_006(self):
        """Reingreso a reportes DZ"""
        return funciones.reingreso_reporte_dz(self)

    def test_007(self):
        """Se ingresa a documentos emitidos"""
        return funciones.documentos_emitidos(self)

    def test_008(self):
        """Se abre el documento emitido"""
        return documento_emitido()

    def test_009(self):
        """Se ingresa a devolucion de contado"""
        return devolucion_contado()

    def test_010(self):
        """Se valida el impuesto del documento"""
        return impuesto_venta(self)

    def test_011(self):
        """Reingreso a reportes DZ"""
        return documentos_emitidos_r()

    def test_012(self):
        """Reingreso documentos emitidos refrescar"""
        return documento_emitido2()

    def test_013(self):
        """Se abre documento emitido"""
        return funciones.reingreso_reporte_dz2(self)

    def test_014(self):
        """Se ingresa al reporte Docarti"""
        return funciones.tabla_docarti_dco(self)

    def test_015(self):
        """Se ingresa el número de documento"""
        return num_doc()

    def test_020(self):
        """Se vizualiza el campo devolución"""
        return funciones.col_devolucion(self)
