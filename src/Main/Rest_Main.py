
import gi
import re
import locale
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from Main import BD_Conect, BD_Prov
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Restaurante:
    def __init__(self):
        Gra = Gtk.Builder()
        Gra.add_from_file('Rest.glade')
        #Ventanas
        self.VP = Gra.get_object("VP")
        self.LS = Gra.get_object("LoginScreen")
        self.VT_Conf = Gra.get_object("VT_Confirmation")
        self.VService = Gra.get_object("V_AddService")
        self.ET_User = Gra.get_object("ET_LS_User")
        self.ET_Pass = Gra.get_object("ET_LS_Passwd")
        #Botones de Mesas
        self.BT_Mesa1 = Gra.get_object("BT_Mesa1")
        self.BT_Mesa2 = Gra.get_object("BT_Mesa2")
        self.BT_Mesa3 = Gra.get_object("BT_Mesa3")
        self.BT_Mesa4 = Gra.get_object("BT_Mesa4")
        self.BT_Mesa5 = Gra.get_object("BT_Mesa5")
        self.BT_Mesa6 = Gra.get_object("BT_Mesa6")
        self.BT_Mesa7 = Gra.get_object("BT_Mesa7")
        self.BT_Mesa8 = Gra.get_object("BT_Mesa8")
        #Botones de clientes
        self.BT_AddC = Gra.get_object("BT_FinalAdd")
        self.BT_ModC = Gra.get_object("BT_Modificar")
        self.BT_DelC = Gra.get_object("BT_Eliminar")
        #Imágenes de mesas
        self.IMG_Mesa1 = Gra.get_object("Mesa1")
        self.IMG_Mesa2 = Gra.get_object("Mesa2")
        self.IMG_Mesa3 = Gra.get_object("Mesa3")
        self.IMG_Mesa4 = Gra.get_object("Mesa4")
        self.IMG_Mesa5 = Gra.get_object("Mesa5")
        self.IMG_Mesa6 = Gra.get_object("Mesa6")
        self.IMG_Mesa7 = Gra.get_object("Mesa7")
        self.IMG_Mesa8 = Gra.get_object("Mesa8")
        #Labels
        self.LB_LE = Gra.get_object("LB_LOGIN_ERROR")
        self.LB_Check = Gra.get_object("LB_LogCheck")
        self.LB_MS = Gra.get_object("LB_MS")
        self.LB_Confirm = Gra.get_object("LB_Confirm")
        #EntryBox
        self.EB_SearchC = Gra.get_object("EB_SearchU")
        self.EB_C_DNI = Gra.get_object("EB_C_DNI")
        self.EB_C_Nombre = Gra.get_object("EB_C_Nombre")
        self.EB_C_Apellidos = Gra.get_object("EB_C_Apellidos")
        self.EB_C_Direccion = Gra.get_object("EB_C_Direccion")
        self.EB_NSN = Gra.get_object("EB_AddSN")
        self.EB_NSP = Gra.get_object("EB_AddSP")
        self.EB_S_Selected = Gra.get_object("EB_S_MS")
        self.EB_S_Camarero = Gra.get_object("EB_S_Cam")
        self.EB_S_Cliente = Gra.get_object("EB_S_Cli")
        self.EB_S_CosteTotal = Gra.get_object("EB_S_CT")
        self.EB_S_Searcher = Gra.get_object("EB_S_Searcher")
        self.EB_F_ClientSearcher = Gra.get_object("EB_F_ClientSearch")
        #ComboBox
        self.CB_C_Provincia = Gra.get_object("CB_C_Provincia")
        self.CB_C_Ciudad = Gra.get_object("CB_C_Ciudad")
        #Otros
        self.NB_Principal = Gra.get_object("NB_Menus")
        self.NB_Clientes = Gra.get_object("NB_Clientes")
        self.CA_Fecha = Gra.get_object("Calendar")
        #Trees
        self.TreeMesas = Gra.get_object("Tree_Mesas")
        self.TreeClientes = Gra.get_object("TR_Clientes")
        self.TreeServicios = Gra.get_object("TreeServicios")
        self.TreeFactsLite = Gra.get_object("Tree_Facts_S")
        self.TreeSM = Gra.get_object("Tree_Mesas_S")
        self.TreeSFM = Gra.get_object("TreeS_F_M")
        self.TreeF_Cliente = Gra.get_object("Tree_F_Clientes")
        self.TreeF_Factura = Gra.get_object("Tree_F_Facturas")
        self.Tree_F_Mesas = Gra.get_object("Tree_Mesas_F")
        #Lists
        self.ListMesas = Gra.get_object("ListMesas")
        self.ListServicios = Gra.get_object("ListServ")
        self.ListFactsLite = Gra.get_object("ListFactsLite")
        self.ListClientes = Gra.get_object("LS_Clientes")
        self.ListSFM = Gra.get_object("ListS_F_M")
        self.ListPro = Gra.get_object("ListProvincias")
        self.ListCiu = Gra.get_object("ListCiudad")
        self.ListF_Cliente = Gra.get_object("List_F_Clientes")
        self.ListF_Factura = Gra.get_object("List_F_Facturas")
        #Variables globales
        self.Selected = 0 #Mesa seleccionada
        self.ServiceSelected = 0
        self.CursorSelected = False
        self.CursorServicesSelected = False
        self.CursorFactLiteSlected = False
        self.CamID = 0 #ID del camarero logeado
        self.ID_Confirm = 0
        #ID de la alerta que necesita confirmación
        ## 0 - Null
        ## 1 - Borrado de cliente
        dic = {
        ################ SALIDAS ##################################
                'on_VP_destroy': self.salir,
                'on_BT_LOGIN_EXIT_clicked': self.salir,
                'on_TB_Salir_clicked': self.salir,
        ################# CONTROL DE PESTAÑAS ####################
                'on_TB_Mesas_clicked': self.Mesas,
                'on_TB_Servicios_clicked': self.Servicios,
                'on_TB_Facturas_clicked': self.Facturas,
                'on_TB_ChangeUser_clicked': self.ReLogin,
                'on_BT_Añadir_clicked': self.AddWindow,
                'on_BT_Eliminar_clicked': self.DelUser,
                'on_BT_FinalBack_clicked': self.BackToList,
        ################# BOTONES DE LAS MESAS ####################
                'on_BT_MesaP1_clicked': self.Mesa1,
                'on_BT_MesaP2_clicked': self.Mesa2,
                'on_BT_MesaP3_clicked': self.Mesa3,
                'on_BT_MesaP4_clicked': self.Mesa4,
                'on_BT_MesaM1_clicked': self.Mesa5,
                'on_BT_MesaM2_clicked': self.Mesa6,
                'on_BT_MesaG1_clicked': self.Mesa7,
                'on_BT_MesaG2_clicked': self.Mesa8,
        ################# Otros botones ###########################
                'on_BT_MOccuped_clicked': self.Occupped,
                'on_Tree_Mesas_cursor_changed': self.SelToDis,
                'on_BT_MFree_clicked': self.Disocupped,
                'on_BT_Conf_YES_clicked': self.ConfYES,
                'on_BT_Conf_NO_clicked': self.ConfNO,
        ################ Añadir servicios ########################
                'on_BT_NewService_clicked': self.NewService,
                'on_BT_AddNS_clicked': self.AddNewService,
                'on_BT_CancelNS_clicked':self.CancelAddNewService,
                'on_BT_AddS_clicked': self.BuyService,
                'on_BT_CancelS_clicked': self.DelService,
        ################ BT Clientes #################
                'on_BT_FinalAdd_clicked': self.AñadirCliente,
        ################ LOGIN ####################
                'on_BT_LS_Login_clicked': self.Login,
                'on_ET_LS_Passwd_key_press_event': self.KeyLoggin,
        ################ OTROS ####################
                'on_EB_SearchU_key_press_event': self.KeySearch,
                'on_CB_C_Provincia_changed': self.LoadCBCiu,
                'on_TR_Clientes_cursor_changed': self.CursorSelection,
                'on_Tree_Mesas_S_cursor_changed': self.SFactsReload,
                'on_Tree_Mesas_F_cursor_changed': self.FFactsReload,
                'on_Tree_Facts_S_cursor_changed': self.FactsLiteLoad,
                'on_TreeServicios_cursor_changed': self.ServieCursorSelection,
                'on_EB_S_Searcher_button_release_event': self.ServiceSearch,
                'on_EB_F_ClientSearch_key_release_event': self.FCliSearch,
                'on_BT_Factura_clicked': self.FacturaCompleta,
                }
        
        Gra.connect_signals(dic)
        self.VP.show()
        self.VP.fullscreen()
        self.LoadMesas()
        self.LoadClientes()
        self.LoadCBPro()
        self.LS.show()
        
    def salir(self, widget, data=None):
        BD_Conect.Disconect()
        Gtk.main_quit()
    #### LOGINS ####
    def ReLogin(self,widget,data=None):
        self.LS.show()
    def KeyLoggin(self,widget,event):
        if event.keyval == 65293:
            self.Login(widget)
    def Login(self, widget,data=None):
        Log = (self.ET_User.get_text(),self.ET_Pass.get_text())
        Res = BD_Conect.LogCompr(Log)
        for Row in Res:
            self.LB_Check.set_text(" Logeado como: \n "+Row[1]) # Establece el label que indica el nombre del camarero logeado
            self.CamID = Row[0] # Guarda su ID para futuros usos sin necesidad de hacer mas busquedas
            if Row[0] != None:
                self.LS.hide()
        self.LB_LE.set_text("Usuario o contraseña incorrectos")
        
    def ConfirmationRequested(self):
        if self.ID_Confirm == 1:
            self.LB_Confirm.set_text("¿Está seguro de que quiere borrar a este cliente?")
        self.VT_Conf.show
    def ConfYES(self,widget,data=None):
        if self.ID_Confirm == 1:
            Model, ID = self.TreeClientes.get_selection().get_selected()
            ResC = BD_Conect.DelClient(self.ListClientes.get_value(ID,0))
            self.LoadClientes()
        self.VT_Conf.hide()
    def ConfNO(self,widget,data=None):
        self.VT_Conf.hide()
        self.ID_Confirm = 0
    
    def CursorSelection(self,widget,data=None):
        self.CursorSelected = True
    def ServieCursorSelection(self,widget,data=None):
        self.CursorServicesSelected = True
    ####### Control de pestañas ########
    #Los siguientes metodos simplemente modifican la pestaña activa del "notebook"
    def Mesas(self, widget,data=None):
        self.LoadMesas()
        self.LoadClientes()
        self.CursorSelected = False
        self.Selected = 0
        self.NB_Principal.set_current_page(0)
    def Servicios(self, widget,data=None):
        self.LoadS()
        self.LoadMesas()
        self.ServiceSelected = 0
        Res = BD_Conect.Load(3)
        self.ListFactsLite.clear()
        for i in Res:
            file = (i[0],i[1],i[4])
            BD_Conect.AltaLista(self.TreeFactsLite, self.ListFactsLite, file)
        self.EB_S_Selected.set_text("")
        self.EB_S_Camarero.set_text("")
        self.EB_S_Cliente.set_text("")
        self.EB_S_CosteTotal.set_text("")
        self.CursorServicesSelected = False
        self.CursorFactLiteSlected = False
        self.NB_Principal.set_current_page(1)
    def Facturas(self, widget,data=None):
        self.LoadMesas()
        self.ListF_Cliente.clear()
        Res = BD_Conect.Load(1)
        for i in Res:
            fila = (i[0],i[1],i[2],i[3],i[4],i[5])
            BD_Conect.AltaLista(self.TreeF_Cliente, self.ListF_Cliente, fila)
        self.ListF_Factura.clear()
        Res = BD_Conect.Load(4)
        for i in Res:
            fila = (i[0],i[1],i[2],i[3],i[4])
            BD_Conect.AltaLista(self.TreeF_Factura, self.ListF_Factura, fila)
        
        self.NB_Principal.set_current_page(2)
    def AddWindow(self,widget,data=None):
        self.NB_Clientes.set_current_page(1)
    def BackToList(self,widget,data=None):
        self.NB_Clientes.set_current_page(0)
        
    #################### Cargas de los treeviews y las listas ###########################
    #### Carga del treeview y del estado de las mesas ####
    def LoadMesas(self):
        ### Limpiamos la lista actual del treeview
        self.ListMesas.clear()
        ### Obtenemos una lista de todas las mesas y su estado.
        Res = BD_Conect.Load(0)
        ### Para cada mesa comprobamos si está ocupada, en ese caso el botón cambio de imagen y se bloquea
        ### Si no está ocupada el botón se desbloquea y la imágen vuelve a la de disponible
        for i in Res:
            fila = (i[0],i[1],i[2])
            if fila[0] == 1:
                if fila[2] == 'Si':
                    self.IMG_Mesa1.set_from_file("../IMG/Mesa4_NO.jpg")
                    self.BT_Mesa1.set_sensitive(False)
                else:
                    self.IMG_Mesa1.set_from_file("../IMG/Mesa4_SI.jpg")
                    self.BT_Mesa1.set_sensitive(True)
            elif fila[0] == 2:
                if fila[2] == 'Si':
                    self.IMG_Mesa2.set_from_file("../IMG/Mesa4_NO.jpg")
                    self.BT_Mesa2.set_sensitive(False)
                else:
                    self.IMG_Mesa2.set_from_file("../IMG/Mesa4_SI.jpg")
                    self.BT_Mesa2.set_sensitive(True)
            elif fila[0] == 3:
                if fila[2] == 'Si':
                    self.IMG_Mesa3.set_from_file("../IMG/Mesa4_NO.jpg")
                    self.BT_Mesa3.set_sensitive(False)
                else:
                    self.IMG_Mesa3.set_from_file("../IMG/Mesa4_SI.jpg")
                    self.BT_Mesa3.set_sensitive(True)
            elif fila[0] == 4:
                if fila[2] == 'Si':
                    self.IMG_Mesa4.set_from_file("../IMG/Mesa4_NO.jpg")
                    self.BT_Mesa4.set_sensitive(False)
                else:
                    self.IMG_Mesa4.set_from_file("../IMG/Mesa4_SI.jpg")
                    self.BT_Mesa4.set_sensitive(True)
            elif fila[0] == 5:
                if fila[2] == 'Si':
                    self.IMG_Mesa5.set_from_file("../IMG/Mesa6_NO.jpg")
                    self.BT_Mesa5.set_sensitive(False)
                else:
                    self.IMG_Mesa5.set_from_file("../IMG/Mesa6_SI.jpg")
                    self.BT_Mesa5.set_sensitive(True)
            elif fila[0] == 6:
                if fila[2] == 'Si':
                    self.IMG_Mesa6.set_from_file("../IMG/Mesa6_NO.jpg")
                    self.BT_Mesa6.set_sensitive(False)
                else:
                    self.IMG_Mesa6.set_from_file("../IMG/Mesa6_SI.jpg")
                    self.BT_Mesa6.set_sensitive(True)
            elif fila[0] == 7:
                if fila[2] == 'Si':
                    self.IMG_Mesa7.set_from_file("../IMG/Mesa8_NO.jpg")
                    self.BT_Mesa7.set_sensitive(False)
                else:
                    self.IMG_Mesa7.set_from_file("../IMG/Mesa8_SI.jpg")
                    self.BT_Mesa7.set_sensitive(True)
            elif fila[0] == 8:
                if fila[2] == 'Si':
                    self.IMG_Mesa8.set_from_file("../IMG/Mesa8_NO.jpg")
                    self.BT_Mesa8.set_sensitive(False)
                else:
                    self.IMG_Mesa8.set_from_file("../IMG/Mesa8_SI.jpg")
                    self.BT_Mesa8.set_sensitive(True)
        ### Obtenemos una lista sólo de las mesas ocupadas para poner en el tree view
        ResOcuped = BD_Conect.LoadOccuped()
        for i in ResOcuped:
            fila = (i[0],i[1],i[2])
            BD_Conect.AltaLista(self.TreeMesas, self.ListMesas, fila)
    #### Carga del tree view de clientes ####
    def LoadClientes(self):
        ### Limpiamos la lista actual del treeview
        self.ListClientes.clear()
        ResCli = BD_Conect.Load(1)
        for i in ResCli:
            fila = (i[0],i[1],i[2])
            BD_Conect.AltaLista(self.TreeClientes, self.ListClientes, fila)
    def LoadCBPro(self):
        BD_Prov.Load(self.ListPro)
    def LoadCBCiu(self,widget,data=None):
        BD_Prov.LoadCiu(self.ListCiu,self.CB_C_Provincia.get_active())
        
    def LoadS(self):
        self.ListServicios.clear()
        Res = BD_Conect.Load(2)
        for i in Res:
            fila = (i[1],str(i[2]),i[0])
            BD_Conect.AltaLista(self.TreeServicios, self.ListServicios, fila)
    def SFactsReload(self,widget,data=None):
        self.ListFactsLite.clear()
        model, iter = self.TreeSM.get_selection().get_selected()
        ID = model.get_value(iter,0)
        Res = BD_Conect.LoadFactLite(ID)
        for i in Res:
            file = (i[0],i[1],i[4])
            BD_Conect.AltaLista(self.TreeFactsLite, self.ListFactsLite, file)
    def FactsLiteLoad(self,widget,data=None):
        self.CursorFactLiteSlected = True
        model, iter = self.TreeFactsLite.get_selection().get_selected()
        ID = model.get_value(iter,0)
        Res1 = BD_Conect.LoadOnService(ID)
        for i in Res1:
            DatosFactura = (i[0],i[1],i[2])
        self.ServiceSelected = DatosFactura[0]
        if self.ServiceSelected > 0 and self.ServiceSelected <= 4:
            Com = " - 6 Comensales"
        elif self.ServiceSelected > 4 and self.ServiceSelected <= 5:
            Com = " - 8 Comensales"
        elif self.ServiceSelected > 5:
            Com = " - 10 Comensales"
        self.EB_S_Selected.set_text("Mesa: "+str(self.ServiceSelected)+Com)
        self.EB_S_Camarero.set_text(DatosFactura[1])
        self.EB_S_Cliente.set_text(DatosFactura[2])
        Total = 0
        self.ListSFM.clear()
        Res = BD_Conect.LoadLF(ID)
        for i in Res:
            file = (str(i[0]),str(i[1]),str(i[2]))
            Total = Total + i[1]*i[2]
            BD_Conect.AltaLista(self.TreeSFM, self.ListSFM, file)
        self.EB_S_CosteTotal.set_text(str(Total)+"€")
            
    def FFactsReload(self,widget,data=None):
        self.ListF_Factura.clear()
        model, iter = self.Tree_F_Mesas.get_selection().get_selected()
        ID = model.get_value(iter,0)
        Res = BD_Conect.LoadFactFilter(ID)
        for i in Res:
            file = (i[0],i[1],i[2],i[3],i[4])
            BD_Conect.AltaLista(self.TreeF_Factura, self.ListF_Factura, file)
    
    ################# Métodos de las mesas ###################
    ### Cada método cambia la variable "Selected" y el Label que indica cúal está seleccionada
    def Mesa1(self, widget, data=None):
        self.LB_MS.set_text("Mesa: 1 - 6 Comensales")
        self.Selected = 1
    def Mesa2(self, widget, data=None):
        self.LB_MS.set_text("Mesa: 2 - 6 Comensales")
        self.Selected = 2
    def Mesa3(self, widget, data=None):
        self.LB_MS.set_text("Mesa: 3 - 6 Comensales")
        self.Selected = 3
    def Mesa4(self, widget, data=None):
        self.LB_MS.set_text("Mesa: 4 - 6 Comensales")
        self.Selected = 4
    def Mesa5(self, widget, data=None):
        self.LB_MS.set_text("Mesa: 5 - 8 Comensales")
        self.Selected = 5
    def Mesa6(self, widget, data=None):
        self.LB_MS.set_text("Mesa: 6 - 8 Comensales")
        self.Selected = 6
    def Mesa7(self, widget, data=None):
        self.LB_MS.set_text("Mesa: 7 - 10 Comensales")
        self.Selected = 7
    def Mesa8(self, widget, data=None):
        self.LB_MS.set_text("Mesa: 8 - 10 Comensales")
        self.Selected = 8
        
        
    ################### Métodos principales #########################
    
        ### Apartado de mesas y reservas ###
    def Occupped(self, widget, data=None):
        """Ocupación de mesas
        
        Este método se encarga del estado de las mesas cuando se oprime el botón de 'Ocupar'
        """
        if self.Selected == 0:# Si la variable de seleccion está a 0 es que no se ha presionado ningún botón de mesa.
            self.LB_MS.set_text("Debe seleccionar una mesa primero")
        elif self.Selected == -1:# Si está a -1 es que se ha seleccionado una mesa ocupada del tree view
            self.LB_MS.set_text("Esa mesa ya estaba ocupada")
        elif self.Selected > 0:
            if self.CursorSelected == False:
                self.LB_MS.set_text("Tiene que seleccionar un cliente primero")
            else:
                Model, ID = self.TreeClientes.get_selection().get_selected()
                Año, Mes, Dia = self.CA_Fecha.get_date()
                Fecha = str(Año)+"-"+str(Mes)+"-"+str(Dia)
                fila = (self.Selected, self.ListClientes.get_value(ID,0),self.CamID,Fecha)
                BD_Conect.Ocupped(fila)
            
        self.LoadMesas()
    
    def SelToDis(self, widget, data=None):
        """Seleccionar para desocupar
        
        Este método permite seleccionar una mesa de la lista de ocupadas para liberarla.
        """
        model, iter = self.TreeMesas.get_selection().get_selected()
        if iter != None:
            ID = model.get_value(iter, 0) # Cogemos la ID de la mesa de la tabla
            self.LB_MS.set_text("Mesa "+str(ID)+" Ocupada")
            self.Selected = -1 # Se cambia la variable de selected a -1 para evitar conflictos si se le da al botón de "Ocupar"
    
    def Disocupped(self, widget, data=None):
        model, iter = self.TreeMesas.get_selection().get_selected()
        if iter != None:
            ID = model.get_value(iter, 0) # Cogemos la ID de la mesa de la tabla
            BD_Conect.Disocupped(ID) #Se cambia el estado de la columna "Ocupada" de la base de datos para la mesa seleccionada
        self.LoadMesas()
    
    ##### Apartado de clientes #####
    
    def AñadirCliente(self,widget,data=None):
        fila = (self.EB_C_DNI.get_text(),self.EB_C_Apellidos.get_text(),self.EB_C_Nombre.get_text(),self.EB_C_Direccion.get_text(),self.ListPro.get_value(self.CB_C_Provincia.get_active_iter(),0),self.ListCiu.get_value(self.CB_C_Ciudad.get_active_iter(),0))
        BD_Conect.Insert(fila, 0)
        self.LoadClientes()
        self.NB_Clientes.set_current_page(0)
        
    def DelUser(self,widget,data=None):
        self.ID_Confirm = 1
        self.ConfirmationRequested()
        
    def KeySearch(self,widget,event):
        """Búsqueda rápida por apellido
        
        Mientras se escriba en la EntryBox del apartado de clientes cada vez que se teclee se realizará una búsqueda de los clientes mediante su apellido
        """
        ResCli = BD_Conect.SearchCli(self.EB_SearchC.get_text())
        self.ListClientes.clear()
        for i in ResCli:
            fila = (i[0],i[1],i[2])
            BD_Conect.AltaLista(self.TreeClientes, self.ListClientes, fila)
            
    ###### Servicios #######
    def NewService(self,widget,data=None):
        self.EB_NSN.set_text("")
        self.EB_NSP.set_text("")
        self.VService.show()
    def CancelAddNewService(self,widget,data=None):
        self.VService.hide()
    def AddNewService(self,widget,data=None):
        fila = (self.EB_NSN.get_text(),self.EB_NSP.get_text())
        BD_Conect.Insert(fila, 1)
        self.LoadS()
        self.VService.hide()
    def BuyService(self,widget,data=None):
        if self.CursorFactLiteSlected == True:
            if self.CursorServicesSelected == True:
                model, iter = self.TreeFactsLite.get_selection().get_selected()
                IDF = model.get_value(iter,0)
        
                model, iter = self.TreeServicios.get_selection().get_selected()
                IDS = model.get_value(iter,2)
                
                BD_Conect.InsertSF(IDF, IDS)
                self.ListSFM.clear()
                Res = BD_Conect.LoadLF(IDF)
                Total = 0
                for i in Res:
                    file = (str(i[0]),str(i[1]),str(i[2]))
                    Total = Total + i[1]*i[2]
                    BD_Conect.AltaLista(self.TreeSFM, self.ListSFM, file)
                self.EB_S_CosteTotal.set_text(str(Total)+"€")
            else:
                a = 1
        else:
            placeholder = 1
            
    def DelService(self,widget,data=None):
        model, iter = self.TreeFactsLite.get_selection().get_selected()
        IDF = model.get_value(iter,0)
        
        model, iter = self.TreeSFM.get_selection().get_selected()
        IDS = model.get_value(iter,0)
                
        BD_Conect.DelLF(IDF, IDS)
        self.ListSFM.clear()
        Res = BD_Conect.LoadLF(IDF)
        Total = 0
        for i in Res:
            file = (str(i[0]),str(i[1]),str(i[2]))
            Total = Total + i[1]*i[2]
            BD_Conect.AltaLista(self.TreeSFM, self.ListSFM, file)
        self.EB_S_CosteTotal.set_text(str(Total)+"€")
            
    def ServiceSearch(self,widget,data=None):
        self.ListServicios.clear()
        Res = BD_Conect.SearchService(self.EB_S_Searcher.get_text())
        for i in Res:
            fila = (i[1],str(i[2]),i[0])
            BD_Conect.AltaLista(self.TreeServicios, self.ListServicios, fila)
    
    def FCliSearch(self,widget,data=None):
        ResCli = BD_Conect.SearchCli(self.EB_F_ClientSearcher.get_text())
        self.ListF_Cliente.clear()
        for i in ResCli:
            fila = (i[0],i[1],i[2],i[3],i[4],i[5])
            BD_Conect.AltaLista(self.TreeF_Cliente, self.ListF_Cliente, fila)
            
    def FacturaCompleta(self,widget,data=None):
        """ Crea la factura para el cliente
        Necesita acceder a dos tablas (join), la propia de la factura y la tabla de servicios
        para obtener los nombres de las comandas y precios, así genera los subtotales y totales.
        Hay ajustes para una mejor alineacion de la presentacion
        """
        try:
            model, iter = self.TreeF_Factura.get_selection().get_selected()
            idfactura = model.get_value(iter,0)
            cser = canvas.Canvas( str(idfactura) + '.pdf', pagesize=A4)
            cabecera(cser) #creamos la cabecera y pie del documento (son otros módulos)
            pie(cser)
            bbdd.cur.execute('select idventa, s.servicio, cantidad, s.precio from comandas as c, servicios as s where c.idfactura = ? and s.Id = c.idservicio', (idfactura,))
            listado = bbdd.cur.fetchall()
            bbdd.conexion.commit()
            textlistado = 'Factura'
            cser.drawString(255, 705, textlistado)
            cser.line(50, 700, 525, 700)
            x = 50
            y = 680
            total = 0
            for registro in listado:
                for i in range(4):
                    if i <= 1:
                        cser.drawString(x, y, str(registro[i]))
                        x = x + 40
                        #para mejorar la alineaciones, es probar y probar
                    else:
                        x = x + 120
                        #para mejorar la alineaciones, es probar y probar
                        cser.drawString(x, y, str(registro[i]))
                        var1 = int(registro[2])
                        # numero de platos
                        var2 = registro[3].split()[0] #precio plato le quito el símbolo €
                        var2 = locale.atof(var2)
                        var2 = round(float(var2), 2) #lo redondedo como float a dos decimales
                        subtotal = var1*var2
                        #precio lato por número de platos pedidos
                        total = total + subtotal
                        # cada pasada voy sumando
                        subtotal = locale.currency(subtotal)
                        #lo paso a moneda
                        x = x + 120
                        cser.drawString(x, y, str(subtotal))
                        y = y - 20
                        x = 50
                        y = y -20
                        #nuevo renglón o fila y vuelta a empezar
                        cser.line(50, y, 525, y)
                        y = y -20
                        x = 400
                        #probando y probando posiciones es una
                        cser.drawString(x, y, 'Total: ')
                        #cuestion de prueba y error
                        x = 485
                        total = round(float(total), 2)
                        #voy situado el total de la factura
                        total = locale.currency(total)
                        cser.drawString(x,y,str(total))
                        cser.showPage()
                        cser.save()
                        dir = os.getcwd()
                        os.system('/usr/bin/xdg-open ' + dir + '/' + str(idfactura) + '.pdf')
        except bbdd.sqlite3.OperationalError as e:
            print(e)
            bbdd.conexion.rollback()
            print('error en factura')
                            
if __name__ == '__main__':
    main = Restaurante()
    Gtk.main()