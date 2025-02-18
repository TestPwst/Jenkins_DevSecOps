import unittest

from Pipeline1.FuncionesGral import *
from Pipeline1.VariablesGral import *
global numero_serie
global numero_documento


# ----------------------------- Funciones Unicas para VCO05--------------------------------------


def ingreso(self):
    try:
        ingreso_chrome()
        Log().info(
            "Venta de Contado número 5: Venta Contado 20 items")
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar correctamente a Chrome, favor de validar el error: {e}")
        raise
    try:
        funciones.ingresologin(self)
    except Exception as e:  # pragma: no cover
        Log().error(f" El ingreso al loggin no fue correcto, favor de validar el siguiente error: {e}")
        raise


# Se realiza la validación del stock del vendedor
def validacion_dz1(self):
    try:
        reportes_dz = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.menu_report_dz)))
        reportes_dz.click()
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logro dar click al menú reportes DZ, validar el error: {e}")
        raise
    try:
        funciones.ingresoreportes_dz(self)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar a reportes DZ, validar el error: {e}")
        raise
        # Obtiene tabla de reporte de stock
    try:
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, Configuracion.frame_reporte1)))

        # Obtiene tabla de reporte de stock
        tablareporte1 = driver.find_element(By.XPATH, Configuracion.tabla_reporte1).get_attribute('outerHTML')
        stocktable_df = pd.read_html(StringIO(tablareporte1))[0]

        # Hace una copia de la tabla, obteniendo solo las columnas de Codigo y Saldo
        df_stock = stocktable_df[['Codigo', 'Saldo']].copy()
        # Limpia la tabla
        df_stock = df_stock.dropna()
        df_stock = df_stock.drop(0)

        # Filtra por codigo de articulo
        stockinicial = df_stock[(df_stock['Codigo'] == Configuracion.codigo_art1_vco)
                                | (df_stock['Codigo'] == Configuracion.codigo_art2_vco)
                                | (df_stock['Codigo'] == Configuracion.codigo_art3_vco)
                                | (df_stock['Codigo'] == Configuracion.codigo_art4_vco)
                                | (df_stock['Codigo'] == Configuracion.codigo_art5_vco)
                                | (df_stock['Codigo'] == Configuracion.codigo_art6_vco)
                                | (df_stock['Codigo'] == Configuracion.codigo_art7_vco)
                                | (df_stock['Codigo'] == Configuracion.codigo_art8_vco)
                                | (df_stock['Codigo'] == Configuracion.codigo_art9_vco)
                                | (df_stock['Codigo'] == Configuracion.codigo_art10_vco)
                                | (df_stock['Codigo'] == Configuracion.codigo_art11_vco)
                                | (df_stock['Codigo'] == Configuracion.codigo_art12_vco)
                                | (df_stock['Codigo'] == Configuracion.codigo_art13_vco)
                                | (df_stock['Codigo'] == Configuracion.codigo_art14_vco)
                                | (df_stock['Codigo'] == Configuracion.codigo_art15_vco)
                                | (df_stock['Codigo'] == Configuracion.codigo_art16_vco)
                                | (df_stock['Codigo'] == Configuracion.codigo_art17_vco)
                                | (df_stock['Codigo'] == Configuracion.codigo_art18_vco)
                                | (df_stock['Codigo'] == Configuracion.codigo_art19_vco)
                                | (df_stock['Codigo'] == Configuracion.codigo_art20_vco)]

        # Resetea los index
        stockinicial = stockinicial.reset_index(drop=True)

        # Imprime el stock
        Log().info(f"El stock inicial de los articulos es: {stockinicial}")

        # Regresamos a la ventana principal
        driver.switch_to.default_content()

    except Exception as e:  # pragma: no cover
        Log().error(f"No se obtuvo datos de la tabla Reportes DZ, validar el error: {e}")
        time.sleep(2)
        raise


def validacion_dz2():
    try:
        refresh_reporte1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_actualizareporte)))
        time.sleep(1)
        refresh_reporte1.click()
        time.sleep(5)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar a reportes DZ, validar el error: {e}")
        raise
        # Obtiene tabla de reporte de stock
    try:
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, Configuracion.frame_reporte1)))

        # Obtiene tabla de reporte de stock
        tablareporte2 = driver.find_element(By.XPATH, Configuracion.tabla_reporte1).get_attribute('outerHTML')
        stocktable_df1 = pd.read_html(StringIO(tablareporte2))[0]

        # Hace una copia de la tabla, obteniendo solo las columnas de Codigo y Saldo
        df_stock = stocktable_df1[['Codigo', 'Saldo']].copy()
        # Limpia la tabla
        df_stock = df_stock.dropna()
        df_stock = df_stock.drop(0)

        # Filtra por codigo de articulo
        stock_final = df_stock[(df_stock['Codigo'] == Configuracion.codigo_art1_vco)
                               | (df_stock['Codigo'] == Configuracion.codigo_art2_vco)
                               | (df_stock['Codigo'] == Configuracion.codigo_art3_vco)
                               | (df_stock['Codigo'] == Configuracion.codigo_art4_vco)
                               | (df_stock['Codigo'] == Configuracion.codigo_art5_vco)
                               | (df_stock['Codigo'] == Configuracion.codigo_art6_vco)
                               | (df_stock['Codigo'] == Configuracion.codigo_art7_vco)
                               | (df_stock['Codigo'] == Configuracion.codigo_art8_vco)
                               | (df_stock['Codigo'] == Configuracion.codigo_art9_vco)
                               | (df_stock['Codigo'] == Configuracion.codigo_art10_vco)
                               | (df_stock['Codigo'] == Configuracion.codigo_art11_vco)
                               | (df_stock['Codigo'] == Configuracion.codigo_art12_vco)
                               | (df_stock['Codigo'] == Configuracion.codigo_art13_vco)
                               | (df_stock['Codigo'] == Configuracion.codigo_art14_vco)
                               | (df_stock['Codigo'] == Configuracion.codigo_art15_vco)
                               | (df_stock['Codigo'] == Configuracion.codigo_art16_vco)
                               | (df_stock['Codigo'] == Configuracion.codigo_art17_vco)
                               | (df_stock['Codigo'] == Configuracion.codigo_art18_vco)
                               | (df_stock['Codigo'] == Configuracion.codigo_art19_vco)
                               | (df_stock['Codigo'] == Configuracion.codigo_art20_vco)]

        # Resetea los index
        stock_final = stock_final.reset_index(drop=True)

        # Imprime el stock
        Log().info(f"El stock final de los articulos es: {stock_final}")

        # Regresamos a la ventana principal
        driver.switch_to.default_content()
        time.sleep(1)

        cierra_reporte = wait.until(EC.presence_of_element_located
                                    ((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[1]")))
        cierra_reporte.click()
        Log().info(" Se presiona el boton 'Cerrar'")
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se obtuvo datos de la tabla Reportes DZ, validar el error: {e}")
        time.sleep(2)
        raise


# Se inicia con la creación del documento de venta contado
def datos_vco(self):
    try:
        funciones.venta_contado(self)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logro acceder al documento venta de contado, validar el error: {e}")
        raise
    try:
        cliente = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cliente)))
        cliente.send_keys(Configuracion.cuenta1)
        time.sleep(1)
        Log().info("Se agregar al cliente 0010051428 para realizar la venta linea de neogocios no permitida")

        observaciones1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_obs1)))
        observaciones1.send_keys(Configuracion.i_observaciones1)
        time.sleep(1)
        Log().info("Se ingresa la observación 1 al documento")

        observaciones2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_obs2)))
        observaciones2.send_keys(Configuracion.i_observaciones_vco5)
        time.sleep(1)
        Log().info("Se ingresa la observación 2 al documento")

        agregaitem = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_agrega_item)))
        agregaitem.click()
        agregaitem.click()

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró dar click para agregar items a la venta. {e}")
        time.sleep(2)
        return False

    # Verifica si tiene el atributo precio unitario
    try:
        funciones.validar_atributo_precio(self)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se encontró el atributo precio unitario {e}")
        time.sleep(2)
        raise


def ingreso_20_art():
    # Se agregan el item 1/20
    try:
        item1 = wait.until(EC.visibility_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        wait.until(EC.visibility_of(item1))
        item1.click()
        time.sleep(1)
        item1.send_keys(Configuracion.codigo_art1_vco)
        Log().info("se ingresa articulo 1")
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar el código del artículo a comprar. {e}")
        time.sleep(2)
        return False

    try:
        cantidaditem1 = wait.until(EC.visibility_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        wait.until(EC.visibility_of(cantidaditem1))
        cantidaditem1.click()
        time.sleep(1)
        cantidaditem1.send_keys(Configuracion.cantidad_art1)
        Log().info(
            f"Se ingresa cantidad de: {Configuracion.cantidad_art1}, al articulo: {Configuracion.codigo_art1_vco}")
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar la cantidad del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        aceptaitem1 = wait.until(EC.element_to_be_clickable((By.XPATH, Configuracion.btn_aceptar)))
        wait.until(EC.visibility_of(aceptaitem1))
        time.sleep(1)
        aceptaitem1.click()
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró dar click en el botón aceptar. {e}")
        time.sleep(2)
        return False

    # Se agregan el item 2/20
    try:
        item2 = wait.until(EC.visibility_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        wait.until(EC.visibility_of(item2))
        item2.click()
        time.sleep(1)
        item2.send_keys(Configuracion.codigo_art2_vco)
        Log().info("se ingresa articulo 2")
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar el código del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        cantidaditem2 = wait.until(EC.visibility_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        wait.until(EC.visibility_of(cantidaditem2))
        cantidaditem2.click()
        time.sleep(1)
        cantidaditem2.send_keys(Configuracion.cantidad_art2)
        Log().info(
            f"Se ingresa cantidad de: {Configuracion.cantidad_art2}, al articulo: {Configuracion.codigo_art2_vco}")
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar la cantidad del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        aceptaitem2 = wait.until(EC.element_to_be_clickable((By.XPATH, Configuracion.btn_aceptar)))
        wait.until(EC.visibility_of(aceptaitem2))
        time.sleep(1)
        aceptaitem2.click()
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró dar click en el botón aceptar.{e}")
        time.sleep(2)
        return False

    # Se agregan el item 3/20
    try:
        item3 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        wait.until(EC.visibility_of(item3))
        item3.click()
        time.sleep(1)
        item3.send_keys(Configuracion.codigo_art3_vco)
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar el código del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        cantidaditem3 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        wait.until(EC.visibility_of(cantidaditem3))
        cantidaditem3.click()
        time.sleep(1)
        cantidaditem3.send_keys(Configuracion.cantidad_art3)
        Log().info(
            f"Se ingresa cantidad de: {Configuracion.cantidad_art3}, al articulo: {Configuracion.codigo_art3_vco}")
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar la cantidad del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        aceptaitem3 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        wait.until(EC.visibility_of(aceptaitem3))
        time.sleep(1)
        aceptaitem3.click()
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró dar click en el botón aceptar. {e}")
        time.sleep(2)
        return False

    # Se agregan el item 4/20
    try:
        item4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        wait.until(EC.visibility_of(item4))
        item4.click()
        time.sleep(1)
        item4.send_keys(Configuracion.codigo_art4_vco)
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar el código del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        cantidaditem4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        wait.until(EC.visibility_of(cantidaditem4))
        cantidaditem4.click()
        time.sleep(1)
        cantidaditem4.send_keys(Configuracion.cantidad_art4)
        Log().info(
            f"Se ingresa cantidad de: {Configuracion.cantidad_art4}, al articulo: {Configuracion.codigo_art4_vco}")
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar la cantidad del artículo a comprar. {e}")
        time.sleep(2)
        return False

    try:
        aceptaitem4 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        wait.until(EC.visibility_of(aceptaitem4))
        time.sleep(1)
        aceptaitem4.click()
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró dar click en el botón aceptar. {e}")
        time.sleep(2)
        return False

    # Se agregan el item 5/20
    try:
        item5 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        wait.until(EC.visibility_of(item5))
        item5.click()
        time.sleep(1)
        item5.send_keys(Configuracion.codigo_art5_vco)
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar el código del artículo a comprar. {e}")
        time.sleep(2)
        return False

    try:
        cantidaditem5 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        wait.until(EC.visibility_of(cantidaditem5))
        cantidaditem5.click()
        time.sleep(1)
        cantidaditem5.send_keys(Configuracion.cantidad_art5)
        Log().info(
            f"Se ingresa cantidad de: {Configuracion.cantidad_art5}, al articulo: {Configuracion.codigo_art5_vco}")
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar la cantidad del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        aceptaitem5 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        wait.until(EC.visibility_of(aceptaitem5))
        time.sleep(1)
        aceptaitem5.click()
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró dar click en el botón aceptar.{e}")
        time.sleep(2)
        return False

    # Se agregan el item 6/20
    try:
        item6 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        wait.until(EC.visibility_of(item6))
        item6.click()
        time.sleep(1)
        item6.send_keys(Configuracion.codigo_art6_vco)
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar el código del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        cantidaditem6 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        wait.until(EC.visibility_of(cantidaditem6))
        cantidaditem6.click()
        time.sleep(1)
        cantidaditem6.send_keys(Configuracion.cantidad_art1)
        Log().info(
            f"Se ingresa cantidad de: {Configuracion.cantidad_art1}, al articulo: {Configuracion.codigo_art6_vco}")
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar la cantidad del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        aceptaitem6 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        wait.until(EC.visibility_of(aceptaitem6))
        time.sleep(1)
        aceptaitem6.click()
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró dar click en el botón aceptar.{e}")
        time.sleep(2)
        return False

    # Se agregan el item 7/20
    try:
        item7 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        wait.until(EC.visibility_of(item7))
        item7.click()
        time.sleep(1)
        item7.send_keys(Configuracion.codigo_art7_vco)
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar el código del artículo a comprar. {e}")
        time.sleep(2)
        return False

    try:
        cantidaditem7 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        wait.until(EC.visibility_of(cantidaditem7))
        cantidaditem7.click()
        time.sleep(1)
        cantidaditem7.send_keys(Configuracion.cantidad_art2)
        Log().info(
            f"Se ingresa cantidad de: {Configuracion.cantidad_art2}, al articulo: {Configuracion.codigo_art7_vco}")
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar la cantidad del artículo a comprar. {e}")
        time.sleep(2)
        return False

    try:
        aceptaitem7 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        wait.until(EC.visibility_of(aceptaitem7))
        time.sleep(1)
        aceptaitem7.click()
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró dar click en el botón aceptar. {e}")
        time.sleep(2)
        return False

    # Se agregan el item 8/20
    try:
        item8 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        wait.until(EC.visibility_of(item8))
        item8.click()
        time.sleep(1)
        item8.send_keys(Configuracion.codigo_art8_vco)
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar el código del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        cantidaditem8 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        wait.until(EC.visibility_of(cantidaditem8))
        cantidaditem8.click()
        time.sleep(1)
        cantidaditem8.send_keys(Configuracion.cantidad_art3)
        Log().info(
            f"Se ingresa cantidad de: {Configuracion.cantidad_art3}, al articulo: {Configuracion.codigo_art8_vco}")
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar la cantidad del artículo a comprar. {e}")
        time.sleep(2)
        return False

    try:
        aceptaitem8 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        wait.until(EC.visibility_of(aceptaitem8))
        time.sleep(1)
        aceptaitem8.click()
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró dar click en el botón aceptar.{e}")
        time.sleep(2)
        return False

    # Se agregan el item 9/20
    try:
        item9 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        wait.until(EC.visibility_of(item9))
        item9.click()
        time.sleep(1)
        item9.send_keys(Configuracion.codigo_art9_vco)
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar el código del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        cantidaditem9 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        wait.until(EC.visibility_of(cantidaditem9))
        cantidaditem9.click()
        time.sleep(1)
        cantidaditem9.send_keys(Configuracion.cantidad_art4)
        Log().info(
            f"Se ingresa cantidad de: {Configuracion.cantidad_art4}, al articulo: {Configuracion.codigo_art9_vco}")
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar la cantidad del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        aceptaitem9 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        wait.until(EC.visibility_of(aceptaitem9))
        time.sleep(1)
        aceptaitem9.click()
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró dar click en el botón aceptar.{e}")
        time.sleep(2)
        return False

    # Se agregan el item 10/20
    try:
        item10 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        wait.until(EC.visibility_of(item10))
        item10.click()
        time.sleep(1)
        item10.send_keys(Configuracion.codigo_art10_vco)
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar el código del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        cantidaditem10 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        wait.until(EC.visibility_of(cantidaditem10))
        cantidaditem10.click()
        time.sleep(1)
        cantidaditem10.send_keys(Configuracion.cantidad_art5)
        Log().info(
            f"Se ingresa cantidad de: {Configuracion.cantidad_art5}, al articulo: {Configuracion.codigo_art10_vco}")
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar la cantidad del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        aceptaitem10 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        wait.until(EC.visibility_of(aceptaitem10))
        time.sleep(1)
        aceptaitem10.click()
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró dar click en el botón aceptar. {e}")
        time.sleep(2)
        return False

    # Se agregan el item 11/20
    try:
        item11 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        item11.send_keys(Configuracion.codigo_art11_vco)
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar el código del artículo a comprar. {e}")
        time.sleep(2)
        return False

    try:
        cantidaditem11 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        cantidaditem11.click()
        time.sleep(1)
        cantidaditem11.send_keys(Configuracion.cantidad_art1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar la cantidad del artículo a comprar. {e}")
        time.sleep(2)
        return False

    try:
        aceptaitem11 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        aceptaitem11.click()
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró dar click en el botón aceptar.{e}")
        time.sleep(2)
        return False

    # Se agregan el item 12/20
    try:
        item12 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        item12.send_keys(Configuracion.codigo_art12_vco)
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar el código del artículo a comprar. {e}")
        time.sleep(2)
        return False

    try:
        cantidaditem12 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        cantidaditem12.click()
        time.sleep(1)
        cantidaditem12.send_keys(Configuracion.cantidad_art2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar la cantidad del artículo a comprar. {e}")
        time.sleep(2)
        return False

    try:
        aceptaitem12 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        aceptaitem12.click()
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró dar click en el botón aceptar. {e}")
        time.sleep(2)
        return False

    # Se agregan el item 13/20
    try:
        item13 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        item13.send_keys(Configuracion.codigo_art13_vco)
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar el código del artículo a comprar. {e}")
        time.sleep(2)
        return False

    try:
        cantidaditem13 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        cantidaditem13.click()
        time.sleep(1)
        cantidaditem13.send_keys(Configuracion.cantidad_art3)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar la cantidad del artículo a comprar. {e}")
        time.sleep(2)
        return False

    try:
        aceptaitem13 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        aceptaitem13.click()
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró dar click en el botón aceptar. {e}")
        time.sleep(2)
        return False

    # Se agregan el item 14/20
    try:
        item14 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        item14.send_keys(Configuracion.codigo_art14_vco)
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar el código del artículo a comprar. {e}")
        time.sleep(2)
        return False

    try:
        cantidaditem14 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        cantidaditem14.click()
        time.sleep(1)
        cantidaditem14.send_keys(Configuracion.cantidad_art4)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar la cantidad del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        aceptaitem14 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        aceptaitem14.click()
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró dar click en el botón aceptar.{e}")
        time.sleep(2)
        return False

    # Se agregan el item 15/20
    try:
        item15 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        item15.send_keys(Configuracion.codigo_art15_vco)
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar el código del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        cantidaditem15 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        cantidaditem15.click()
        time.sleep(1)
        cantidaditem15.send_keys(Configuracion.cantidad_art5)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar la cantidad del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        aceptaitem15 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        aceptaitem15.click()
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró dar click en el botón aceptar.{e}")
        time.sleep(2)
        return False

    # Se agregan el item 16/20
    try:
        item16 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        item16.send_keys(Configuracion.codigo_art16_vco)
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar el código del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        cantidaditem16 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        cantidaditem16.click()
        time.sleep(1)
        cantidaditem16.send_keys(Configuracion.cantidad_art1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar la cantidad del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        aceptaitem16 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        aceptaitem16.click()
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró dar click en el botón aceptar.{e}")
        time.sleep(2)
        return False

    # Se agregan el item 17/20
    try:
        item17 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        item17.send_keys(Configuracion.codigo_art17_vco)
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar el código del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        cantidaditem17 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        cantidaditem17.click()
        time.sleep(1)
        cantidaditem17.send_keys(Configuracion.cantidad_art2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar la cantidad del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        aceptaitem17 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        aceptaitem17.click()
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró dar click en el botón aceptar.{e}")
        time.sleep(2)
        return False

    # Se agregan el item 18/20
    try:
        item18 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        item18.send_keys(Configuracion.codigo_art18_vco)
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar el código del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        cantidaditem18 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        cantidaditem18.click()
        time.sleep(1)
        cantidaditem18.send_keys(Configuracion.cantidad_art3)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar la cantidad del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        aceptaitem18 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        aceptaitem18.click()
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró dar click en el botón aceptar.{e}")
        time.sleep(2)
        return False

    # Se agregan el item 19/20
    try:
        item19 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        item19.send_keys(Configuracion.codigo_art19_vco)
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar el código del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        cantidaditem19 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        cantidaditem19.click()
        time.sleep(1)
        cantidaditem19.send_keys(Configuracion.cantidad_art4)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar la cantidad del artículo a comprar, validar el error: {e}")
        time.sleep(2)
        return False

    try:
        aceptaitem19 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        aceptaitem19.click()
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró dar click en el botón aceptar. {e}")
        time.sleep(2)
        return False

    # Se agregan el item 20/20
    try:
        item20 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        item20.send_keys(Configuracion.codigo_art20_vco)
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar el código del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        cantidaditem20 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        cantidaditem20.click()
        time.sleep(1)
        cantidaditem20.send_keys(Configuracion.cantidad_art5)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró ingresar la cantidad del artículo a comprar.{e}")
        time.sleep(2)
        return False

    try:
        aceptaitem20 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        aceptaitem20.click()
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró dar click en el botón aceptar.{e}")
        time.sleep(2)
        return False

    try:
        cerraritem = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cancelar)))
        cerraritem.click()
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error(f"No se logró dar click en el botón Cerrar.{e}")
        time.sleep(2)
        return False


# Ingresar al documento de Preventa Contado
def documento_emitido(self):
    try:
        funciones.documentos_emitidos(self)
    except Exception as e:  # pragma: no cover
        Log().error(f"Validar el error. {e}")
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
        Log().error(f"Validar el error. {e}")
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
        Log().error(f"Validar el error. {e}")
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
        Log().error(f"Validar el error. {e}")
        raise


def impuesto_venta(self):
    try:
        infoventa = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_info_art)))
        infoventa.click()
        Log().info("Se da click a la información a detalle de la venta de contado")
        time.sleep(2)

        valida_iva = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.iva_venta_contado5))).text
        self.assertEqual("4,066.27", valida_iva, "El IVA es correcto")
        Log().info("El IVA de la venta es correcto")
        time.sleep(1)

        validatotal = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.total_venta_contado5))).text
        self.assertEqual("29,480.47", validatotal, "El total es correcto")
        Log().info("El total de la venta es correcto")
        time.sleep(1)

        cerrarinfo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar)))
        cerrarinfo.click()
        Log().info("Se cierra información a detalle de la venta de contado")

        # Guarda el documento venta de contado
        guarda = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_guarda)))
        time.sleep(1)
        guarda.click()
        Log().info(" Se da clic en el boton Guardar; se emite el documento.")
        time.sleep(2)
    except Exception as e:  # pragma: no cover
        Log().error(f"Validar el error. {e}")
        raise


def impuesto_venta_valida(self):
    try:
        infoventa1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_info_art)))
        infoventa1.click()
        Log().info("Se da click a la información a detalle de la venta de contado")
        time.sleep(2)

        valida_iva1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.iva_venta_contado5))).text
        self.assertEqual("4,066.27", valida_iva1, "El IVA es correcto")
        Log().info("El IVA de la venta es correcto")
        time.sleep(1)

        validatotal1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.total_venta_contado5))).text
        self.assertEqual("29,480.47", validatotal1, "El total es correcto")
        Log().info("El total de la venta es correcto")
        time.sleep(1)

        cerrarinfo1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar)))
        cerrarinfo1.click()
        Log().info("Se cierra información a detalle de la venta de contado")
        time.sleep(2)

        try:
            cierra_todo1 = wait.until(EC.presence_of_element_located
                                      ((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[2]")))
            cierra_todo1.click()
            Log().info(" Se presiona el boton 'Cerrar', para cerrar el documento de venta.")
            time.sleep(2)

            cierra_todo = wait.until(EC.presence_of_element_located
                                     ((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[1]")))
            cierra_todo.click()
            Log().info(" Se presiona el boton 'Cerrar', para cerrar pantalla de documentos emitidos")
            time.sleep(2)
        except Exception as e:  # pragma: no cover
            Log().error(f"error no se pudo cerrar las ventanas {e}")
            raise
    except Exception as e:  # pragma: no cover
        Log().error(f"Validar el error. {e}")
        raise


# Válida que el documento se haya emitido de forma correcta
def tabla_docarti_numero(self):
    try:
        funciones.tabla_docarti_vco(self)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se logro acceder a la tabla docarti, validar el error: {e}")
        raise
    # Ingreso numero de documento
    try:
        cnumerodoc = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_numero_doc)))
        cnumerodoc.send_keys(numero_documento)
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(
            "No se pudo ingresar el numero de documento, validar que la acción anterior haya finalizado,"
            f"que el xpath sea el correcto o que la página no presente lentitud {e}")

    # Da clic en ver
    try:
        ver = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_ver)))
        ver.click()
        time.sleep(4)
    except Exception as e:  # pragma: no cover
        Log().error("No se dio click al botón Ver, validar que la acción anterior haya finalizado,"
                    f"que el xpath sea el correcto o que la página no presente lentitud {e}")

    try:
        cierra_todo2 = wait.until(EC.presence_of_element_located
                                  ((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[2]")))
        cierra_todo2.click()
        Log().info(" Se presiona el boton 'Cerrar', para cerrar el documento de venta.")
        time.sleep(2)

        cierra_todo1 = wait.until(EC.presence_of_element_located
                                  ((By.XPATH, f"({Configuracion.btn_cerrar_pantalla})[1]")))
        cierra_todo1.click()
        Log().info(" Se presiona el boton 'Cerrar', para cerrar pantalla de documentos emitidos")
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error("No se dio click al botón Ver, validar que la acción anterior haya finalizado,"
                    f"que el xpath sea el correcto o que la página no presente lentitud {e}")


# ----------------------------- FUNCIONES EJECUTAN VCO05 --------------
class Test(unittest.TestCase):
    def test_000(self):
        """Ingreso a Chrome"""
        return ingreso(self)

    def test_003(self):
        """ingresa datos de 20 items obtiene stock"""
        return validacion_dz1(self)

    def test_005(self):
        """Crear el documento de venta"""
        return datos_vco(self)

    def test_006(self):
        """Añadir 20 articulos al documento de venta"""
        return ingreso_20_art()

    def test_007(self):
        """Válida el impuesto en el documento emitido"""
        return impuesto_venta(self)

    def test_008(self):
        """Válida que el stock haya disminuido"""
        return validacion_dz2()

    def test_009(self):
        """Válida que el documento se encuentre emitido"""
        return documento_emitido(self)

    def test_010(self):
        """Válida el impuesto en el documento emitido"""
        return impuesto_venta_valida(self)

    def test_013(self):
        """Válida que el documento se haya emitido correctamente"""
        return tabla_docarti_numero(self)
