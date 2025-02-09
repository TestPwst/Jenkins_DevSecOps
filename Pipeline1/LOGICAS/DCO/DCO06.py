import unittest

from Pipeline1.FuncionesGral import *
from Pipeline1.VariablesGral import *


# ----------------------------- Funciones Unicas para DCO01--------------------------------------
def validar_articulos():
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

        cerrar_articulo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_ventana1)))
        cerrar_articulo.click()
        time.sleep(2)
        # ---------------------- Inicia la validación del articulo 2 --------------------------------------
        articulo2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_codart)))
        articulo2.click()
        articulo2.send_keys(Configuracion.codigo_art2_vco)
        # Log().info(" Ingresa el codigo del articulo ")
        time.sleep(1)

        refresca2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_refresca)))
        refresca2.click()
        # Log().info(" Se presiona el boton 'Refrescar', para mostrar la informacion filtrada.")
        time.sleep(2)

        art2 = driver.find_element(By.XPATH, Configuracion.articulo2)
        action \
            .double_click(art2) \
            .pause(0) \
            .release()
        action.perform()
        time.sleep(3)

        cerrar_articulo2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_ventana1)))
        cerrar_articulo2.click()
        time.sleep(2)

        # ---------------------- Inicia la validación del articulo 3 --------------------------------------
        articulo3 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_codart)))
        articulo3.click()
        articulo3.send_keys(Configuracion.codigo_art22_vco)
        # Log().info(" Ingresa el codigo del articulo ")
        time.sleep(1)

        refresca3 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_refresca)))
        refresca3.click()
        # Log().info(" Se presiona el boton 'Refrescar', para mostrar la informacion filtrada.")
        time.sleep(2)

        art3 = driver.find_element(By.XPATH, Configuracion.articulo22)
        action \
            .double_click(art3) \
            .pause(0) \
            .release()
        action.perform()
        time.sleep(3)

        cerrar_articulo3 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_ventana1)))
        cerrar_articulo3.click()
        time.sleep(2)

        # ---------------------- Inicia la validación del articulo 4 --------------------------------------
        articulo4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_codart)))
        articulo4.click()
        articulo4.send_keys(Configuracion.codigo_art4_vco)
        # Log().info(" Ingresa el codigo del articulo ")
        time.sleep(1)

        refresca4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_refresca)))
        refresca4.click()
        # Log().info(" Se presiona el boton 'Refrescar', para mostrar la informacion filtrada.")
        time.sleep(2)

        art4 = driver.find_element(By.XPATH, Configuracion.articulo4)
        action \
            .double_click(art4) \
            .pause(0) \
            .release()
        action.perform()
        time.sleep(3)

        cerrar_articulo4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_ventana1)))
        cerrar_articulo4.click()
        time.sleep(2)

        cierra_ventana = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_ventana)))
        cierra_ventana.click()
        # Log().info(" Se presiona el boton 'Cerrar', para cerrar la ventana")

    except Exception as e:  # pragma: no cover
        Log().error(f"No se validaron los artículos: {e}")
        raise


def validacion_dz():
    try:
        # El elemento deseado está dentro de un <iframe> por lo que hay que:
        # Inducir al WebDriverWait para que el frame deseado esté disponible y cambiar a él.

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Configuracion.frame_reporte1)))

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
                                 | (df_stock['Codigo'] == Configuracion.codigo_art22_vco)
                                 | (df_stock['Codigo'] == Configuracion.codigo_art4_vco)]

        # Resetea los index
        stock_inicial = stock_inicial.reset_index(drop=True)

        # Imprime el stock
        Log().info("El stock de los articulos es:")
        print(stock_inicial)

        # Regresamos a la ventana principal
        driver.switch_to.default_content()

    except Exception as e:  # pragma: no cover
        Log().error(f"No se obtuvo datos: {e}")
        time.sleep(2)
        return False


def datos_vco():
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
        observaciones2.send_keys(Configuracion.i_observaciones_vc6)
        time.sleep(1)
        # Log().info("Se ingresa la observación al documento")

        agrega_item = wait.until(EC.element_to_be_clickable((By.XPATH, Configuracion.btn_agrega_item)))
        agrega_item.click()
        agrega_item.click()

        articulo_vco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        articulo_vco.send_keys(Configuracion.codigo_art1_vco)
        Log().info(" Ingresa articulo 1")
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar los datos al documento Venta de contado: {e}")
        raise

    try:
        try:
            # atributo_precio = self.driver.find_elements(By.XPATH, Configuracion.precio_venta).is_displayed()
            atributo_precio = WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.XPATH, Configuracion.precio_venta)))

            if atributo_precio.is_displayed():
                Log().info("El precio unitario está en pantalla")

        except Exception as e:  # pragma: no cover
            Log().error(f"No se pudo validar atributo precio: {e}")
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
                # Log().info("Se agrega el atributo precio unitario")

            except Exception as e:  # pragma: no cover
                Log().error(f"No se logro agregar el atributo precio unitario, error: {e}")
                pass

    except Exception as e:  # pragma: no cover
        Log().error(f"No se encontró el atributo precio unitario: {e}")
        time.sleep(2)
        driver.quit()
        return False

    try:
        ccantidad1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        time.sleep(1)
        ccantidad1.click()
        time.sleep(1)
        ccantidad1.send_keys(Configuracion.cantidad_art1)
        Log().info(" Ingresa la cantidad del articulo ")

        aceptar1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        time.sleep(1)
        aceptar1.click()
        Log().info(" Se presiona el boton 'aceptar', para ingresar el articulo y la cantidad.")
        time.sleep(2)

        # ----------------------------------- Ingreso articulo 2 -------------------------------------------
        articulo2_vco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        time.sleep(1)
        articulo2_vco.send_keys(Configuracion.codigo_art2_vco)
        Log().info(" Ingresa articulo 2")
        time.sleep(1)

        ccantidad2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        time.sleep(1)
        ccantidad2.click()
        time.sleep(1)
        ccantidad2.send_keys(Configuracion.cantidad_art1)
        Log().info(" Ingresa la cantidad del articulo ")

        aceptar2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        time.sleep(1)
        aceptar2.click()
        Log().info(" Se presiona el boton 'aceptar', para ingresar el articulo y la cantidad.")
        time.sleep(2)

        # ------------------------------------- Ingreso articulo 3 -----------------------------------------
        articulo3_vco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        time.sleep(1)
        articulo3_vco.send_keys(Configuracion.codigo_art22_vco)
        Log().info(" Ingresa articulo 3")
        time.sleep(1)

        ccantidad3 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        ccantidad3.click()
        time.sleep(1)
        ccantidad3.send_keys(Configuracion.cantidad_art1)
        Log().info(" Ingresa la cantidad del articulo ")

        aceptar3 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        time.sleep(1)
        aceptar3.click()
        Log().info(" Se presiona el boton 'aceptar', para ingresar el articulo y la cantidad.")
        time.sleep(2)

        # ------------------------------------- Ingreso articulo 4 -----------------------------------------
        articulo4_vco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        time.sleep(1)
        articulo4_vco.send_keys(Configuracion.codigo_art4_vco)
        Log().info(" Ingresa articulo 4")
        time.sleep(1)

        ccantidad4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        ccantidad4.click()
        time.sleep(1)
        ccantidad4.send_keys(Configuracion.cantidad_art1)
        Log().info(" Ingresa la cantidad del articulo ")

        aceptar4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        time.sleep(1)
        aceptar4.click()
        Log().info(" Se presiona el boton 'aceptar', para ingresar el articulo y la cantidad.")
        time.sleep(2)

        cancelar4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cancelar)))
        time.sleep(1)
        cancelar4.click()
        Log().info(" Se presiona el boton 'cancelar', para mostrar la informacion del reporte.")
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudieron agregar los articulos al documento: {e}")
        raise


def datos_dco():
    try:
        cliente_dco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cliente)))
        cliente_dco.send_keys(Configuracion.cuenta)
        time.sleep(1)
        Log().info("Se agregar al cliente 0010051428 para realizar la venta de contado por packing")

        observaciones1_dco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_obs1)))
        observaciones1_dco.send_keys(Configuracion.i_observaciones2)
        time.sleep(1)

        observaciones2_dco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_obs2)))
        observaciones2_dco.send_keys(Configuracion.i_observaciones_dco6)
        time.sleep(1)

        agrega_item_dco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_agrega_item)))
        agrega_item_dco.click()
        agrega_item_dco.click()
        time.sleep(0)

        # ingreso del primer articulo
        articulo1_dco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        articulo1_dco.send_keys(Configuracion.codigo_art1_vco)
        Log().info(" Ingresa articulo 1")
        time.sleep(1)

        ccantidad_dco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        ccantidad_dco.click()
        time.sleep(1)
        ccantidad_dco.send_keys(Configuracion.cantidad_art1)
        Log().info(" Ingresa la cantidad del articulo ")

        aceptar_dco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        aceptar_dco.click()
        time.sleep(2)
        Log().info(" Se presiona el boton 'aceptar', para ingresar el articulo y la cantidad.")

    except Exception as e:  # pragma: no cover
        Log().error(f"Error al agregar los articulos al documento: {e}")
        raise

    try:
        # ----------------------------------- Ingreso articulo 2 -------------------------------------------
        articulo2_dco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        time.sleep(1)
        articulo2_dco.send_keys(Configuracion.codigo_art2_vco)
        Log().info(" Ingresa articulo 2")
        time.sleep(1)

        ccantidad2_dco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        time.sleep(1)
        ccantidad2_dco.click()
        time.sleep(1)
        ccantidad2_dco.send_keys(Configuracion.cantidad_art1)
        Log().info(" Ingresa la cantidad del articulo ")

        aceptar2_dco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        time.sleep(1)
        aceptar2_dco.click()
        Log().info(" Se presiona el boton 'aceptar', para ingresar el articulo y la cantidad.")
        time.sleep(2)

        # ------------------------------------- Ingreso articulo 3 -----------------------------------------
        articulo3_dco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        time.sleep(1)
        articulo3_dco.send_keys(Configuracion.codigo_art22_vco)
        Log().info(" Ingresa articulo 3")
        time.sleep(1)

        ccantidad3_dco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        ccantidad3_dco.click()
        time.sleep(1)
        ccantidad3_dco.send_keys(Configuracion.cantidad_art1)
        Log().info(" Ingresa la cantidad del articulo ")

        aceptar3_dco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        time.sleep(1)
        aceptar3_dco.click()
        Log().info(" Se presiona el boton 'aceptar', para ingresar el articulo y la cantidad.")
        time.sleep(2)

        # ------------------------------------- Ingreso articulo 4 -----------------------------------------
        articulo4_dco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        time.sleep(1)
        articulo4_dco.send_keys(Configuracion.codigo_art4_vco)
        Log().info(" Ingresa articulo 4")
        time.sleep(1)

        ccantidad4_dco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        ccantidad4_dco.click()
        time.sleep(1)
        ccantidad4_dco.send_keys(Configuracion.cantidad_art1)
        Log().info(" Ingresa la cantidad del articulo ")

        aceptar4_dco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        time.sleep(1)
        aceptar4_dco.click()
        Log().info(" Se presiona el boton 'aceptar', para ingresar el articulo y la cantidad.")
        time.sleep(2)

        cancelar4_dco = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cancelar)))
        time.sleep(1)
        cancelar4_dco.click()
        Log().info(" Se presiona el boton 'Cancelar', para mostrar la informacion del reporte.")
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudieron agregar los articulos al documento, validar error: : {e}")
        raise


def impuesto_venta(self):
    try:
        info_venta = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_info_art)))
        info_venta.click()
        Log().info("Se da click a la información a detalle de la venta de contado")
        time.sleep(2)

        valida_iva = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.ivaventaanu))).text
        self.assertEqual("300.66", valida_iva, "El IVA es correcto")
        Log().info("El IVA de la venta es correcto")
        time.sleep(1)

        valida_total = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.totalventaanu))).text
        self.assertEqual("2,179.76", valida_total, "El total es correcto")
        Log().info("El total de la venta es correcto")
        time.sleep(1)

        cerrar_info = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar)))
        cerrar_info.click()
        Log().info("Se cierra información a detalle de la venta de contado")

        # guarda el documento venta de contado
        guarda = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_guarda)))
        time.sleep(1)
        guarda.click()
        Log().info(" Se da clic en el boton guardar; se emite el documento.")

    except Exception as e:  # pragma: no cover
        Log().error(f"El detalle de la venta no es correcto validar IVA / Total: {e}")
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
        Log().info(" Se encontro y abrio el documento emitido ")
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se encontró el documento: {e}")
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
        Log().error(f"Error al encontrar el documento: {e}")
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
        Log().error(f"Error al presionar botón cerrar: {e}")
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
        Log().info(" Se encontro y abrio el documento emitido ")
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"Error al abrir el documento, validar error: {e}")
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
        Log().error(f"Error al obtener serie y número de documento: {e}")
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
        Log().info(" Se encontro y abrio el documento emitido ")
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"Error al encontrar doc, validar: {e}")
        raise

    try:
        cierra_todo2 = wait.until(EC.presence_of_element_located
                                  ((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[3]")))
        cierra_todo2.click()
        Log().info(" Se presiona el boton 'Cerrar', para cerrar el documento de venta.")
        time.sleep(2)

        # cierra_todo_2 = wait.until(EC.presence_of_element_located
        #                          ((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[2]")))
        # cierra_todo_2.click()
        # Log().info(" Se presiona el boton 'Cerrar', para cerrar pantalla de documentos emitidos.")
        # time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"Error al cerrar documento de venta: {e}")
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
        time.sleep(4)
    except Exception as e:  # pragma: no cover
        Log().error(f"Error al ingresar el número de documento: {e}")
        raise


def anular():
    # Busca el documento que creamos y abre el menú
    try:
        busqueda_docemitido_anular = wait.until(
            EC.presence_of_element_located((By.XPATH, Configuracion.busqueda_odocemitido)))
        busqueda_docemitido_anular.click()
        action \
            .click(busqueda_docemitido_anular) \
            .pause(0) \
            .context_click(busqueda_docemitido_anular) \
            .pause(0) \
            .release()
        action.perform()
        Log().info(" Se encontro y abrio el menu ")
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se encontro/abrio el menú: {e}")
        time.sleep(2)
        raise

    # Da clic en anular
    try:
        anular1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_anular)))
        anular1.click()
        Log().info(" Selecciona las ventas y las anula ")
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se dio clic en anular: {e}")
        time.sleep(2)
        raise

    # Ingresamos motivo de anulacion
    try:
        motivo_ayuda = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_ayuda)))
        motivo_ayuda.click()

        motivo_anulacion = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.motivo_anulacion)))
        action \
            .double_click(motivo_anulacion) \
            .pause(0) \
            .release()
        action.perform()
        # Log().info(" Se agrega motivo de anulacion ")
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se agrego motivo de anulacion: {e}")
        time.sleep(2)
        raise

    # Da clic en aceptar
    try:
        aceptar_anular = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        aceptar_anular.click()
        Log().info(" Se dio clic en aceptar ")
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se dio clic en aceptar: {e}")
        time.sleep(2)
        raise

    # Ordena por columna observaciones
    try:
        ordenarcobservaciones = wait.until(
            EC.presence_of_element_located((By.XPATH, Configuracion.columna_observaciones)))
        ordenarcobservaciones.click()
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se ordeno la columna observaciones: {e}")
        time.sleep(2)
        raise

    try:
        ordenarcobservaciones2 = wait.until(
            EC.presence_of_element_located((By.XPATH, Configuracion.columna_observaciones)))
        ordenarcobservaciones2.click()
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se ordeno la columna observaciones: {e}")
        time.sleep(2)
        raise

    try:
        cierra_todo_anular = wait.until(EC.presence_of_element_located
                                        ((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[2]")))
        cierra_todo_anular.click()
        Log().info(" Se presiona el boton 'Cerrar', para cerrar pantalla de documentos emitidos.")
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"Error al cerrar pantalla documentos emitidos: {e}")
        raise


# ---------------------------------- Inicio de la automatización DCO06---------------------------------------------

class Test(unittest.TestCase):

    def test_000(self):
        """Ingreso a Chrome"""
        return ingreso_chrome()

    def test_001(self):
        """Ingreso a Power Street"""
        return funciones.ingresologin(self)

    def test_002(self):
        """Ingreso a articulos"""
        tablas = wait.until(EC.presence_of_element_located
                            ((By.XPATH, Configuracion.menu_tablas)))
        tablas.click()
        return funciones.ingreso_tabla_articulos(self)

    def test_003(self):
        """Validación de articulos"""
        return validar_articulos()

    def test_004(self):
        """Ingreso a Reportes DZ"""
        return funciones.ingresoreportes_dz(self)

    def test_005(self):
        """Validación del reporte DZ"""
        return validacion_dz()

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

    # def test_010(self):
    #     """Validación de reporte DZ"""
    #     return validacion_dz()

    def test_011(self):
        """Se ingresa a documentos emitidos"""
        return funciones.documentos_emitidos(self)

    def test_012(self):
        """Se abre el documento emitido"""
        return documento_emitido()

    def test_013(self):
        """Se ingresa a devolucion de contado"""
        return funciones.devolucion_contado(self)

    def test_014(self):
        """Se ingresan los datos al documento"""
        return datos_dco()

    def test_015(self):
        """Se valida el impuesto del documento"""
        return impuesto_venta(self)

    def test_016(self):
        """Reingreso a reportes DZ"""
        return funciones.reingreso_reporte_dz(self)

    # def test_017(self):
    #     """Validación de reporte DZ"""
    #     return validacion_dz()

    def test_018(self):
        """Reingreso documentos emitidos"""
        return funciones.documentos_emitidos(self)

    def test_019(self):
        """Se abre documento emitido"""
        return documento_emitido2()

    def test_020(self):
        """Se anula documento"""
        return anular()

    def test_021(self):
        """Reingreso a reportes DZ"""
        return funciones.reingreso_reporte_dz2(self)

    #
    # def test_021(self):
    #     """Se ingresa al reporte Docarti"""
    #     return funciones.tabla_docarti_dco(self)
    #
    # def test_022(self):
    #     """Se ingresa el número de documento"""
    #     return num_doc()

    # def test_022(self):
    #     """Se vizualiza el campo devolución"""
    #     return funciones.col_devolucion(self)
