from datetime import datetime, timedelta
from time import strftime

import os
import logging


# ------------------------------CLASE LOG---------------------------------------------
class Log:
    def __init__(self):
        self.now = strftime("%Y-%m-%d-%H")
        self.logname = os.path.join('{0}.log'.format(self.now))

    def __printconsole(self, level, message):

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler(self.logname, 'a', encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(ch)
        if level == 'info':
            logger.info(message)
        elif level == 'debug':
            logger.debug(message)
        elif level == 'warning':
            logger.warning(message)
        elif level == 'error':
            logger.error(message)
        logger.removeHandler(ch)
        logger.removeHandler(fh)
        fh.close()

    def debug(self, message):
        self.__printconsole('debug', message)

    def info(self, message):
        self.__printconsole('info', message)

    def warning(self, message):
        self.__printconsole('warning', message)

    def error(self, message):
        self.__printconsole('error', message)


# ----------------------------------CLASE CONFIGGNERAL---------------------------------


class Configuracion:
    # Datos de ingreso al ambiente
    # usuario = "te1aut006"  # versión 4
    usuario = "au03aut2"  # versión 5
    contrasena = "Pwst12345*"

    # XPATH Loggin
    ingreso_usuario = "//input[@id='txtLoginUserName']"
    ingreso_contrasena = "//input[@name='pass']"
    btn_ingresar = "//input[@type= 'submit' and @value= 'iniciar sesión']"
    btn_enterprise = "//div[@title='PowerStreet2 - Enterprise']"

    # ---------------------------ENTERPRISE----------------------------------------------
    # Variables de observaciones (Introduce una observación con los datos de la fecha y tiempo)
    current_datetime = datetime.now()
    microseconds = timedelta(microseconds=1)
    later = microseconds + current_datetime
    later2 = (microseconds * 2) + current_datetime
    later3 = (microseconds * 3) + current_datetime
    later4 = (microseconds * 4) + current_datetime
    later5 = (microseconds * 5) + current_datetime

    # Variables para el campo de observaciones
    campo_observaciones = "//input[contains(@id, 'observaciones_element')]"
    i_observaciones1 = str(current_datetime)
    i_observaciones2 = str(later)

    # XPATH menú
    btn_sandwich = "//div[@title='alternar barra de menú']"
    menulateral = "(//div[contains(@class, 'ui-startmenu-menu')]//descendant::div)[1]"

    # Configuraciones para el Buscador
    buscador = "//div[@class= 'menubarbtn quicksearch-btn']"
    input_buscador = "//input[@class= 'search-box-text']"

    # Para sesion activa
    btn_cierrasesionactiva2 = "//button[@class = 'p-continuebutton']"

    # ---------------------------VARIABLES DCO----------------------------------------
    # Valores y datos a utilzar
    cuenta = "125H000057"
    codigo_art_compo1 = "FAP02628"
    codigo_art_compo = "FAP02629"
    codigo_art_combo = "FAP02630"
    codigo_art1 = "FA01001"  # Articulo Packing
    codigo_art2 = "FA013083"  # Articulo compo
    codigo_art3 = "FAP02630"  # Articulo combo
    codigo_art4 = "FA01005 "  # Articulo Packing
    codigo_art5 = "FA01009 "  # Articulo Packing
    codigo_art6 = "FA01003"  # Articulo Unitario
    codigo_art7 = "FA03007"  # Articulo Unitario
    codigo_art8 = "FA03022"  # Articulo Unitario
    codigo_art23_vco = "FA01002"
    cantidad1 = "1"
    almacen = "1703"
    almacen_central = "1750"
    cod_tipo_doc_dco = "PM10"
    cod_tipo_doc_vco = "PM03"
    serie = "AA"
    i_observaciones_vc1 = "Venta de Contado item facturado por Packing"
    i_observaciones_dco1 = "Devolución de contado item facturado por Packing"
    i_observaciones_vc2 = "Venta de Contado item facturado por Unidad"
    i_observaciones_dco2 = "Devolución de contado item facturado por Unidad"
    i_observaciones_vc3 = "Venta de Contado Combo por Componentes"
    i_observaciones_dco3 = "Devolución de contado Combo por Componentes"
    i_observaciones_vc4 = "Venta de Contado Combo por Combo"
    i_observaciones_dco4 = "Devolución de contado Combo por Combo"
    i_observaciones_vc5 = "Venta de Contado generando una devolución de contado"
    i_observaciones_dco5 = "Devolucion de Contado generada apartir de una venta de Contado"
    i_observaciones_vc6 = "Venta de Contado items facturados por packing y unidad"
    i_observaciones_dco6 = "Anulación de una Devolución de Contado"

    # Validación de artículos
    articulo1 = "(//span[text()= 'FA01001'])[1]"
    articulo2 = "(//span[text()= 'FA01005'])[1]"
    articulo3 = "(//span[text()= 'FA01009'])[1]"
    articulo4 = "(//span[text()= 'FA03007'])[1]"
    articulo5 = "(//span[text()= 'FA03019'])[1]"
    articulo6 = "(//span[text()= 'FA03022'])[1]"
    articulo7 = "(//span[text()= 'FA09015'])[1]"
    articulo8 = "(//span[text()= 'FA09029'])[1]"
    articulo9 = "(//span[text()= 'FA09030'])[1]"
    articulo10 = "(//span[text()= 'FA09053'])[1]"
    articulo11 = "(//span[text()= 'FA02039'])[1]"
    articulo12 = "(//span[text()= 'FA002010'])[1]"
    articulo13 = "(//span[text()= 'FA003424'])[1]"
    articulo14 = "(//span[text()= 'FA007530'])[1]"
    articulo15 = "(//span[text()= 'FA013083'])[1]"
    articulo16 = "(//span[text()= '40042686'])[1]"
    articulo17 = "(//span[text()= '40041615'])[1]"
    articulo18 = "(//span[text()= '40041602'])[1]"
    articulo19 = "(//span[text()= '40041954'])[1]"
    articulo20 = "(//span[text()= '40042126'])[1]"
    articulo21 = "(//span[text()= 'FA01004'])[1]"
    articulo22 = "(//span[text()= 'FA01003'])[1]"
    articulo_comp = "(//span[text()= 'FAP02629'])[1]"
    articulo_comb = "(//span[text()= 'FAP02630'])[1]"

    # XPATH Generales
    btn_ver = "//button[text()= 'Ver']"
    btn_cerrar_ventana1 = "(//span[@class= 'ui-window-button-close'])[2]"
    btn_cerrar_ventana = "//span[@class= 'ui-window-button-close']"
    btn_aceptar = "//button[text()= 'Aceptar']"
    btn_aceptar2 = "(//button[text()= 'Aceptar'])[2]"
    btn_guarda = "//div[contains(@id, 'save_element')]"
    btn_ayuda = "//span[contains(@class, 'help')]"  # V 4.0.0.X

    # Menu y documentos
    menu_tablas = "//*[@id='_tablas']"
    menu_articulos = "//*[@id='_tablas_articulo']"
    articulos = "//*[@id='articulos']"
    filtro_art = "(//div[@class= 'tabulator-data-tree-control'])[2]"
    buscar_cod = "//div[text()= 'Activo ?']"
    filtro_codart = "//div[text()= 'Código de artículo']"
    campo_codart = "(//input[contains(@id, 'control_element')])[1]"
    btn_refresca = "//div[contains(@id, 'refresh_element')]"
    art_combo = "//button[contains(@id, '_combo_tabitem')]"
    items_doc = "//button[contains(@id, '_pagItems_tabitem')]"  # nueva
    menu_documentos = "//div[@id='_documentos']"
    menu_doc_emitidos = "//div[@id= 'verdocumentos|false']"
    menu_doc_pendientes = "//*[@id='verdocumentos|true']"
    filtro_doc_pend = "//div[text()= 'Documentos Pendientes']"
    filtro_backorder = "//div[text()= 'BackOrder ?']"
    menu_doc_clie = "//div[@id='_doc_cli']"
    menu_mas_doc = "//div[@id= 'doc_clientes_more']"
    doc_venta_contado = "//span[contains(text(),'Venta Contado')]"
    doc_preventa_contado = "//span[contains(text(),'Preventa Contado')]"
    doc_dev_contado = "(//span[text() = 'PM10' or text() = 'Devolucion Contado'])[1]"
    campo_obs1 = "//input[contains(@id, 'observaciones_element')]"
    campo_obs2 = "//input[contains(@id, 'observaciones2_element')]"
    btn_agrega_item = "//div[contains(@id, 'items|add_element')]"
    precio_venta = "//input[contains(@id, 'precioUnitario_element')]"
    btn_atributos = "//*[contains(@id, 'camposItems_element')]"
    atributo_precio = "//span[text()= 'Precio Venta']//parent::div//preceding-sibling::div//input[@type= 'checkbox']"
    tabla_reporte1 = "//table[contains(@class, 'report-data-table report-data-table')]"
    info_doc = "//div[contains(@id, 'pagGeneral_tabpage')]"
    tabla_docs = "(//span[contains(@class, 'tabulator-cell')])[2]"
    menu_herramientas = "//*[@id='_herramientas']"
    menu_exp_reportes = "//*[@id='reportexplorer']"
    titulo_pantalla = "//span[contains(@class, 'ui-window-title')]"
    btn_generar_nuevo_doc = "//span[text()= 'Generar nuevo documento']"
    campo_tipodoc_generar = "//input[contains(@id, 'tipoDocumento_element')]"
    btn_restricciones = "//button[contains(@id, 'restrinciones_tabitem')]"
    btn_aprobar = "//span[text()= 'Aprobar Emisión']"

    # Reportes DZ
    menu_report_dz = "//span[text()= 'Reportes DZ']"
    menu_stock = "//span[text()= 'Stock']"
    menu_saldos = "//span[text()= 'Saldos']"
    menu_svd = "//span[text()= 'Stock Valorizado por Deposito']"
    campo_almacen = "//input[contains(@id, 'variable_3_element')]"
    campo_lista_precio = "//input[contains(@id, 'variable_4_element')]"
    frame_reporte1 = "//iframe[contains(@id, 'report')]"
    btn_actulizareporte = ("/html/body/div[3]/div[2]/ui-container/ui-window/div[10]/div[2]/"
                           "ui-container/ui-row[1]/ui-toolband/div/span[1]/ui-toolbarbutton/div")
    btn_cerrarreporte = "/html/body/div[3]/div[2]/ui-container/ui-window/div[1]/div/span[4]"

    # obtener mensaje
    frame_mensaje = "//iframe[contains(@id, 'rpt1_element')]"
    mensaje_negritas = "//ui-errmsg//b"

    # Calculos Devolución de contado
    total_devolucion_contado4 = "//span[text()= '999.69']"
    iva_devolucion_contado4 = "//span[text()= '137.89']"

    # Venta de Contado (Calculos)
    importe_venta_contado1 = "//span[text()='1,575.90'"
    iva_venta_contado1 = "//span[text()= '252.14']"
    total_venta_contado1 = "//span[text()= '1,828.04']"
    iva_venta_contado2 = "//span[text()= '68.94']"
    total_venta_contado2 = "//span[text()= '499.84']"
    iva_venta_contado3 = "//span[text()= '186.11']"
    total_venta_contado3 = "//span[text()= '1,349.31']"
    iva_venta_contado4 = "//span[text()= '93.06']"
    total_venta_contado4 = "//span[text()= '674.66']"
    total_venta_contado5 = "//span[text()= '29,480.47']"
    iva_venta_contado5 = "//span[text()= '4,066.27']"
    total_venta_contado6 = "(//span[text()= '607.19'])[2]"
    iva_venta_contado6 = "//span[text()= '83.75']"
    iva_venta_contado7 = "//span[text()= '79.10']"
    total_venta_contado7 = "(//span[text()= '573.46'])[2]"
    iva_venta_contado8 = "//span[text()= '56.06']"
    total_venta_contado8 = "(//span[text()= '406.43'])[2]"
    iva_venta_contado9 = "//span[text()= '42.75']"
    total_venta_contado9 = "(//span[text()= '309.97'])[2]"
    iva_venta_contado10 = "//span[text()= '37.67']"
    total_venta_contado10 = "(//span[text()= '273.14'])[2]"
    iva_venta_contado11 = "//span[text()= '85.74']"
    total_venta_contado11 = "//span[text()= '621.60']"
    iva_venta_contado12 = "//span[text()= '38.27']"
    total_venta_contado12 = "(//span[text()= '277.44'])[2]"
    iva_venta_contado13 = "(//span[text()= '186.11'])[1]"
    total_venta_contado13 = "(//span[text()= '1,349.31'])[2]"

    iva_venta_contado15 = "(//span[text()= '324.00'])[1]"
    total_venta_contado15 = "(//span[text()= '2,349.00'])[1]"

    iva_venta_contado18 = "//span[text()= '209.30']"
    total_venta_contado18 = "//span[text()= '1,517.45']"

    iva_venta_contado20 = "//span[text()= '93.06']"
    total_venta_contado20 = "//span[text()= '674.66']"

    totalventadev = "//span[text()= '2,174.19']"
    ivaventadev = "//span[text()= '299.89']"
    totalventaanu = "//span[text()= '2,179.76']"
    ivaventaanu = "//span[text()= '300.66']"

    importevco07 = "(//span[text()= '430.90'])[4]"
    revisar_var = "//span[text()= '232.74']"
    revisar_var1 = "//span[text()= '1,687.34']"

    # Devolucion de contado (Calculos)
    iva_devolucion_contado2 = "//span[text()= '232.74']"
    total_devolucion_contado2 = "//span[text()= '1,687.34']"
    iva_devolucion_contado3 = "//span[text()= '186.11']"
    total_devolucion_contado3 = "//span[text()= '1,349.31']"

    # Explorador de reportes
    campo_busqueda = "//input[contains(@id, 'txtBuscarRep_element')]"
    t_reporte_docarti = "docarti no tocar"
    t_reporte_docartimpu = "docartimpu no tocar"
    reporte_docarti = "//span[contains(text(),'DOCARTI NO TOCAR')]"
    reporte_docartimpu = "//span[contains(text(),'DOCARTIMPU NO TOCAR')]"
    btn_ayuda_serie = "(//span[@class= 'help'])[2]"
    txt_serie = "//span[contains(text(),'AA')]"
    buscar_art = "//input[contains(@id, 'tbSearch_element')]"
    btn_busqueda = "//button[contains(@id, 'btnFind_element')]"
    btn_buscar = "//input[contains(@class, 'filterText')]"

    # Anular documento
    btn_anular = "//span[text()= 'Anular']"
    motivo_anulacion = "//span[text()= 'PM02']"

    # Agregar nuevo, eliminar y modificar el registro
    btn_nuevo = "//div[contains(@id, 'new_element')]"
    btn_agregar = "//div[contains(@id, '|add_element')]"

    btn_elimina1 = "//div[contains(@id, 'removecurrent_element')]"
    btn_elimina = "//a[contains(@emevt, 'emRemove')]"
    btn_cancelar = "//button[text()= 'Cancelar']"
    btn_cerrar_pantalla = "/html/body/div[3]/div[2]/ui-container/ui-window/div[1]/div/span[4]"
    btn_cerrar = "//button[text()= 'Cerrar']"
    titulo_nuevo = "/html/body/div[3]/div[2]/ui-container/ui-window[2]/div[1]/span[2]"
    btn_error = "//div[contains(@id, 'tbPanelErrors_element')]"
    btn_ver1 = "//button[contains(@id, 'viewBtn_element')]"

    etiqueta_codigo = "//*[contains(@id, 'Codigo_label_element')]"
    etiqueta_codigo_alt = "//*[contains(@id, 'codigoak_label_element')]"
    etiqueta_descripcion = "//*[contains(@id, 'Descripcion_label_element')]"
    campo_codigo = "//input[@type = 'text' and contains(@id, 'Codigo_element')]"
    campo_codigo_alt = "//input[@type = 'text' and contains(@id, 'codigoak_element')]"
    campo_descripcion = "//input[@type = 'text' and contains(@id, 'Descripcion_element')]"
    campo_unidad_negocio = "//*[contains(@id, 'UnidadNegocio_element')]"
    campo_unidad_negocio_ayuda = "//*[contains(@class, 'help')]"
    unidad_negocio = "//*[contains(@id, 'vHelpData_grid')]/div[2]/div/div[1]"
    selecciona = "//span[text()='Modifica C']"
    cerrar_ayuda = "(//span[@class = 'ui-window-button-close'])[3]"

    # FILTROS
    filtro_articulos = ("/html/body/div[3]/div[2]/ui-container/ui-window/div[10]/div[2]/"
                        "ui-container/ui-row[2]/ui-treeview/div/div/div[2]/div/div[2]/div/div[2]")
    filtro_codigo_articulo = "//div[text()= 'Código de artículo']"
    filtro_listaprecios = "//div[text()= 'Listas Precio']"
    filtro_codigo_listaprecios = "//div[text()= 'Código de lista de precios']"
    filtro_doc_emit = "//div[text()= 'Documentos Emitidos']"
    filtro_hoy = "//div[text()= 'Hoy']"
    filtro_anulado = "//div[text()= 'Anulado ?']"

    # Articulos
    campo_codigoarticulo = "//input[contains(@id, 'control_element')]"
    i_articulo1 = "54321"

    # Lista de precios
    campo_codigo_listaprecio = ("//input[contains(@id, 'control_element')]"
                                "//following::input[contains(@id, 'control_element')]")
    i_lista_precio = "8251"

    # Columnas info
    columna_fecha = "//div[text()= 'Fecha']"
    columna_observaciones = "//div[text()= 'Observaciones']"

    # Campos reporte stock
    campo_lista = "//input[contains(@id, 'variable_4_element')]"
    i_almacen = "4200"

    # Venta contado
    campo_cliente = "//input[contains(@id, 'cuenta_element')]"
    i_cliente = "5233"

    campo_lista_vco = "//input[contains(@id, 'lista_element')]"
    campo_articulo = "//input[contains(@id, 'articulo_element')]"

    campo_cantidad = "//input[contains(@id, 'cantidad_element')]"
    i_cantidad = "1"

    # Busqueda doc emitido
    busqueda_odocemitido = (f"(//span[text()= '{i_observaciones1}']"
                            f"//ancestor::div[contains(@class, 'tabulator-cell')])[1]")
    busqueda_odocemitido2 = (f"(//span[text()= '{i_observaciones2}']"
                             f"//ancestor::div[contains(@class, 'tabulator-cell')])[1]")

    # Calculo del documento
    btn_info_art = "//div[contains(@id, 'details_element')]"

    # Doc emitidos
    numero_doc = "(//span[contains(@class, 'ui-window-title')])[2]"
    campo_tipodoc = "//input[contains(@id, 'variable_1_element')]"
    campo_serie = "//input[contains(@id, 'variable_2_element')]"
    campo_numero_doc = "//input[contains(@id, 'variable_3_element')]"

    # ********************************************Variables VCO****************************************************

    # Valores y datos a utilizar en documentos
    lista_precio = "7"
    i_observaciones_vco1 = "Venta de Contado item facturado por Packing"
    i_observaciones_vco2 = "Venta Contado por unidad"
    i_observaciones_vco3 = "Venta Contado item sin stock"
    i_observaciones_vco4 = "Venta Contado Linea de Negocio no permitida"
    i_observaciones_vco5 = "Venta Contado 20 items"
    i_observaciones_vco6 = "Venta Contado Descuento 1 Renglón"
    i_observaciones_vco7 = "Venta Contado Descuento 2 Renglón"
    i_observaciones_vco8 = "Venta Contado Descuento 1 y 2 Renglón"
    i_observaciones_vco9 = "Venta Contado Descuento Global"
    i_observaciones_vco10 = "Venta Contado Descuento Global, 1 y 2 Renglón"
    i_observaciones_vco11 = "Venta Contado Recargo Global"
    i_observaciones_vco12 = "Venta Contado Descuento y Recargo Global, descuento 1 y 2 Renglón"
    i_observaciones_vco13 = "Venta Contado Combo por componente"
    i_observaciones_vco14 = "Venta Contado Combo + articulo"
    i_observaciones_vco15 = "Venta Contado 2 Combos por componentes"
    i_observaciones_vco16 = "Venta Contado Generar Nuevo Documento"
    i_observaciones_vco17 = "Venta Contado Generar Nuevo Documento con 4 documentos emitidos"
    i_observaciones_vco18 = "Venta de contado Generar nuevo documento con decuento global"
    i_observaciones_vco19 = "Venta de Contado Comportamiento de items"
    i_observaciones_vco20 = "Venta de contado que solicite Aprobacion de Documento ERRONEA"
    i_observaciones_vco25 = "Venta de contado Proceso de anulación"
    descuento_1renglon = "10"
    descuento_2renglon = "15"
    descuento_global = "5"
    recargo = "17"
    cantidad_art1 = "1"
    cantidad_art2 = "2"
    cantidad_art3 = "3"
    cantidad_art4 = "4"
    cantidad_art5 = "5"
    art_uni_negocio = "FA09037"
    codigo_art1_vco = "FA01001"
    codigo_art2_vco = "FA01005"
    codigo_art3_vco = "FA01009"
    codigo_art4_vco = "FA03007"
    codigo_art5_vco = "FA03019"  # Articulo con Lotes
    codigo_art6_vco = "FA03022"
    codigo_art7_vco = "FA09015"
    codigo_art8_vco = "FA09029"
    codigo_art9_vco = "FA09030"
    codigo_art10_vco = "FA09053"
    codigo_art11_vco = "FA02039"
    codigo_art12_vco = "FA002010"
    codigo_art13_vco = "FA003424"
    codigo_art14_vco = "FA007530"
    codigo_art15_vco = "FA013083"
    codigo_art16_vco = "40042686"
    codigo_art17_vco = "40041615"
    codigo_art18_vco = "40041602"
    codigo_art19_vco = "40041954"
    codigo_art20_vco = "40042126"
    codigo_art21_vco = "FA01004"
    codigo_art22_vco = "FA01003"
    t_rep_doc = "documentos no tocar"

    # XPATH de documentos de venta de contado
    menu_lista_pre = "//*[@id='_tablas_lstpre']"
    menu_precios = "//*[@id='abmprecios']"
    campo_codlp = "(//input[contains(@id, 'control_element')])[2]"
    cuenta1 = "0010051428"
    descuento_venta = "//input[contains(@id, 'dto1_element')]"
    atributo_descuento = "//span[text()= 'Descuento']//parent::div//preceding-sibling::div//input[@type= 'checkbox']"
    campo_descuento_1renglon = "//input[contains(@id, 'dto1_element')]"
    campo_descuento_2renglon = "//input[contains(@id, 'dto2_element')]"
    campo_descuento = "//input[contains(@id, 'dto_element')]"
    click_um = "(//input[contains(@id, '_UMEquiv_element')])"
    menu_tipo_doc = "//*[@id='_tablas_tdoc']"
    sub_menu_tipo_doc = "//*[@id='tiposdocumento']"
    buscar_tipodoc = "//div[contains(@id, 'search_element')]"
    campo_busqueda_vco = "//input[contains(@id, 'txtBusqueda_element')]"
    articulo_un_neg = "(//span[text()= 'FA09037'])[1]"
    articulo_un_neg2 = "//span[text()= 'FA09037']"

    recargo_global12 = "//span[text()= '34.75']"
    importevco12 = "(//span[text()= '281.28'])[4]"

    campo_recargo = "//input[contains(@id, 'recargo_element')]"
    btn_guarda_crear = "//div[contains(@id, 'saveadd_element')]"
    reporte_documentos = "//span[contains(text(),'DOCUMENTOS NO TOCAR')]"

    # solo lleva _element en el xpath de CambioFrame porque el resto del xpath cambia cada que se refresca
    cambio_frame = "//iframe[contains(@id,'_element')]"
    columna_combo = "(//th[contains(text(), 'cantidadCombo')])[1]"
    columna_devolucion = "(//th[contains(text(), 'devuelve')])[1]"
    columna_centro = "(//th[contains(text(), 'centrocosto')])[1]"
    columna_usuario = "(//th[contains(text(), 'usuario')])[1]"
    columna_descuento = "(//th[contains(text(), 'totdto')])[1]"
    columna_recargo = "(//th[contains(text(), 'recargo')])[1]"
    columna_precioventa = "(//th[contains(text(), 'precvent')])[1]"
    columna_impofpag = "(//th[contains(text(), 'impofpag')])[1]"

    campo_checkbox1 = "(//input[@type= 'checkbox'])[1]"
    campo_checkbox2 = "(//input[@type= 'checkbox'])[2]"
    campo_checkbox3 = "(//input[@type= 'checkbox'])[3]"
    campo_checkbox4 = "(//input[@type= 'checkbox'])[4]"
    campo_checkbox5 = "(//input[@type= 'checkbox'])[5]"
    i_observaciones4 = str(later4)

    # XPATH PARA VENTA DE CONTADO 19
    columna_articulo = "//div[text()= 'Artículo']"
    columna_descripcion = "//div[text()= 'Descripción']"
    columna_cantidad = "//div[text()= 'Cantidad']"
    columna_unidades = "//div[text()= 'Unidades']"
    columna_importe = "//div[text()= 'Importe']"
    columna_total = "(//div[text()= 'Total'])[2]"
    columna_total2 = "(//div[text()= 'Total'])[4]"

    tipo_doc_pre_con = "PR01"
    documento_preventa_contado = "(//span[text() = 'PR01'])[1]"
    btn_aprobaciones = "//button[contains(@id, 'aprobaciones_tabitem')]"
    btn_aprobaciones_click = "//input[contains(@id, '_necesitaaprobacion_checkbox')]"

    totdto_vco18 = [("FA09053", -22.90), ("FA02039", -23.10), ("FA002010", -22.85)]
    anulado_vco26 = [("FA01001", 1), ("FA013083", 1), ("FAP02630", 1)]

    btn_versiones = "//div[text()='versiones']"  # *****WBC28******
    identificador_wc28 = "//input[@name='_ID']"  # *******************WBC28*******************
    descripcion__wc28 = "//input[@name='_Description']"  # *******************WBC28*******************
    id_version_clickonce = "//input[@name='_VersionIdent']"  # *******************WBC28*******************
    id_version_powerstreet = "//input[@name='_PWSTVersionID']"  # *******************WBC28*******************
    id_version_mobile = "//input[@name='_MobileVersion']"  # *******************WBC28*******************
    id_version_mobile_vm = "//input[@name='_MobileRuntimeVersion']"  # *******************WBC28*******************
    tipo_version = "//select[@name='_VersionType']"  # *******************WBC28*******************
    activa = "//input[@name='_Enabled']"
    elementos = "//tr[@class='emDataRow'][last()]"  # *******************WBC28*******************
    versiones = "//table[@class='ui-widget ui-widget-content dataTable']"
    buscar_v6 = "6.0.0"
    buscar_v5 = "5.0.0"
    buscar_v4 = "4.0.0"
    btn_grupos = "//div[text()='grupos']"
    grupo_v6 = "pc4"
    grupo_v5 = "pc2"
    grupo_v4 = "pex"
    pc2 = "//td[text()='pc2']"
    pex = "//td[text()='pex']"
    pc4 = "//td[text()='pc4']"
    serv_version = "//a[contains(text(), 'Servidor y versión')]"
    menu_desplegable_serv_version = "//select[@name='_ClickOnceVersion']"
    actualizar_base_version = "//span[@class='ui-icon ui-icon-check']"
    aceptar_bd = "//button[text()='Si']"

    # ***************************************** Variables VCR *******************************************************

    # Valores y datos a utilizar en documentos
    moneda = "//span[text() = '1']"

    # XPATH de documentos de venta de credito
    menu_cancelaciones = "(//span[text()= 'Cancelaciones'])[1]"
    campo_cuenta_cancelacion = "//input[contains(@id, 'cuentasC_element')]"
    cuenta1_vcr = "0010049228"
    ayuda_moneda = "//input[contains(@id, 'monedas_element')]//following::span[contains(@class, 'help')]"
    cancelaciones = ("//div[contains(@id, 'listviewDerecha_grid')]//descendant::div[contains(@class, 'tabulator-row "
                     "tabulator-selectable tabulator-row')]")
    doc_recibo_pago = "//span[text()= 'Recibo de Pago    (PM08)']"

    # ************************************** Variables Web Client *************************************************
    # Datos al ingresar sesión

    usuariowc = "awsautest"
    contrasena_error = "Pwst12345*"
    contrasena_ok = "Pwst12345**"

    # usuarios assist
    usuario_assist = "xcsautest1"
    usuario_assist_modif = "xcsautest"
    nombre_usuario = "Testing Auto1"
    nombre_cambio = "Test Auto2 Editado"
    nombre_cambio2 = "Usuario Predeterminado"
    nombre_cambiosop = "awsTesAut1"
    nombre_cambiosop2 = "Pruebas Automatización"

    campo_perfil_nada = "(//option[@value=''])[2]"
    btn_aceptar_error = "//button[text()= 'aceptar']"
    btn_guardar = "//button[text()='guardar']"
    btn_confirmar = "//button[text()='Si']"
    btn_cerrar_pantalla_wc = "//button[@title= 'Close']"
    campo_newpass = "//input[@name= 'newpass']"
    campo_validarpass = "//input[@name= 'retypepass']"
    btn_confirmar_pass = "//input[@value= 'cambiar contraseña']"
    btn_usuarios = "//div[text()='usuarios']"
    campo_idusu = "//input[@name= '_NombreLogin']"
    campo_nomusu = "//input[@name= '_NombreUsuario']"
    campo_perfil = "//select[@name= '_PerfilSeguridad']"
    campo_buscar = "(//input[contains(@class, 'filterText')])[1]"
    check_contra = "//input[@name= '_ChangePasswordAtNextLogon']"
    check_inactivo = "//input[@name= '_Inactivo']"
    campo_grupoxab = "//option[@value= 'xab']"
    campo_perfilaut1 = "//option[@value= 'AUT1']"
    btn_nuevowc = "//button[@id='emAddItem']"
    campo_grupo = "//select[@name = '_NombreGrupo']"
    campo_opcion_grupo = "//option[@value='te3']"
    check_inactivo_activo = "//input[@name='_Inactivo']"

    # XPATH Client assist usuarios
    campo_grupoxcs = "//option[@value= 'xcs']"
    buscar_usu_assist = "//td[text()='xcsautest1']"
    txt_buscar_assist = "//td[text()='xcsautest']"
    campo_perfil_assist = "//option[@value= 'BACKOFFICE']"
    btn_habilitarwc = "(//td[@title= 'deshabilitado'])[3]"
    btn_habilitar_cuenta = "(//td[@title= 'deshabilitado'])[4]"
    btn_cerrar_sesion = "(//a[@class='logoffLink'])[1]"
    btn_cerrar_sesion2 = "(//a[@class='logoffLink'])[2]"  # anel
    btn_cerrar_sesion3 = "(//a[@class='logoffLink'])[3]"  # anel
    btn_cerrar_sesion4 = "(//a[@class='logoffLink'])[4]"  # anel
    btn_rest_contra = "//a[@title='resetear contraseña']"
    campo_newpass2 = "//input[@id= '_NewPass1']"
    campo_validarpass2 = "//input[@id= '_NewPass2']"

    # **************************** Flujos ****************************************************
    checkbox_art_activo = "(//input[contains(@id, 'activo_checkbox')])[1]"
