import wx
import os
import shutil #shutil mueve los archivos a sus respectivas directorios
import datetime #datetime se usa para mostrar la fecha de modificacion de los archivos

class MiPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        #lista onde se mostrarán los archivos
        self.arbol = wx.TreeCtrl(self)
        #Icono para los directorios y archivos
        self.imagenes = wx.ImageList(16, 16)
        self.icono_carpeta = self.imagenes.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16, 16)))
        self.icono_archivo = self.imagenes.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, (16, 16)))
        self.arbol.AssignImageList(self.imagenes)

        #Columas del arbol
        self.lista = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.lista.InsertColumn(0, "Nombre", width=200)
        self.lista.InsertColumn(1, "Tipo", width=100)
        self.lista.InsertColumn(2, "Tamaño", width=100)
        self.lista.InsertColumn(3, "Fecha de modificación", width=150)

        #Barra de busqueda
        self.barra_busqueda = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.boton_buscar = wx.Button(self, label="Buscar")

        #sizer para la barra de busqueda
        sizer_busqueda = wx.BoxSizer(wx.VERTICAL)
        sizer_busqueda.Add(self.barra_busqueda, proportion=0, 
                flag=wx.EXPAND | wx.ALL, border=5)
        sizer_busqueda.Add(self.boton_buscar, proportion=0,
                flag=wx.EXPAND | wx.ALL, border=5)
        sizer_busqueda.Add(self.arbol, proportion=1,
                flag=wx.EXPAND | wx.ALL, border=5)
        
        #sizer principal
        sizer_menu = wx.BoxSizer(wx.HORIZONTAL)
        sizer_menu.Add(sizer_busqueda, proportion=1,
                 flag=wx.EXPAND | wx.ALL, border=10)
        sizer_menu.Add(self.lista, proportion =1,
                flag=wx.EXPAND | wx.ALL, border=10)
        self.SetSizer(sizer_menu)

#Esta clase abre la ventana "Organizar archivos"
class OrganizarArchivosDialog(wx.Frame):
    def __init__(self, parent, ruta_carpeta):
        super().__init__(parent, title = "Organizar archivos", size=(800, 400))
        self.parent = parent
        self.ruta_carpeta = ruta_carpeta
        #self.panel.arbol.Bind(wx.EVT_TREE_SEL_CHANGED, self.abrir_archivo)
        panel = wx.Panel(self)
        texto = wx.StaticText(panel, label="Seleccione una opción para organizar los archivos:")
        texto_2 = wx.StaticText(panel, label="ADVERTENCIA: Esta acción moverá los archivos a sus respectivas carpetas y no se podrá deshacer.")
        opcion_tipo_archivo = wx.RadioButton(panel, label="Organizar por tipo de archivo", style=wx.RB_GROUP)
        boton_organizar = wx.Button(panel, label="Organizar ahora")
        boton_organizar.Bind(wx.EVT_BUTTON, self.organizar_archivos)

        #Sizer de la ventana "Organizar archivos"
        sizer= wx.BoxSizer(wx.VERTICAL)
        sizer.Add(texto, proportion=0, flag=wx.ALL, border=10)
        sizer.Add(texto_2, proportion=0, flag=wx.ALL, border=10)
        sizer.Add(opcion_tipo_archivo, proportion=0, flag=wx.ALL, border=10)
        sizer.Add(boton_organizar, proportion=0, flag=wx.ALL, border=10)

        panel.SetSizer(sizer)
    
    #def abrir_archivo(self, event):
        #item = event.GetItem()


    
#Evento del botón "Organizar ahora"
    def organizar_archivos(self, event):
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
        for archivo in os.listdir(self.ruta_carpeta):
            ruta_archivo = os.path.join(self.ruta_carpeta, archivo)
            if os.path.isdir(ruta_archivo):
                continue
            extension = os.path.splitext(archivo)
            extension = extension[1].lower()  # Obtener la extensión en minúsculas
            carpeta_destino = "Otros"
            for categoria, extensiones in categorias.items():
                if extension in extensiones:
                    carpeta_destino = categoria
                    break
            ruta_destino = os.path.join(self.ruta_carpeta, carpeta_destino)
            os.makedirs(ruta_destino, exist_ok=True)
            shutil.move(ruta_archivo, os.path.join(ruta_destino, archivo))
        wx.MessageBox("Archivos organizados correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        self.parent.actualizar_arbol() #Llama a la funcion actualizar_arbol() del frame principal para actualizarlo
        self.Close() #Cierra la ventana "Organizar archivos" despues de organizar los archivos

class MiFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="FileSort", size=(900, 600))
        self.panel= MiPanel(self)
        icono = (wx.Icon(path, wx.BITMAP_TYPE_ICO)
                 if (path := next((p for p in (os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icono.ico'), os.path.join(os.getcwd(), 'icono.ico'))
                                   if os.path.exists(p)), None)) else wx.NullIcon())
        self.SetIcon(icono)

        #Barra de busqueda
        self.panel.boton_buscar.Bind(wx.EVT_BUTTON, self.buscar_archivo)
        self.panel.barra_busqueda.Bind(wx.EVT_TEXT_ENTER, self.buscar_archivo)

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

        #Asignar la barra de menú al frame
        self.SetMenuBar(barra_menu)
        
        #Eventos del menú
        self.Bind(wx.EVT_MENU, self.abrir_carpeta, opcion_abrir_carpeta)
        #self.Bind(wx.EVT_MENU, self.ordenar_por_nombre, opcion_ordenar_nombre)
        #self.Bind(wx.EVT_MENU, self.ordenar_por_fecha, opcion_ordenar_fecha)
        #self.Bind(wx.EVT_MENU, self.ordenar_por_tamaño_mayor, opcion_ordenar_tamaño_mayor)
        #self.Bind(wx.EVT_MENU, self.ordenar_por_tamaño_menor, opcion_ordenar_tamaño_menor)
        self.Bind(wx.EVT_MENU, self.abrir_ventana_organizar, opcion_organizar_archivos)
        self.Bind(wx.EVT_MENU, self.tema_oscuro, opcion_tema_oscuro)
        self.Bind(wx.EVT_MENU, self.tema_claro, opcion_tema_claro)
        self.Bind(wx.EVT_MENU, self.mostrar_estadisticas, opcion_estadisticas)

        #Detecta las columnas
        self.panel.arbol.Bind(wx.EVT_TREE_SEL_CHANGED, self.mostrar_contenido_carpeta)
        
        #Hace doble clic en el archivo para abrirlo
        self.panel.arbol.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.abrir_archivo)


        self.Show()
        self.Center()
    
    #Funciones para cambiar el tema de la app
    def tema_oscuro(self, event):
        self.panel.SetBackgroundColour(wx.Colour(30, 30, 30))
        self.panel.arbol.SetBackgroundColour(wx.Colour(40, 40, 40))
        self.panel.arbol.SetForegroundColour(wx.WHITE)
        self.panel.lista.SetBackgroundColour(wx.Colour(40, 40, 40))
        self.panel.lista.SetForegroundColour(wx.WHITE)
        self.Refresh()

    def tema_claro(self, event):
        self.panel.SetBackgroundColour(wx.WHITE)
        self.panel.arbol.SetBackgroundColour(wx.WHITE)
        self.panel.arbol.SetForegroundColour(wx.BLACK)
        self.panel.lista.SetBackgroundColour(wx.WHITE)
        self.panel.lista.SetForegroundColour(wx.BLACK)
        self.Refresh()

    #Funcion para mostrar las estadisticas del directorio
    def mostrar_estadisticas(self, event):
        if not hasattr(self, "ruta_carpeta"):
            wx.MessageBox("Primero debes abrir una carpeta.", "FileSort", wx.OK | wx.ICON_WARNING)
            return
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

        for ruta_actual, directorios, archivos in os.walk(self.ruta_carpeta):
            total_carpetas += len(directorios)
            for archivo in archivos:
                total_archivos += 1
                ruta_archivo = os.path.join(ruta_actual, archivo)
                tamaño_total += os.path.getsize(ruta_archivo)
                extension = os.path.splitext(archivo)[1].lower()
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
            tamaño_MB = round(tamaño_total / (1024 * 1024), 2)
            mensaje = (
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
        wx.MessageBox(mensaje, "Estadísticas de carpeta", wx.OK | wx.ICON_INFORMATION)
            
    #Ventana para organizar archivos
    def abrir_ventana_organizar(self, event):
        if not hasattr(self, "ruta_carpeta"):
           wx.MessageBox("Primero debes abrir una carpeta.", "FileSort", wx.OK | wx.ICON_WARNING)
           return
        self.ventana_organizar = OrganizarArchivosDialog(self, self.ruta_carpeta)
        self.ventana_organizar.Show()
    
    #Esta funcion carga el arbol con los directorios y archivos de la ruta seleccionada
    def cargar_arbol(self, ruta, nodo_padre):
        elementos = os.listdir(ruta)
        for elemento in elementos:
            ruta_completa = os.path.join(ruta, elemento)
            if os.path.isdir(ruta_completa):
                nodo = self.panel.arbol.AppendItem(nodo_padre, elemento, image = self.panel.icono_carpeta)
                self.panel.arbol.SetItemData(nodo, ruta_completa)
                self.cargar_arbol(ruta_completa, nodo)
            else:
                nodo = self.panel.arbol.AppendItem(nodo_padre, elemento, image = self.panel.icono_archivo)
                self.panel.arbol.SetItemData(nodo, ruta_completa)

    #funcion para buscar archivos en el directorio seleccionado
    def buscar_archivo(self, event):
        texto = self.panel.barra_busqueda.GetValue().lower()
        if texto == "":
            return
        self.panel.lista.DeleteAllItems()
        for ruta_actual, carpetas, archivos in os.walk(self.ruta_carpeta):
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
        self.panel.lista.DeleteAllItems()

        for archivo in os.listdir(ruta):
            ruta_archivo = os.path.join(ruta, archivo)

            if os.path.isdir(ruta_archivo):
                tipo = "Carpeta"
                tamaño = "-"
            else:
                tipo = os.path.splitext(archivo)[1]
                tamaño = str(os.path.getsize(ruta_archivo) // 1024) + "KB" 
                if os.path.getsize(ruta_archivo) < 1024 * 1024 :
                    tamaño = str(os.path.getsize(ruta_archivo) // 1024) + "KB"
                else:
                    tamaño = str(os.path.getsize(ruta_archivo) // (1024 * 1024)) + "MB"
                #else:
                 #   tamaño = str(os.path.getsize(ruta_archivo) // (1024 * 1024 * 1024)) + "GB"

            fecha = datetime.datetime.fromtimestamp(
                    os.path.getmtime(ruta_archivo)).strftime("%d/%m/%Y %H:%M")
            indice = self.panel.lista.InsertItem(self.panel.lista.GetItemCount(), archivo)
            self.panel.lista.SetItem(indice, 1, tipo)
            self.panel.lista.SetItem(indice, 2, tamaño)
            self.panel.lista.SetItem(indice, 3, fecha)

    def abrir_archivo(self, event):
        item = event.GetItem()
        ruta = self.panel.arbol.GetItemData(item)
        if os.path.isfile(ruta):
            os.startfile(ruta)

    #Funciones del menu
    
    #Función para abrir el directorio y mostrar los archivos en la lista
    def abrir_carpeta(self,event):
        dialogo = wx.DirDialog(self, "Selecciona un directorio")
        if dialogo.ShowModal() == wx.ID_OK:
            self.ruta_carpeta = dialogo.GetPath()
            self.panel.arbol.DeleteAllItems()  # Limpiar el árbol antes de agregar nuevos elementos
            raiz = self.panel.arbol.AddRoot(os.path.basename(self.ruta_carpeta))
            self.panel.arbol.SetItemData(raiz, self.ruta_carpeta)
            self.cargar_arbol(self.ruta_carpeta, raiz)
            self.panel.arbol.Expand(raiz)  # Expandir el nodo raíz para mostrar los archivos

        dialogo.Destroy() #Destruye el dialogo despues de seleccionar la carpeta

    #Funcion para actualizar arbol y lista despues de organizar archivos
    def actualizar_arbol(self):
        self.panel.arbol.DeleteAllItems()  # Limpiar el árbol antes de agregar nuevos elementos
        raiz = self.panel.arbol.AddRoot(os.path.basename(self.ruta_carpeta))
        self.panel.arbol.SetItemData(raiz, self.ruta_carpeta)
        self.cargar_arbol(self.ruta_carpeta, raiz)
        self.panel.arbol.Expand(raiz)  # Expandir el nodo raíz para mostrar los archivos

#pregunta si la app corre local o la importe
if __name__ == "__main__":
    app = wx.App(redirect=False)
    frame= MiFrame()
    app.MainLoop()
