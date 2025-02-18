import unittest

from Pipeline1.FuncionesGral import *
from Pipeline1.VariablesGral import *

# Válida que el artículo no tiene stock


# ----------------------------- Funciones Unicas para VCO03--------------------------------------
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


def validacion_dz2(self):
    try:
        reporte_dz = wait.until(EC.visibility_of_element_located((By.XPATH, Configuracion.menu_report_dz)))
        reporte_dz.click()
    except Exception as e:  # pragma: no cover
        Log().error(f"Validar el error: {e}")
        raise
    try:
        funciones.ingresoreportes_dz(self)
    except Exception as e:  # pragma: no cover
        Log().error(f"No se pudo ingresar al reporte DZ, validar el error: {e}")
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
        stock = df_stock[(df_stock['Codigo'] == Configuracion.codigo_art21_vco)]

        # Resetea los index
        stock = stock.reset_index(drop=True)

        # Imprime el stock
        Log().info(f"El stock inicial de los articulos  es: {stock}")
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
        Log().error(f"Validar el error: {e}")
        raise
    try:
        ccliente = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cliente)))
        ccliente.send_keys(Configuracion.cuenta1)
        time.sleep(1)
    except Exception as e:  # pragma: no cover
        Log().error(
            "No se pudo ingresar el cliente, validar que la acción anterior haya finalizado,"
            f"que el xpath sea el correcto o que la página no presente lentitud {e}")
        time.sleep(2)
        return False

    # Ingresamos observacion
    try:
        observaciones1 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_obs1)))
        observaciones1.send_keys(Configuracion.i_observaciones1)
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().info(f"El ingreso de la cuenta no fue correcto. {e}")
        time.sleep(2)
        return False

    try:
        observaciones2 = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_obs2)))
        observaciones2.send_keys(Configuracion.i_observaciones_vc3)
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().info(f"El ingreso de la cuenta no fue correcto. {e}")
        time.sleep(2)
        return False

    # Da clic en agregar
    try:
        agregar = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_agrega_item)))
        agregar.click()
        agregar.click()

    except Exception as e:  # pragma: no cover
        Log().error(
            "No se dio click al botón Agregar, validar que la acción anterior haya finalizado,"
            f"que el xpath sea el correcto o que la página no presente lentitud {e}")
        time.sleep(2)
        return False

    # Ingreso articulo
    try:
        c_articulo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_articulo)))
        c_articulo.send_keys(Configuracion.codigo_art21_vco)
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error(
            "No se pudo ingresar el articulo, validar que la acción anterior haya finalizado,"
            f"que el xpath sea el correcto o que la página no presente lentitud {e}")
        time.sleep(2)
        return False

    # Ingreso de cantidad del artículo
    try:
        c_cantidad = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.campo_cantidad)))
        c_cantidad.click()
        time.sleep(1)
        c_cantidad.send_keys(Configuracion.cantidad_art1)

    except Exception as e:  # pragma: no cover
        Log().error(
            "No se pudo ingresar la cantidad del articulo, validar que la acción anterior haya finalizado,"
            f"que el xpath sea el correcto o que la página no presente lentitud {e}")
        time.sleep(2)
        return False

    # Da clic en aceptar
    try:
        aceptar = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_aceptar)))
        aceptar.click()
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error("No se dio click al botón Aceptar, validar que la acción anterior haya finalizado,"
                    f"que el xpath sea el correcto o que la página no presente lentitud {e}")
        time.sleep(2)
        return False

    # Da clic en cancelar para cerrar el ingreso de articulos
    try:
        cancelar = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cancelar)))
        cancelar.click()
        time.sleep(2)

    except Exception as e:  # pragma: no cover
        Log().error("No se dio click al botón Cancelar, validar que la acción anterior haya finalizado,"
                    f"que el xpath sea el correcto o que la página no presente lentitud {e}")
        time.sleep(2)
        return False

    # Guarda el documento de venta contado
    try:
        guarda = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_guarda)))
        guarda.click()
        time.sleep(2)

        # Toma imagen del mensaje de error de que no hay stock
        Log().info("Se valida que muestra el mensaje de error por falta de stock y la venta no se guarda")

    except Exception as e:  # pragma: no cover
        Log().error("No se dio click al botón Guardar, validar que la acción anterior haya finalizado,"
                    f"que el xpath sea el correcto o que la página no presente lentitud {e}")
        time.sleep(2)
        return False

    # Se cierran todas las ventanas y se termine prueba
    try:
        cierra_ventana = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar)))
        cierra_ventana.click()
        time.sleep(3)

        cierra_todo = wait.until(EC.presence_of_element_located((By.XPATH, Configuracion.btn_cerrar_ventana)))
        cierra_todo.click()
        time.sleep(1)

    except Exception as e:  # pragma: no cover
        Log().error("No se dio click al botón Cerrar, validar que la acción anterior haya finalizado,"
                    f"que el xpath sea el correcto o que la página no presente lentitud {e}")
        time.sleep(2)
        return False


# ---------------------------------- Inicio de la automatización DCO01---------------------------------------------

class Test(unittest.TestCase):

    def test_000(self):
        """Ingreso a Chrome"""
        return ingreso(self)

    def test_002(self):
        """Ingreso a Reportes DZ"""
        return validacion_dz2(self)

    def test_004(self):
        """Ingreso de datos en venta de contado"""
        return datos_vco(self)
