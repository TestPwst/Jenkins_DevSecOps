import unittest

from Pipeline1.FuncionesGral import *
from Pipeline1.VariablesGral import *

doc_emitidos = " Se encontró y abrió el documento emitido "
log_aceptar = " Se presiona el boton 'Aceptar', para ingresar el articulo y la cantidad."


# ----------------------------- Funciones Unicas para DCO01--------------------------------------
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


# ----------------------------- Funciones Unicas para DCO01--------------------------------------
def validar_articulos(self):
    try:
        tablas = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_tablas)))
        tablas.click()
        funciones.ingreso_tabla_articulos(self)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar al menú tablas {e}")
        raise
    try:
        articulo1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_codart)))
        articulo1.send_keys(Configuracion.codigo_art1_vco)
        Log().info(f" Ingresa el codigo del articulo {Configuracion.codigo_art1_vco}")
        time.sleep(1)

        refresca = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_refresca)))
        refresca.click()
        Log().info(" Se presiona el boton 'Refrescar', para mostrar la informacion filtrada")
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
        Log().info(f" Ingresa el codigo del articulo {Configuracion.codigo_art2_vco}")
        time.sleep(1)

        refresca_2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_refresca)))
        refresca_2.click()
        Log().info(" Se presiona el boton 'Refrescar'")
        time.sleep(2)

        art2 = driver.find_element(By.XPATH, Configuracion.articulo2)
        action \
            .double_click(art2) \
            .pause(0) \
            .release()
        action.perform()
        time.sleep(3)

        cerrar_articulo_2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_ventana1)))
        cerrar_articulo_2.click()
        time.sleep(2)

        # ---------------------- Inicia la validación del articulo 3 --------------------------------------
        articulo3 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_codart)))
        articulo3.click()
        articulo3.send_keys(Configuracion.codigo_art3_vco)
        Log().info(f" Ingresa el codigo del articulo {Configuracion.codigo_art3_vco}")
        time.sleep(1)

        refresca_3 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_refresca)))
        refresca_3.click()
        Log().info(" Se presiona el boton 'Refrescar', para mostrar la informacion filtrada.")
        time.sleep(2)

        art3 = driver.find_element(By.XPATH, Configuracion.articulo3)
        action \
            .double_click(art3) \
            .pause(0) \
            .release()
        action.perform()
        time.sleep(3)

        cerrar_articulo_3 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_ventana1)))
        cerrar_articulo_3.click()
        time.sleep(2)

        cierra_ventana = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_ventana)))
        cierra_ventana.click()
        Log().info(" Se presiona el boton 'Cerrar', para cerrar la ventana")

    except Exception as e:  # pragma: no cover
        Log().error(f"No se validaron los articulos. {e}")
        raise


def validacion_dz1(self):
    try:
        funciones.ingresoreportes_dz(self)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar a reportes dz {e}")
        raise
    try:
        # El elemento deseado está dentro de un <iframe> por lo que hay que:
        # Inducir al WebDriverWait para que el frame deseado esté disponible y cambiar a él.

        wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, Configuracion.frame_reporte1)))

        # Obtiene tabla de reporte de stock
        tabla_reporte = driver.find_element(By.XPATH, Configuracion.tabla_reporte1).get_attribute('outerHTML')
        stock_table_df = pd.read_html(StringIO(tabla_reporte))[0]

        # Hace una copia de la tabla, obteniendo solo las columnas de Codigo y Saldo
        df_stock = stock_table_df[['Codigo', 'Saldo']].copy()
        # Limpia la tabla
        df_stock = df_stock.dropna()
        df_stock = df_stock.drop(0)

        # Filtra por codigo de articulo
        stock_inicial = df_stock[(df_stock['Codigo'] == Configuracion.codigo_art1_vco)
                                 | (df_stock['Codigo'] == Configuracion.codigo_art2_vco)
                                 | (df_stock['Codigo'] == Configuracion.codigo_art3_vco)]

        # Resetea los index
        stock_inicial = stock_inicial.reset_index(drop=True)

        # Imprime el stock
        Log().info(f"El stock inicial de los articulos es: {stock_inicial}")
        # print(stockInicial)

        # Regresamos a la ventana principal
        driver.switch_to.default_content()

    except Exception as e:  # pragma: no cover
        Log().error(f"No se obtuvo datos, {e}")
        time.sleep(2)
        return False


def validacion_dz2():
    try:
        refresh_reporte = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_actulizareporte)))
        time.sleep(1)
        refresh_reporte.click()
        time.sleep(5)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo actualizar el reporte DZ2 {e}")
        raise
    try:
        # El elemento deseado está dentro de un <iframe> por lo que hay que:
        # Inducir al WebDriverWait para que el frame deseado esté disponible y cambiar a él.

        wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, Configuracion.frame_reporte1)))

        # Obtiene tabla de reporte de stock
        tablareporte = driver.find_element(By.XPATH, Configuracion.tabla_reporte1).get_attribute('outerHTML')
        stock_ttable_df = pd.read_html(StringIO(tablareporte))[0]

        # Hace una copia de la tabla, obteniendo solo las columnas de Codigo y Saldo
        df_stock = stock_ttable_df[['Codigo', 'Saldo']].copy()
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

    except Exception as e:  # pragma: no cover
        Log().error(f"No se obtuvo datos, validar el error: {e}")
        time.sleep(2)
        return False


def validacion_dz3():
    try:
        refresh_reporte_2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_actulizareporte)))
        time.sleep(1)
        refresh_reporte_2.click()
        time.sleep(5)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo actualizar el reporte DZ3{e}")
        raise
    try:
        # El elemento deseado está dentro de un <iframe> por lo que hay que:
        # Inducir al WebDriverWait para que el frame deseado esté disponible y cambiar a él.

        wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, Configuracion.frame_reporte1)))

        # Obtiene tabla de reporte de stock
        tabla_reporte_1 = driver.find_element(By.XPATH, Configuracion.tabla_reporte1).get_attribute('outerHTML')
        stocktable_df = pd.read_html(StringIO(tabla_reporte_1))[0]

        # Hace una copia de la tabla, obteniendo solo las columnas de Codigo y Saldo
        df_stock = stocktable_df[['Codigo', 'Saldo']].copy()
        # Limpia la tabla
        df_stock = df_stock.dropna()
        df_stock = df_stock.drop(0)

        # Filtra por codigo de articulo
        stock_final = df_stock[(df_stock['Codigo'] == Configuracion.codigo_art1_vco)
                               | (df_stock['Codigo'] == Configuracion.codigo_art2_vco)
                               | (df_stock['Codigo'] == Configuracion.codigo_art3_vco)]

        # Resetea los index
        stock_final = stock_final.reset_index(drop=True)

        # Imprime el stock
        Log().info(f"El stock final de los articulos es: {stock_final}")
        # print(stockInicial)

        # Regresamos a la ventana principal
        driver.switch_to.default_content()
        time.sleep(1)

        cierra_todo = wait.until(EC.presence_of_element_located
                                 ((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[1]")))
        cierra_todo.click()
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
        Log().error(f"No se pudo acceder al documento venta de contado {e}")
        raise
    try:
        cliente = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cliente)))
        cliente.send_keys(Configuracion.cuenta)
        time.sleep(1)
        Log().info("Se agregar al cliente 0010051428 para realizar la venta de contado por packing")

        observaciones1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_obs1)))
        observaciones1.send_keys(Configuracion.i_observaciones1)
        time.sleep(1)
        # Log().info("Se ingresa la observación al documento")

        observaciones2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_obs2)))
        observaciones2.send_keys(Configuracion.i_observaciones_vco1)
        time.sleep(1)
        # Log().info("Se ingresa la observación al documento")

        agrega_item = wait.until(EC.element_to_be_clickable((By.XPATH, Configuracion.btn_agrega_item)))
        agrega_item.click()
        agrega_item.click()

        articulo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        articulo.send_keys(Configuracion.codigo_art1_vco)
        Log().info(" Ingresa articulo 1")
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar los datos al documento Venta de contado, {e}")
        raise

    try:
        try:
            atributo_precio = WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.XPATH, Configuracion.precio_venta)))

            if atributo_precio.is_displayed():
                Log().info("El precio unitario está en pantalla")

        except Exception as e:  # pragma: no cover
            Log().error(f"No se pudo acceder a atributo precio {e}")
            # Configura el atributo
            try:
                agrega_atributo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_atributos)))
                time.sleep(1)
                agrega_atributo.click()
                time.sleep(1)

                atributo_preciounitario = wait.until(
                    EC.presence_of_element_located((By.XPATH, Configuracion.atributo_precio)))
                time.sleep(1)
                atributo_preciounitario.click()
                time.sleep(1)

                cerrar_atributo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar2)))
                time.sleep(1)
                cerrar_atributo.click()
                time.sleep(1)
                Log().info("Se agrega el atributo precio unitario")

            except Exception as e:  # pragma: no cover
                Log().error(f"No se logro agregar el atributo precio unitario, error {e}")

    except Exception as e:  # pragma: no cover
        Log().error(f"No se encontró el atributo precio unitario, verificar error {e}")
        time.sleep(2)
        driver.quit()
        return False

    try:
        ccantidad = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        time.sleep(1)
        ccantidad.click()
        time.sleep(1)
        ccantidad.send_keys(Configuracion.cantidad_art1)
        Log().info(f" Ingresa la cantidad del articulo {Configuracion.cantidad_art1}")

        aceptar = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        time.sleep(1)
        aceptar.click()
        Log().info(log_aceptar)
        time.sleep(2)

        # ----------------------------------- Ingreso articulo 2 -------------------------------------------
        articulo_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        time.sleep(1)
        articulo_1.send_keys(Configuracion.codigo_art2_vco)
        Log().info(" Ingresa articulo 2")
        time.sleep(1)

        ccantidad_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        time.sleep(1)
        ccantidad_1.click()
        time.sleep(1)
        ccantidad_1.send_keys(Configuracion.cantidad_art1)
        Log().info(f" Ingresa la cantidad del articulo {Configuracion.cantidad_art1}")

        aceptar_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        time.sleep(1)
        aceptar_1.click()
        Log().info(log_aceptar)
        time.sleep(2)

        # ------------------------------------- Ingreso articulo 3 -----------------------------------------
        articulo_2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        time.sleep(1)
        articulo_2.send_keys(Configuracion.codigo_art3_vco)
        Log().info(" Ingresa articulo 3")
        time.sleep(1)

        ccantidad_2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        ccantidad_2.click()
        time.sleep(1)
        ccantidad_2.send_keys(Configuracion.cantidad_art1)
        Log().info(f" Ingresa la cantidad del articulo {Configuracion.cantidad_art1}")

        aceptar_2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        time.sleep(1)
        aceptar_2.click()
        Log().info(log_aceptar)
        time.sleep(2)

        cancelar = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cancelar)))
        time.sleep(1)
        cancelar.click()
        Log().info(" Se presiona el boton 'Cancelar', para mostrar la informacion del reporte.")
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudieron agregar los artículos, error {e}")
        raise


def datos_dco(self):
    try:
        funciones.devolucion_contado(self)
    except Exception as e:  # pragma: no cover
        Log().error(f"Mo se pudo acceder a documento devolucion de contado {e}")
        raise
    try:
        cliente = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cliente)))
        cliente.send_keys(Configuracion.cuenta)
        time.sleep(1)
        Log().info("Se agregar al cliente 0010051428 para realizar la venta de contado por packing")

        observaciones1_dco1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_obs1)))
        observaciones1_dco1.send_keys(Configuracion.i_observaciones2)
        time.sleep(1)

        observaciones2_dco1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_obs2)))
        observaciones2_dco1.send_keys(Configuracion.i_observaciones_dco1)
        time.sleep(1)

        agregaitem = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_agrega_item)))
        agregaitem.click()
        agregaitem.click()
        time.sleep(0)

        # ingreso del primer articulo
        articulo_1_dco1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        articulo_1_dco1.send_keys(Configuracion.codigo_art1_vco)
        Log().info(" Ingresa articulo 1")
        time.sleep(1)

        ccantidad_1_dco1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        ccantidad_1_dco1.click()
        time.sleep(1)
        ccantidad_1_dco1.send_keys(Configuracion.cantidad_art1)
        Log().info(f" Ingresa la cantidad del articulo {Configuracion.cantidad_art1}")

        aceptar_1_dco1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        aceptar_1_dco1.click()
        time.sleep(2)
        Log().info(log_aceptar)

    except Exception as e:  # pragma: no cover
        Log().error(f" No se pudieron agregar los articulos al documento, {e}")
        raise

    try:
        # ----------------------------------- Ingreso articulo 2 -------------------------------------------
        articulo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        time.sleep(1)
        articulo.send_keys(Configuracion.codigo_art2_vco)
        Log().info(" Ingresa articulo 2")
        time.sleep(1)

        ccantidad_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        time.sleep(1)
        ccantidad_1.click()
        time.sleep(1)
        ccantidad_1.send_keys(Configuracion.cantidad_art1)
        Log().info(f" Ingresa la cantidad del articulo {Configuracion.cantidad_art1}")

        aceptar_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        time.sleep(1)
        aceptar_1.click()
        Log().info(log_aceptar)
        time.sleep(2)

        # ------------------------------------- Ingreso articulo 3 -----------------------------------------
        articulo_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        time.sleep(1)
        articulo_1.send_keys(Configuracion.codigo_art3_vco)
        Log().info(" Ingresa articulo 3")
        time.sleep(1)

        ccantidad_2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        ccantidad_2.click()
        time.sleep(1)
        ccantidad_2.send_keys(Configuracion.cantidad_art1)
        Log().info(f" Ingresa la cantidad del articulo {Configuracion.cantidad_art1}")

        aceptar_2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        time.sleep(1)
        aceptar_2.click()
        Log().info(log_aceptar)
        time.sleep(2)

        cancelar_2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cancelar)))
        time.sleep(1)
        cancelar_2.click()
        Log().info(" Se presiona el boton 'Cancelar', para mostrar la informacion del reporte.")
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f" No se pudieron agregar los articulos al documento, error {e}")
        raise


def impuesto_venta(self):
    try:
        infoventa = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_info_art)))
        infoventa.click()
        Log().info("Se da click a la información a detalle de la venta de contado")
        time.sleep(2)

        validaiva = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.iva_venta_contado1))).text
        self.assertEqual("252.14", validaiva, "El IVA es correcto")
        # Log().info("El IVA de la venta es correcto")
        time.sleep(1)

        validatotal = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.total_venta_contado1))).text
        self.assertEqual("1,828.04", validatotal, "El total es correcto")
        # Log().info("El total de la venta es correcto")
        time.sleep(1)

        cerrarinfo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar)))
        cerrarinfo.click()
        Log().info("Se cierra información a detalle de la venta de contado")

        # Guarda el documento venta de contado
        guarda = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_guarda)))
        time.sleep(1)
        guarda.click()
        Log().info(" Se da clic en el boton Guardar; se emite el documento.")

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo validar el cálculo del documento {e}")
        raise


def documento_emitido(self):
    try:
        funciones.documentos_emitidos(self)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar a documentos emitidos {e}")
        raise
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
        Log().info(doc_emitidos)
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo abrir el documento emitido, revisar error {e}")
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
        Log().info(doc_emitidos)
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo abrir el documento emitido {e}")
        raise

    try:
        cierra_todo1 = wait.until(EC.presence_of_element_located
                                  ((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[3]")))
        cierra_todo1.click()
        Log().info(" Se presiona el boton 'Cerrar', para cerrar el documento de venta.")
        time.sleep(2)

        cierra_todo = wait.until(EC.presence_of_element_located
                                 ((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[2]")))
        cierra_todo.click()
        Log().info(" Se presiona el boton 'Cerrar', para cerrar pantalla de documentos emitidos.")
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo cerrar el documento emitido {e}")
        raise


def documento_emitido2(self):
    try:
        funciones.documentos_emitidos(self)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar a los documentos emitidos {e}")
        raise
    try:
        busqueda_docemitido = wait.until(
            EC.presence_of_element_located((By.XPATH, Configuracion.busqueda_odocemitido2)))
        action \
            .click(busqueda_docemitido) \
            .pause(0) \
            .double_click(busqueda_docemitido) \
            .pause(1) \
            .double_click(busqueda_docemitido) \
            .release()
        action.perform()
        Log().info(doc_emitidos)
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No permite abrir el documento emitido nuevamente {e}")
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
        Log().error(f"No se pudo extraer el numero de documento y la serie {e}")
        raise

    try:
        doc_emitido_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.info_doc)))
        action \
            .click(doc_emitido_1) \
            .pause(0) \
            .send_keys(Keys.ARROW_DOWN) \
            .pause(0) \
            .send_keys(Keys.ARROW_DOWN) \
            .pause(0) \
            .release()
        action.perform()
        Log().info(doc_emitidos)
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo abrir y revisar el documento emitido {e}")
        raise

    try:
        cierra_todo1_1 = wait.until(EC.presence_of_element_located
                                    ((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[2]")))
        cierra_todo1_1.click()
        Log().info(" Se presiona el boton 'Cerrar', para cerrar el documento de venta.")
        time.sleep(2)

        cierra_todo_1 = wait.until(EC.presence_of_element_located
                                   ((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[1]")))
        cierra_todo_1.click()
        Log().info(" Se presiona el boton 'Cerrar', para cerrar pantalla de documentos emitidos.")
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No cerró correctamente todas las ventanas {e}")
        raise


def num_doc(self):
    try:
        funciones.tabla_docarti_dco(self)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar a tabla docarti {e}")
        raise
    try:
        cnumerodoc = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_numero_doc)))
        cnumerodoc.send_keys(numero_documento)
        Log().info(" Ingresa el numero de documento ")
        time.sleep(1)

        ver = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_ver1)))
        ver.click()
        Log().info(" Se presiona el boton 'Ver', para mostrar la informacion del reporte.")
        time.sleep(4)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar el numero del documento, {e}")
        raise


# ---------------------------------- Inicio de la automatización DCO01---------------------------------------------
class Test(unittest.TestCase):

    def test_000(self):
        """Ingreso a Powet Street"""
        ingreso(self)

    def test_001(self):
        """Validación de articulos"""
        return validar_articulos(self)

    def test_002(self):
        """Validación del reporte DZ"""
        return validacion_dz1(self)

    def test_003(self):
        """Ingreso de datos en venta de contado"""
        return datos_vco(self)

    def test_004(self):
        """Validar precios en el articulo"""
        return impuesto_venta(self)

    def test_005(self):
        """Validación de reporte DZ"""
        return validacion_dz2()

    def test_006(self):
        """Se abre el documento emitido"""
        return documento_emitido(self)

    def test_007(self):
        """Se ingresan los datos al documento"""
        return datos_dco(self)

    def test_008(self):
        """Se valida el impuesto del documento"""
        return impuesto_venta(self)

    def test_009(self):
        """Validación de reporte DZ"""
        return validacion_dz3()

    def test_010(self):
        """Se abre documento emitido"""
        return documento_emitido2(self)

    def test_011(self):
        """Se ingresa el número de documento"""
        return num_doc(self)
