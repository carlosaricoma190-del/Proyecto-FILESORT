import wx #Libreria para crear la interfaz gráfica
import os #Permite trabajar con archivos y directorios del sistema
import shutil #shutil mueve los archivos a sus respectivas directorios
import datetime #datetime se usa para mostrar la fecha de modificacion de los archivos
import wx.adv #wx.adv se usa para mostrar la pantalla de bienvenida (splash screen)

RUTA_BASE = os.path.dirname(os.path.abspath(__file__)) #Esto obtiene la ruta del archivo actual y la guarda en la variable RUTA_BASE

#La clase MiPanel crea el panel principal de la aplicación y contiene el árbol de directorios, la lista de archivos y la barra de búsqueda.
class MiPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        #lista donde se mostrarán los directorios y archivos
        self.arbol = wx.TreeCtrl(self)
        #Iconos para los directorios y archivos
        self.imagenes = wx.ImageList(16, 16)
        self.icono_carpeta = self.imagenes.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16, 16)))
        self.icono_archivo = self.imagenes.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16, 16)))

        #Asigna la lista de iconos al árbol
        self.arbol.AssignImageList(self.imagenes)

        #Lista donde se muestra informacion de los archivos
        self.lista = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.lista.InsertColumn(0, "Nombre", width=200)
        self.lista.InsertColumn(1, "Tipo", width=100)
        self.lista.InsertColumn(2, "Tamaño", width=100)
        self.lista.InsertColumn(3, "Fecha de modificación", width=150)

        #Barra de busqueda
        self.barra_busqueda = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.boton_buscar = wx.Button(self, label="Buscar")

        #sizer para la barra de busqueda y el arbol esten organizados
        sizer_busqueda = wx.BoxSizer(wx.VERTICAL)
        sizer_busqueda.Add(self.barra_busqueda, proportion=0, 
                flag=wx.EXPAND | wx.ALL, border=5)
        sizer_busqueda.Add(self.boton_buscar, proportion=0,
                flag=wx.EXPAND | wx.ALL, border=5)
        sizer_busqueda.Add(self.arbol, proportion=1,
                flag=wx.EXPAND | wx.ALL, border=5)
        
        #Sizer principal de la ventana
        #A la izquierda esta la busqueda y a la derecha la lista con la informacion de los archivos
        sizer_menu = wx.BoxSizer(wx.HORIZONTAL)
        sizer_menu.Add(sizer_busqueda, proportion=1,
                 flag=wx.EXPAND | wx.ALL, border=10)
        sizer_menu.Add(self.lista, proportion =1,
                flag=wx.EXPAND | wx.ALL, border=10)

        #Asigna el sizer principal al panel
        self.SetSizer(sizer_menu)

#Esta clase esta encargada de organizar automaticamente
class OrganizarArchivosDialog(wx.Frame):
    def __init__(self, parent, ruta_carpeta):
        super().__init__(parent, title = "Organizar archivos", size=(800, 400))
        #Referencia al frame principal
        self.parent = parent
        #Ruta de la carpeta seleccionada
        self.ruta_carpeta = ruta_carpeta
        #Panel principal de la ventana
        panel = wx.Panel(self)
        #Texto informativo antes de organizar archivos
        texto = wx.StaticText(panel, label="Seleccione una opción para organizar los archivos:")
        #Advertencia para el usuario
        texto_2 = wx.StaticText(panel, label="ADVERTENCIA: Esta acción moverá los archivos a sus respectivas carpetas y no se podrá deshacer.")
        #Opcion para organizar por tipo de archivo
        opcion_tipo_archivo = wx.RadioButton(panel, label="Organizar por tipo de archivo", style=wx.RB_GROUP)
        #Boton que inicia la organización
        boton_organizar = wx.Button(panel, label="Organizar ahora")
        #Evento del boton
        boton_organizar.Bind(wx.EVT_BUTTON, self.organizar_archivos)

        #Sizer de la ventana "Organizar archivos"
        sizer= wx.BoxSizer(wx.VERTICAL)
        sizer.Add(texto, proportion=0, flag=wx.ALL, border=10)
        sizer.Add(texto_2, proportion=0, flag=wx.ALL, border=10)
        sizer.Add(opcion_tipo_archivo, proportion=0, flag=wx.ALL, border=10)
        sizer.Add(boton_organizar, proportion=0, flag=wx.ALL, border=10)

        panel.SetSizer(sizer)
    
#Evento del botón "Organizar ahora"
    def organizar_archivos(self, event):
        #Carpetas que se crearan con los archivos correspondientes
        categorias = {
            "Documentos": [".docx"],
            "Hojas de cálculo": [".xlsx"],
            "Presentaciones": [".pptx"],
            "PDFs": [".pdf"],
            "Archivos de texto": [".txt"],
            "Código fuente": [".py", ".java", ".cpp", ".html", ".css", ".js"],
            "Imagenes": [".jpg", ".jpeg",".png", ".gif"],
            "Videos": [".mp4", ".avi", ".mkv"],
            "Audios": [".mp3", ".wav", ".aac"],
            "Otros": []
        }
        #Recorre todos los archivos del directorio seleccionado
        for archivo in os.listdir(self.ruta_carpeta):
            ruta_archivo = os.path.join(self.ruta_carpeta, archivo)
            #Omite las carpetas
            if os.path.isdir(ruta_archivo):
                continue
            #Obtiene la extension del archivo
            extension = os.path.splitext(archivo)
            extension = extension[1].lower()  # Obtener la extensión en minúsculas
            #carpeta por defecto (para archivos por ejemplo .bin)
            carpeta_destino = "Otros"
            #Busca la categoría correspondiente
            for categoria, extensiones in categorias.items():
                if extension in extensiones:
                    carpeta_destino = categoria
                    break
            #Crea la carpeta si aún no existe
            ruta_destino = os.path.join(self.ruta_carpeta, carpeta_destino)
            os.makedirs(ruta_destino, exist_ok=True)
            #Mueve el archivo a la carpeta correspondiente
            shutil.move(ruta_archivo, os.path.join(ruta_destino, archivo))
        #Avisa que la operación fue un exito
        wx.MessageBox("Archivos organizados correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        self.parent.actualizar_arbol() #Llama a la funcion actualizar_arbol() del frame principal para actualizarlo
        self.Close() #Cierra la ventana "Organizar archivos" despues de organizar los archivos

class ManualDeApp(wx.adv.WizardPageSimple):
    def __init__(self, parent, title, contenido):
        super().__init__(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        titulo = wx.StaticText(self, label=title)
        titulo.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        sizer.Add(titulo, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        sizer.Add(wx.StaticLine(self), 0, wx.EXPAND | wx.ALL, 5)

        texto = wx.StaticText(self, label=contenido)
        texto.Wrap(500)
        sizer.Add(texto, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(sizer)

#clase para mostrar un screen en la pantalla antes de abrir la ventana principal de la aplicacion
class MiSplash(wx.adv.SplashScreen):
    def __init__(self):
        #Obtiene la ruta donde se encuentra la imagen del logo
        ruta_logo = os.path.join(RUTA_BASE, "logo.png")
        #Verifica que el archivo exista
        os.path.exists(ruta_logo)
        #Carga la imagen del logo
        imagen = wx.Image(ruta_logo)
        #Cambia el tamaño de la imagen para que sea mas ajustable
        imagen = imagen.Scale(100, 100, wx.IMAGE_QUALITY_HIGH)
        #Convierte la imagen del logo en un Bitmap para mostrarla
        bitmap = wx.Bitmap(os.path.join(RUTA_BASE, "logo.png"))
        #COnfiguracion para que sea ajuste en el centro de la pantalla
        splashStyle = wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT

        #Crea la ventana Splash Screen
        super().__init__(bitmap, splashStyle, 3000, None, -1)
        #Cuando el splash se cierre, se ejecutara la función cerrar()
        self.Bind(wx.EVT_CLOSE, self.cerrar)
        #Centra la ventana en la pantalla
        self.Centre()
        #Muestra el SplashScreen
        self.Show()
    #Función que se ejecuta cuando termina el SplashScreen
    def cerrar(self, event):
        #Crea la ventana principal de la aplicación
        frame = MiFrame()
        #Muestra la ventana principal
        frame.Show()
        #Permite que le evento del screen se cierre continue con MiFrame
        event.Skip()        

#clase principal de la ventana aplicacion
class MiFrame(wx.Frame):
    def __init__(self):
        #crea la ventana principal con su titulo y tamaño
        super().__init__(parent=None, title="FileSort", size=(900, 600))
        self.panel= MiPanel(self) #agrega el panel principal a la ventana
        icono = (wx.Icon(path, wx.BITMAP_TYPE_ICO) #carga el icono de la aplicacion si existe
                 if (path := next((p for p in (os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icono.ico'), os.path.join(os.getcwd(), 'icono.ico'))
                                   if os.path.exists(p)), None)) else wx.NullIcon())
        self.SetIcon(icono)
        
#==========================
        #Barra de busqueda
        self.panel.boton_buscar.Bind(wx.EVT_BUTTON, self.buscar_archivo) #se busca presionando el boton
        self.panel.barra_busqueda.Bind(wx.EVT_TEXT_ENTER, self.buscar_archivo) # se busca presionando el boton ENTER

#============================
        #Barra de menú  
        barra_menu = wx.MenuBar()
        
        #Barra de menú Archivo
        menu_archivo = wx.Menu()
        opcion_abrir_carpeta = menu_archivo.Append(wx.ID_ANY, "Abrir carpeta")
        barra_menu.Append(menu_archivo, "Archivo")
        

        #Barra de menú Ver
        menu_ver = wx.Menu()
        opcion_ordenar_nombre = menu_ver.Append(wx.ID_ANY, "Ordenar por nombre")
        opcion_ordenar_fecha = menu_ver.Append(wx.ID_ANY, "Ordenar por fecha")
        opcion_ordenar_tamaño_mayor = menu_ver.Append(wx.ID_ANY, "Ordenar por tamaño (mayor a menor)")
        opcion_ordenar_tamaño_menor = menu_ver.Append(wx.ID_ANY, "Ordenar por tamaño (menor a mayor)")
        barra_menu.Append(menu_ver, "Ver")

        #Barra de menu Herramientas
        menu_herramientas = wx.Menu()
        opcion_organizar_archivos = menu_herramientas.Append(wx.ID_ANY, "Organizar archivos")
        opcion_estadisticas = menu_herramientas.Append(wx.ID_ANY, "Estadísticas de carpeta")
        opcion_tema_oscuro = menu_herramientas.Append(wx.ID_ANY, "Tema oscuro")
        opcion_tema_claro = menu_herramientas.Append(wx.ID_ANY, "Tema claro")
        barra_menu.Append(menu_herramientas, "Herramientas")
        
        #Barra de menu Ayuda
        menu_ayuda = wx.Menu()
        opcion_manual_de_app = menu_ayuda.Append(wx.ID_ANY, "Manual de la app")
        opcion_acerca_de = menu_ayuda.Append(wx.ID_ANY,"Acerca de")
        barra_menu.Append(menu_ayuda, "Ayuda")

        #Asignar la barra de menú a la ventana
        self.SetMenuBar(barra_menu)

#=====================
        #Eventos del menú

        #menu archivo
        self.Bind(wx.EVT_MENU, self.abrir_carpeta, opcion_abrir_carpeta)
        #menu ver
        self.Bind(wx.EVT_MENU, self.ordenar_por_nombre, opcion_ordenar_nombre)
        self.Bind(wx.EVT_MENU, self.ordenar_por_fecha, opcion_ordenar_fecha)
        self.Bind(wx.EVT_MENU, self.ordenar_por_mayor_a_menor, opcion_ordenar_tamaño_mayor)
        self.Bind(wx.EVT_MENU, self.ordenar_por_menor_a_mayor, opcion_ordenar_tamaño_menor)
        #menu herramientas
        self.Bind(wx.EVT_MENU, self.abrir_ventana_organizar, opcion_organizar_archivos)
        self.Bind(wx.EVT_MENU, self.tema_oscuro, opcion_tema_oscuro)
        self.Bind(wx.EVT_MENU, self.tema_claro, opcion_tema_claro)
        self.Bind(wx.EVT_MENU, self.mostrar_estadisticas, opcion_estadisticas)
        #menu ayuda
        self.Bind(wx.EVT_MENU, self.mostrar_manual_de_app, opcion_manual_de_app)
        self.Bind(wx.EVT_MENU, self.acerca_de, opcion_acerca_de)

#========================
#eventos del arbol
        
        #Detecta las columnas y muestra su contenido
        self.panel.arbol.Bind(wx.EVT_TREE_SEL_CHANGED, self.mostrar_contenido_carpeta)
        
        #Hace doble clic en el archivo para abrirlo
        self.panel.arbol.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.abrir_archivo)

        #muestra y centra la ventana
        self.Show()
        self.Center()

#============================
    #Funciones del menu
    
    #Funcion para cambiar el tema de la app a tema oscuro
    def tema_oscuro(self, event):
        self.panel.SetBackgroundColour(wx.Colour(30, 30, 30))
        self.panel.arbol.SetBackgroundColour(wx.Colour(40, 40, 40))
        self.panel.arbol.SetForegroundColour(wx.WHITE)
        self.panel.lista.SetBackgroundColour(wx.Colour(40, 40, 40))
        self.panel.lista.SetForegroundColour(wx.WHITE)
        
        self.Refresh() #actualiza la interfaz

    #funcion para cambiar el tema de la app a tema claro
    def tema_claro(self, event):
        self.panel.SetBackgroundColour(wx.WHITE)
        self.panel.arbol.SetBackgroundColour(wx.WHITE)
        self.panel.arbol.SetForegroundColour(wx.BLACK)
        self.panel.lista.SetBackgroundColour(wx.WHITE)
        self.panel.lista.SetForegroundColour(wx.BLACK)
        
        self.Refresh() #actualiza la interfaz

    #Funcion para mostrar las estadisticas del directorio
    def mostrar_estadisticas(self, event):
        if not hasattr(self, "ruta_carpeta"): #verifica que exista un directorio abierto
            wx.MessageBox("Primero debes abrir una carpeta.", "FileSort", wx.OK | wx.ICON_WARNING)
            return

        #Contadores de los archivos
        total_archivos = 0
        total_carpetas = 0
        pptx_archivos = 0
        docx_archivos = 0
        PDFs = 0
        txt_archivos = 0
        xlsx_archivos = 0
        codigo_archivos = 0
        imagenes = 0
        videos = 0
        otros_archivos = 0
        tamaño_total = 0 

        #recorre todo el directorio y sus subcarpetas
        for ruta_actual, directorios, archivos in os.walk(self.ruta_carpeta):
            total_carpetas += len(directorios)
            for archivo in archivos:
                total_archivos += 1
                ruta_archivo = os.path.join(ruta_actual, archivo)
                tamaño_total += os.path.getsize(ruta_archivo)
                extension = os.path.splitext(archivo)[1].lower()

                #clasifica los arcivos por extension
                if extension in [".jpg", ".jpeg", ".png", ".gif"]:
                    imagenes += 1
                elif extension == ".pdf":
                    PDFs+= 1
                elif extension == ".docx":
                        docx_archivos += 1
                elif extension == ".txt":
                        txt_archivos += 1
                elif extension == ".xlsx":
                        xlsx_archivos += 1
                elif extension == ".html" or extension == ".css" or extension == ".js" or extension == ".py" or extension == ".java" or extension == ".cpp": 
                        codigo_archivos += 1
                elif extension == ".pptx":
                        pptx_archivos += 1
                elif extension == ".bin" or extension == ".exe" or extension == ".dll":
                        otros_archivos += 1 
                elif extension in [".mp4", ".avi", ".mkv"]:
                    videos += 1
            tamaño_MB = round(tamaño_total / (1024 * 1024), 2) #convierte el tamaño total a MB
            mensaje = ( #Contruye mensaje que se le mostrara al usuario 
                f"Archivos: {total_archivos}\n"
                f"Carpetas: {total_carpetas}\n"
                f"Archivos de código: {codigo_archivos}\n"
                f"Archivos de texto: {txt_archivos}\n"
                f"Archivos de Excel: {xlsx_archivos}\n"
                f"Archivos de PowerPoint: {pptx_archivos}\n"
                f"Documentos: {docx_archivos}\n"
                f"PDFs: {PDFs}\n"
                f"Imágenes: {imagenes}\n"
                f"Videos: {videos}\n"
                f"Otros archivos: {otros_archivos}\n"
                f"Tamaño total: {tamaño_MB} MB\n"
            )

        #muestra las estadisticas
        wx.MessageBox(mensaje, "Estadísticas de carpeta", wx.OK | wx.ICON_INFORMATION)
            
    #Ventana para organizar archivos
    def abrir_ventana_organizar(self, event):
        if not hasattr(self, "ruta_carpeta"): #verifica que exista un directorio abierto
           wx.MessageBox("Primero debes abrir una carpeta.", "FileSort", wx.OK | wx.ICON_WARNING)
           return

        #crea y muestra la ventana
        self.ventana_organizar = OrganizarArchivosDialog(self, self.ruta_carpeta)
        self.ventana_organizar.Show()

    #funcion de la ventana ayuda, el manual
    def mostrar_manual_de_app(self, event):
        #crea la ventana con el título del manual
        wizard = wx.adv.Wizard(self, -1, "Manual de FileSort")
        wizard.CenterOnScreen()

        #lista de paginas que contendra el manual (título y contenido)
        paginas = [
            ("Introducción", "FileSort es una aplicación para organizar y explorar archivos en tu computadora. Este manual te guiará a través de todas las características disponibles."),
            ("Abrir Carpeta", "1. Ve al menú Archivo\n2. Selecciona 'Abrir carpeta'\n3. Elige la carpeta que deseas explorar\n\nLa carpeta aparecerá en el árbol de directorios y podrás ver su contenido en la lista."),
            ("Buscar Archivos", "1. Escribe el nombre del archivo en la barra de búsqueda\n2. Presiona Enter o haz clic en el botón Buscar\n\nLos archivos que coincidan con tu búsqueda aparecerán en la lista."),
            ("Ordenar Archivos", "Usa el menú Ver para ordenar los archivos por:\n- Nombre: orden alfabético\n- Fecha: por fecha de modificación\n- Tamaño (mayor a menor): archivos más grandes primero\n- Tamaño (menor a mayor): archivos más pequeños primero"),
            ("Organizar Archivos", "1. Ve al menú Herramientas\n2. Selecciona 'Organizar archivos'\n3. Elige la opción deseada\n\nLos archivos se organizarán automáticamente en carpetas según su tipo."),
            ("Estadísticas", "1. Ve al menú Herramientas\n2. Selecciona 'Estadísticas de carpeta'\n\nVerás información sobre el total de archivos, carpetas, tipos de archivos y tamaño total."),
            ("Temas", "En el menú Herramientas puedes cambiar entre:\n- Tema oscuro: interfaz oscura para trabajar de noche\n- Tema claro: interfaz clara y tradicional"),
            ("Fin", "¡Felicidades! Has completado el manual de FileSort.\n\nPara más información, consulta el menú Ayuda > Acerca de.")
        ]

        lista_paginas = [] #lista donde se almacenan las paginas creadas
        
        for titulo, contenido in paginas: #crea cada pagina del manual y la agrega a la lista
            pagina = ManualDeApp(wizard, titulo, contenido)
            lista_paginas.append(pagina)

        #conecta las paginas para poder avanzar y retroceder con los botones del wizard
        for i in range(len(lista_paginas) - 1):
            wx.adv.WizardPageSimple.Chain(lista_paginas[i], lista_paginas[i + 1])

        wizard.GetPageAreaSizer().Add(lista_paginas[0]) #Agrega la primera pagina
        wizard.RunWizard(lista_paginas[0]) #inicia el recorrido del manual desde la primera pagina
        wizard.Destroy() cierra y libera la ventana cuando finalice
    
    #Esta funcion carga el arbol con los directorios y archivos de la ruta seleccionada
    def cargar_arbol(self, ruta, nodo_padre):
        elementos = os.listdir(ruta) #obtiene todos los elementos del directorio
        for elemento in elementos:
            ruta_completa = os.path.join(ruta, elemento)
            if os.path.isdir(ruta_completa):
                nodo = self.panel.arbol.AppendItem(nodo_padre, elemento, image = self.panel.icono_carpeta) #agrega carpeta al arbol
                self.panel.arbol.SetItemData(nodo, ruta_completa)
                self.cargar_arbol(ruta_completa, nodo) #muestra subcarpetas
            else:
                nodo = self.panel.arbol.AppendItem(nodo_padre, elemento, image = self.panel.icono_archivo)
                self.panel.arbol.SetItemData(nodo, ruta_completa)

    #funcion para buscar archivos en el directorio seleccionado
    def buscar_archivo(self, event):
        texto = self.panel.barra_busqueda.GetValue().lower()
        if texto == "":
            return
        self.panel.lista.DeleteAllItems()
        for ruta_actual, carpetas, archivos in os.walk(self.ruta_carpeta): #busca en todas las subcarpetas
            for archivo in archivos:
                if texto in archivo.lower():
                    indice = self.panel.lista.InsertItem(self.panel.lista.GetItemCount(), archivo)
                    self.panel.lista.SetItem(indice, 1, os.path.splitext(archivo)[1])
    
    #Funcion para mostrar el contenido del directorio seleccionado en la lista
    def mostrar_contenido_carpeta(self, event):
        item = event.GetItem()
        ruta = self.panel.arbol.GetItemData(item)
        
        if not os.path.isdir(ruta):
            return
        self.panel.lista.DeleteAllItems() #limpia la lista

        for archivo in os.listdir(ruta):
            ruta_archivo = os.path.join(ruta, archivo)

            if os.path.isdir(ruta_archivo):
                tipo = "Carpeta"
                tamaño = "-"
            else:
                tipo = os.path.splitext(archivo)[1]
                tamaño = str(os.path.getsize(ruta_archivo) // 1024) + "KB" 
                #convierte el tamaño a KB o MB
                if os.path.getsize(ruta_archivo) < 1024 * 1024 :
                    tamaño = str(os.path.getsize(ruta_archivo) // 1024) + "KB"
                else:
                    tamaño = str(os.path.getsize(ruta_archivo) // (1024 * 1024)) + "MB"
            #fecha de modificacion
            fecha = datetime.datetime.fromtimestamp(
                    os.path.getmtime(ruta_archivo)).strftime("%d/%m/%Y %H:%M")
            indice = self.panel.lista.InsertItem(self.panel.lista.GetItemCount(), archivo) #agrega el archivo a la lista
            self.panel.lista.SetItem(indice, 1, tipo)
            self.panel.lista.SetItem(indice, 2, tamaño)
            self.panel.lista.SetItem(indice, 3, fecha)

    def abrir_archivo(self, event):
        item = event.GetItem()
        ruta = self.panel.arbol.GetItemData(item)
        if os.path.isfile(ruta):
            os.startfile(ruta)
    
    #Función para abrir el directorio y mostrar los archivos en la lista
    def abrir_carpeta(self,event):
        #se abre un cuadro de dialogo para elegir un directorio
        dialogo = wx.DirDialog(self, "Selecciona un directorio")
        if dialogo.ShowModal() == wx.ID_OK:
            self.ruta_carpeta = dialogo.GetPath() #guarda la ruta seleccionada
            self.panel.arbol.DeleteAllItems()  #limpiar el árbol antes de agregar nuevos elementos
            raiz = self.panel.arbol.AddRoot(os.path.basename(self.ruta_carpeta)) #crea el nodo raiz con el nombre de la carpeta
            self.panel.arbol.SetItemData(raiz, self.ruta_carpeta) #guarda la ruta en el nodo raiz
            self.cargar_arbol(self.ruta_carpeta, raiz) #carga todos los directorios y archivos
            self.panel.arbol.Expand(raiz)  #expandir el nodo raíz para mostrar los archivos

        dialogo.Destroy() #Destruye el dialogo despues de seleccionar la carpeta

    #Funcion para actualizar arbol y lista despues de organizar archivos
    def actualizar_arbol(self):
        self.panel.arbol.DeleteAllItems()  #limpiar el árbol antes de agregar nuevos elementos
        raiz = self.panel.arbol.AddRoot(os.path.basename(self.ruta_carpeta)) #vuelve a crear el nodo raiz
        self.panel.arbol.SetItemData(raiz, self.ruta_carpeta) #asigna la ruta al nodo raiz
        self.cargar_arbol(self.ruta_carpeta, raiz) #recarga todas las carpetas y archivos
        self.panel.arbol.Expand(raiz)  #expandir el nodo raíz para mostrar los archivos

    #Funcion para ordenar por nombre
    def ordenar_por_nombre(self, event):
        if not hasattr(self, "ruta_actual"): #verifica que exista el directorio
           return
        self.panel.lista.DeleteAllItems() #limpia la listra
        archivos = os.listdir(self.ruta_actual) #obtiene todos los elementos
        archivos.sort(key=str.lower) #ordena alfabeticamente sin importar las mayusculas
        for archivo in archivos: #recorre todos los elementos ordenados
            ruta_archivo = os.path.join(self.ruta_actual, archivo)
            if os.path.isdir(ruta_archivo):
                tipo = "Carpeta"
                tamaño = "-"
            else:
                tipo = os.path.splitext(archivo)[1]
                if os.path.getsize(ruta_archivo) < 1024 * 1024:
                    tamaño = str(os.path.getsize(ruta_archivo)//1024) + " KB"
                else:
                    tamaño = str(os.path.getsize(ruta_archivo)//(1024*1024)) + " MB"
            #fecha de modificacion
            fecha = datetime.datetime.fromtimestamp( 
                os.path.getmtime(ruta_archivo)
            ).strftime("%d/%m/%Y %H:%M")
            #inserta el archivo en la lista
            indice = self.panel.lista.InsertItem( 
                self.panel.lista.GetItemCount(),
                archivo
            )

            self.panel.lista.SetItem(indice, 1, tipo)
            self.panel.lista.SetItem(indice, 2, tamaño)
            self.panel.lista.SetItem(indice, 3, fecha)

    #Funcion para ordenar por fecha
    def ordenar_por_fecha(self, event):
        if not hasattr(self, "ruta_actual"): #verifica que exista el directorio
           return
        self.panel.lista.DeleteAllItems() #limpia la lista
        archivos = os.listdir(self.ruta_actual)
        #ordena de la fecha mas reciente a la mas antigua
        archivos.sort(
            key=lambda archivo: os.path.getmtime(
                os.path.join(self.ruta_actual, archivo)
            ), 
            reverse=True
        )
        for archivo in archivos:
            ruta_archivo = os.path.join(self.ruta_actual, archivo)
            if os.path.isdir(ruta_archivo):
                tipo = "Carpeta"
                tamaño = "-"
            else:
                tipo = os.path.splitext(archivo)[1]
                if os.path.getsize(ruta_archivo) < 1024 * 1024:
                    tamaño = str(os.path.getsize(ruta_archivo)//1024) + " KB"
                else:
                    tamaño = str(os.path.getsize(ruta_archivo)//(1024*1024)) + " MB"
            #fecha de modificacion
            fecha = datetime.datetime.fromtimestamp(
                os.path.getmtime(ruta_archivo)
            ).strftime("%d/%m/%Y %H:%M")
            #inserta el archivo en la lista
            indice = self.panel.lista.InsertItem(
                self.panel.lista.GetItemCount(),
                archivo
            )

            self.panel.lista.SetItem(indice,1,tipo)
            self.panel.lista.SetItem(indice,2,tamaño)
            self.panel.lista.SetItem(indice,3,fecha)

    #Funcion para ordenar de mayor a menor
    def ordenar_por_mayor_a_menor(self, event):
        if not hasattr(self, "ruta_actual"): #verifica que exista un directorio
           return
        self.panel.lista.DeleteAllItems() #limpia la lista
        archivos = os.listdir(self.ruta_actual)
        #ordena por tamaño mayor a menor
        archivos.sort(key=lambda archivo: os.path.getsize(
                        os.path.join(self.ruta_actual, archivo)
                    ) if os.path.isfile(os.path.join(self.ruta_actual, archivo)) else -1,
                    reverse=True
        )
        for archivo in archivos:
            ruta_archivo = os.path.join(self.ruta_actual, archivo)
            if os.path.isdir(ruta_archivo):
                tipo = "Carpeta"
                tamaño = "-"
            else:
                tipo = os.path.splitext(archivo)[1]
                if os.path.getsize(ruta_archivo) < 1024 * 1024:
                    tamaño = str(os.path.getsize(ruta_archivo)//1024) + " KB"
                else:
                    tamaño = str(os.path.getsize(ruta_archivo)//(1024*1024)) + " MB"

            fecha = datetime.datetime.fromtimestamp(
                os.path.getmtime(ruta_archivo)
            ).strftime("%d/%m/%Y %H:%M")

            indice = self.panel.lista.InsertItem(
                self.panel.lista.GetItemCount(),
                archivo
            )

            self.panel.lista.SetItem(indice, 1, tipo)
            self.panel.lista.SetItem(indice, 2, tamaño)
            self.panel.lista.SetItem(indice, 3, fecha)

    #Funcion para ordenar de menor a mayor
    def ordenar_por_menor_a_mayor(self, event):
        if not hasattr(self, "ruta_actual"): #verifica que no exista un directorio
           return
        self.panel.lista.DeleteAllItems() #limpia la lista
        archivos = os.listdir(self.ruta_actual)
        #ordena por tamaño de menor a mayor
        archivos.sort(key=lambda archivo: os.path.getsize(
                          os.path.join(self.ruta_actual, archivo)
                     ) if os.path.isfile(os.path.join(self.ruta_actual, archivo)) else -1
        )
        for archivo in archivos:
            ruta_archivo = os.path.join(self.ruta_actual, archivo)
            if os.path.isdir(ruta_archivo):
                tipo = "Carpeta"
                tamaño = "-"
            else:
                tipo = os.path.splitext(archivo)[1]
                if os.path.getsize(ruta_archivo) < 1024 * 1024:
                    tamaño = str(os.path.getsize(ruta_archivo)//1024) + " KB"
                else:
                    tamaño = str(os.path.getsize(ruta_archivo)//(1024*1024)) + " MB"
            #fecha de modificacion
            fecha = datetime.datetime.fromtimestamp(
                os.path.getmtime(ruta_archivo)
            ).strftime("%d/%m/%Y %H:%M")
            #inserta el archivo emn la lista
            indice = self.panel.lista.InsertItem(
                self.panel.lista.GetItemCount(),
                archivo
            )

            self.panel.lista.SetItem(indice, 1, tipo)
            self.panel.lista.SetItem(indice, 2, tamaño)
            self.panel.lista.SetItem(indice, 3, fecha)                 
    
        #Funcion para para crear el "Acerca de" para mostrar a los desarrolladores
    def acerca_de(self, event):
        info = wx.adv.AboutDialogInfo() #crea el cuadro de informacion
        logo = wx.Icon(os.path.join(RUTA_BASE, "logo.png")) #carga el logo de la aplicacion
        info.SetIcon(logo)

        #informacion general
        info.SetName("FILESORT")
        info.SetVersion("1.0")
        #descripcion del proyecto
        info.SetDescription(
            "Aplicación para organizar archivos por categorías,\n"
            "explorar carpetas y visualizar información de los archivos,\n"
            "Proyecto desarrollado con Python utilizando wxPython"
        )
        #copyright
        info.SetCopyright("© 2026")
        #repositorio GitHub
        info.SetWebSite("https://github.com/carlosaricoma190-del/Proyecto-FILESORT.git")
        #licencia deel proyecto
        info.SetLicence("Proyecto desarrollado con fines educativos")
        #desarrolladores 
        info.AddDeveloper("Juan Aricoma y Tomas Tarifa")

        #muestra la ventana "acerca de"
        wx.adv.AboutBox(info)

    
#pregunta si la app corre local o la importe
if __name__ == "__main__":
    app = wx.App(redirect=False) #crea la aplicacion
    splash = MiSplash() #se crea la pantalla de bienvenida en splash
    app.MainLoop() #inicia el bucle de la aplicacion para que no se cierre
