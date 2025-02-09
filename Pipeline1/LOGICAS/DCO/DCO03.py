import unittest

from Pipeline1.FuncionesGral import *
from Pipeline1.VariablesGral import *


# ----------------------------- Funciones Unicas para DCO03--------------------------------------
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
        funciones.ingreso_tabla_articulos(self)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo acceder a menú tablas {e}")
        raise
    try:
        ccodigo_articulo1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_codart)))
        ccodigo_articulo1.send_keys(Configuracion.codigo_art_compo)
        # Log().info(" Ingresa el codigo del articulo ")
        time.sleep(1)

        refresca = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_refresca)))
        refresca.click()
        # Log().info(" Se presiona el boton 'Refrescar', para mostrar la informacion filtrada.")
        time.sleep(2)

        artcomp = driver.find_element(By.XPATH, Configuracion.articulo_comp)
        action \
            .double_click(artcomp) \
            .pause(0) \
            .release()
        action.perform()
        time.sleep(1)

        # se cambia a la pestaña combo
        combo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.art_combo)))
        action \
            .click(combo) \
            .pause(0) \
            .release()
        action.perform()
        Log().info("Se valida que el articulo este configurado como Factura Componente")
        time.sleep(1)

        cerrararticulo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_ventana1)))
        cerrararticulo.click()
        time.sleep(2)

        cierra_ventana = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_ventana)))
        cierra_ventana.click()
        # Log().info(" Se presiona el boton 'Cerrar', para cerrar la ventana")

    except Exception as e:  # pragma: no cover
        Log().error(f"La validación de la configuración del articulo FAP02629 no es correcta {e}")
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
        tablareporte = driver.find_element(By.XPATH, Configuracion.tabla_reporte1).get_attribute('outerHTML')
        stocktable_df = pd.read_html(StringIO(tablareporte))[0]

        # Hace una copia de la tabla, obteniendo solo las columnas de Codigo y Saldo
        df_stock = stocktable_df[['Codigo', 'Saldo']].copy()
        # Limpia la tabla
        df_stock = df_stock.dropna()
        df_stock = df_stock.drop(0)

        # Filtra por codigo de articulo
        stock_inicial = df_stock[(df_stock['Codigo'] == Configuracion.codigo_art1_vco)
                                 | (df_stock['Codigo'] == Configuracion.codigo_art23_vco)]

        # Resetea los index
        stock_inicial = stock_inicial.reset_index(drop=True)

        # Imprime el stock
        Log().info(f"El stock inicial de los articulos es: {stock_inicial}")
        time.sleep(1)
        # print(stockInicial)

        # Regresamos a la ventana principal
        driver.switch_to.default_content()

    except Exception as e:  # pragma: no cover
        Log().error(f"No se obtuvo datos, validar el error: {e}")
        time.sleep(2)
        return False


def validacion_dz2():
    try:
        refresh_reporte = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_actulizareporte)))
        time.sleep(1)
        refresh_reporte.click()
        time.sleep(5)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo actualizar el reporte DZ {e}")
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
        stock = df_stock[(df_stock['Codigo'] == Configuracion.codigo_art1_vco)
                         | (df_stock['Codigo'] == Configuracion.codigo_art23_vco)]

        # Resetea los index
        stock = stock.reset_index(drop=True)

        # Imprime el stock
        Log().info(f"El stock de los articulos despues de la venta es: {stock}")
        time.sleep(1)
        # print(stockInicial)

        # Regresamos a la ventana principal
        driver.switch_to.default_content()

    except Exception as e:  # pragma: no cover
        Log().error(f"No se obtuvo datos, validar el error: {e}")
        time.sleep(2)
        return False


def validacion_dz3():
    try:
        refresh_reporte = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_actulizareporte)))
        time.sleep(1)
        refresh_reporte.click()
        time.sleep(5)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo actualizar el reporte DZ {e}")
        raise
    try:
        # El elemento deseado está dentro de un <iframe> por lo que hay que:
        # Inducir al WebDriverWait para que el frame deseado esté disponible y cambiar a él.

        wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, Configuracion.frame_reporte1)))

        # Obtiene tabla de reporte de stock
        tabla_reporte_1 = driver.find_element(By.XPATH, Configuracion.tabla_reporte1).get_attribute('outerHTML')
        stock_table_df_1 = pd.read_html(StringIO(tabla_reporte_1))[0]

        # Hace una copia de la tabla, obteniendo solo las columnas de Codigo y Saldo
        df_stock = stock_table_df_1[['Codigo', 'Saldo']].copy()
        # Limpia la tabla
        df_stock = df_stock.dropna()
        df_stock = df_stock.drop(0)

        # Filtra por codigo de articulo
        stock_final = df_stock[(df_stock['Codigo'] == Configuracion.codigo_art1_vco)
                               | (df_stock['Codigo'] == Configuracion.codigo_art23_vco)]

        # Resetea los index
        stock_final = stock_final.reset_index(drop=True)

        # Imprime el stock
        Log().info(f"El stock final de los articulos es: {stock_final}")
        time.sleep(1)
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
        Log().error(f"No se pudo acceder a menú venta de contado {e}")
        raise
    # Ingreso de informacion a la venta
    # Ingreso cliente
    try:
        ccliente_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cliente)))
        ccliente_1.send_keys(Configuracion.cuenta)
        time.sleep(2)
        Log().info(
            f"Se agregar al cliente: {Configuracion.cuenta} para realizar la venta de contado por combo componente")

        observaciones1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_obs1)))
        observaciones1.send_keys(Configuracion.i_observaciones1)
        time.sleep(1)
        # Log().info("Se ingresa la observación al documento")

        observaciones2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_obs2)))
        observaciones2.send_keys(Configuracion.i_observaciones_vc3)
        time.sleep(1)
        # Log().info("Se ingresa la observación al documento")

        # Da clic en agregar

        agregaitem = wait.until(EC.element_to_be_clickable((By.XPATH, Configuracion.btn_agrega_item)))
        agregaitem.click()
        agregaitem.click()

        articulo = wait.until(EC.visibility_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        wait.until(EC.visibility_of(articulo))
        articulo.click()
        time.sleep(1)
        articulo.send_keys(Configuracion.codigo_art_compo)

    except Exception as e:  # pragma: no cover
        Log().error(
            f"No se pudo ingresar el articulo, validar {e}")
        raise

    try:
        try:
            atributoprecio = WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.XPATH, Configuracion.precio_venta)))

            if atributoprecio.is_displayed():
                Log().info("El precio unitario está en pantalla")

        except Exception as e:  # pragma: no cover
            Log().error(f"No se pudo abrir el atributo precio {e}")
            # Configura el atributo
            try:
                agregaatributo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_atributos)))
                agregaatributo.click()
                time.sleep(1)

                atributopreciounitario = wait.until(
                    EC.presence_of_element_located((By.XPATH, Configuracion.atributo_precio)))
                atributopreciounitario.click()
                time.sleep(1)

                cerraratributo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar2)))
                cerraratributo.click()
                time.sleep(1)
                # Log().info("Se agrega el atributo precio unitario")

            except Exception as e:  # pragma: no cover
                Log().info(f"No se logro agregar el atributo precio unitario, error {e}")
    except Exception as e:
        Log().info(f"No se encontró el atributo precio unitario {e}")
        raise

    # Ingreso de cantidad del articulo
    try:
        ccantidad = wait.until(EC.visibility_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        wait.until(EC.element_to_be_clickable(ccantidad))
        ccantidad.click()
        time.sleep(1)
        ccantidad.send_keys(Configuracion.cantidad_art1)
        Log().info(
            f" Ingresa la cantidad de: {Configuracion.cantidad_art1} del articulo: {Configuracion.codigo_art_compo}")
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(
            f"No se pudo ingresar la cantidad del articulo, validar {e}")
        raise

    # Da clic en aceptar
    try:
        aceptar = wait.until(EC.visibility_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        wait.until(EC.visibility_of(aceptar))
        time.sleep(1)
        aceptar.click()
        Log().info(" Se presiona el boton 'aceptar', para ingresar el articulo y la cantidad.")
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se dio click al botón Aceptar, validar {e}")
        raise

    # Da clic en cancelar para cerrar el ingreso de articulos
    try:
        cancelar = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cancelar)))
        wait.until(EC.visibility_of(cancelar))
        cancelar.click()
        Log().info(" Se presiona el boton 'Cancelar', para mostrar la informacion del reporte.")
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se dio click al botón Cancelar, validar que {e}")
        raise


def datos_dco(self):
    try:
        funciones.devolucion_contado(self)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo acceder a devolución de contado {e}")
        raise
    # Ingreso de informacion a la venta
    # Ingreso cliente
    try:
        ccliente_2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cliente)))
        ccliente_2.send_keys(Configuracion.cuenta)
        time.sleep(2)
        Log().info(
            f"Se agregar al cliente: {Configuracion.cuenta} para realizar la venta de contado por combo componente")

        observaciones1_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_obs1)))
        observaciones1_1.send_keys(Configuracion.i_observaciones2)
        time.sleep(1)
        # Log().info("Se ingresa la observación al documento")

        observaciones2_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_obs2)))
        observaciones2_1.send_keys(Configuracion.i_observaciones_dco3)
        time.sleep(1)
        # Log().info("Se ingresa la observación al documento")

        # Da clic en agregar

        agregaitem_1 = wait.until(EC.element_to_be_clickable((By.XPATH, Configuracion.btn_agrega_item)))
        agregaitem_1.click()
        agregaitem_1.click()

        articulo_1 = wait.until(EC.visibility_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        wait.until(EC.visibility_of(articulo_1))
        articulo_1.click()
        time.sleep(1)
        articulo_1.send_keys(Configuracion.codigo_art_compo)
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar el articulo, validar error {e}")
        raise

    # Ingreso de cantidad del articulo
    try:
        ccantidad_1 = wait.until(EC.visibility_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        wait.until(EC.element_to_be_clickable(ccantidad_1))
        ccantidad_1.click()
        time.sleep(1)
        ccantidad_1.send_keys(Configuracion.cantidad_art1)
        Log().info(
            f" Ingresa la cantidad de: {Configuracion.cantidad_art1} del articulo: {Configuracion.codigo_art_compo}")
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar la cantidad del articulo, validar error {e}")
        raise

    # Da clic en aceptar
    try:
        aceptar_1 = wait.until(EC.visibility_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        wait.until(EC.visibility_of(aceptar_1))
        time.sleep(1)
        aceptar_1.click()
        Log().info(" Se presiona el boton 'Aceptar', para ingresar el articulo y la cantidad.")
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se dio click al botón Aceptar, validar error {e}")
        raise

    # Da clic en cancelar para cerrar el ingreso de articulos
    try:
        cancelar_1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cancelar)))
        wait.until(EC.visibility_of(cancelar_1))
        time.sleep(1)
        cancelar_1.click()
        Log().info(" Se presiona el boton 'Cancelar', para mostrar la informacion del reporte.")
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se dio click al botón Cancelar, validar {e}")
        raise


def impuesto_venta(self):
    # Se abre el detalle del calculo del documento
    try:
        infoventa = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_info_art)))
        infoventa.click()
        Log().info("Se da click a la información a detalle de la venta de contado")
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().info(f"No se logró dar click a la información a detalle de la venta de contado. {e}")
        raise

    try:
        validaiva = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.iva_devolucion_contado3))).text
        self.assertEqual("186.11", validaiva, "El IVA es correcto")
        Log().info("El IVA de la venta es correcto")
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().info(f"El IVA de la venta no son correctos. {e}")
        raise

    try:
        validatotal = wait.until(EC.presence_of_element_located((
            By.XPATH, Configuracion.total_devolucion_contado3))).text
        self.assertEqual("1,349.31", validatotal, "El total es correcto")
        Log().info("El total de la venta es correcto")
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().info(f"El total de la venta no son correctos. {e}")
        raise

    # Se cierra la ventana de detalle de calculo de informacion
    try:
        cerrarinfo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar)))
        cerrarinfo.click()
        Log().info("Se cierra información a detalle de la venta de contado")

    except Exception as e:  # pragma: no cover
        Log().info(f"No se logró cerrar la informacion de detalle de la venta de contado. {e}")
        raise

    # Guarda el documento de venta contado
    try:
        guarda = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_guarda)))
        time.sleep(1)
        guarda.click()
        Log().info(" Se da clic en el boton Guardar; se emite el documento.")

    except Exception as e:  # pragma: no cover
        Log().error(f"No se dio click al botón Guardar, validar {e}")
        raise


def documento_emitido(self):
    try:
        funciones.documentos_emitidos(self)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo acceder a documentos emitidos, verificar error {e}")
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
        Log().info(" Se encontro y abrio el documento emitido ")
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo buscar el documento emitido, verificar error {e}")
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
        # Log().info(" Se encontro y abrio el documento emitido ")
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo abrir el documento emitido, verificar error {e}")
        raise

    try:
        cierra_todo1 = wait.until(EC.presence_of_element_located
                                  ((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[3]")))
        cierra_todo1.click()
        Log().info(" Se presiona el boton 'Cerrar', para cerrar el documento de venta.")
        time.sleep(2)

        cierra_todo1 = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                  f"({Configuracion.btn_cerrar_pantalla})[2]")))
        cierra_todo1.click()
        Log().info(" Se presiona el boton 'Cerrar', para cerrar pantalla de documentos emitidos.")
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se encontraron ventanas a cerrar {e}")
        raise


def documento_emitido2(self):
    try:
        funciones.documentos_emitidos(self)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se ingresó a documentos emitidos {e}")
        raise
    try:
        busqueda_docemitido_1 = wait.until(
            EC.presence_of_element_located((By.XPATH, Configuracion.busqueda_odocemitido2)))
        action \
            .click(busqueda_docemitido_1) \
            .pause(0) \
            .double_click(busqueda_docemitido_1) \
            .pause(1) \
            .double_click(busqueda_docemitido_1) \
            .release()
        action.perform()
        Log().info(" Se encontro y abrio el documento emitido ")
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo abrir documentos emitidos {e}")
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
        Log().error(f"No se pudo extrae el # de serie ni el # de documento del documento emitido {e}")
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
        # Log().info(" Se encontro y abrio el documento emitido ")
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se abrió el documento emitido ni se pudo acceder a él {e}")
        raise

    try:
        cierra_todo1_1 = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                    f"({Configuracion.btn_cerrar_pantalla})[2]")))
        cierra_todo1_1.click()
        Log().info(" Se presiona el boton 'Cerrar', para cerrar el documento de venta.")
        time.sleep(2)

        cierra_todo1_1 = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                    f"({Configuracion.btn_cerrar_pantalla})[1]")))
        cierra_todo1_1.click()
        Log().info(" Se presiona el boton 'Cerrar', para cerrar pantalla de documentos emitidos.")
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo cerrar completamente {e}")
        raise


def num_doc(self):
    try:
        funciones.tabla_docarti_dco(self)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo acceder a tabla docarti {e}")
        raise
    try:
        cnumerodoc = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_numero_doc)))
        cnumerodoc.send_keys(numero_documento)
        Log().info(" Ingresa el numero de documento ")
        time.sleep(1)

        ver = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_ver1)))
        ver.click()
        Log().info(" Se presiona el boton 'Ver', para mostrar la informacion del reporte.")
        time.sleep(5)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se colocaron datos en reporte / click en ver {e}")
        raise
    try:
        funciones.col_combo(self)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo acceder a col_combo {e}")
        raise

# ---------------------------------- Inicio de la automatización DCO03---------------------------------------------


class Test(unittest.TestCase):

    def test_000(self):
        """Ingreso a Chrome"""
        return ingreso(self)

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
        """Validación de reporte DZ cerrar"""
        return validacion_dz3()

    def test_010(self):
        """Se abre documento emitido"""
        return documento_emitido2(self)

    def test_011(self):
        """Se ingresa el número de documento"""
        return num_doc(self)
