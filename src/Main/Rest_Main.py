
import gi
import re
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
        #EntryBox
        self.EB_SearchC = Gra.get_object("EB_SearchU")
        self.EB_C_DNI = Gra.get_object("EB_C_DNI")
        self.EB_C_Nombre = Gra.get_object("EB_C_Nombre")
        self.EB_C_Apellidos = Gra.get_object("EB_C_Apellidos")
        self.EB_C_Direccion = Gra.get_object("EB_C_Direccion")
        #ComboBox
        self.CB_C_Provincia = Gra.get_object("CB_C_Provincia")
        self.CB_C_Ciudad = Gra.get_object("CB_C_Ciudad")
        #Otros
        self.NB_Principal = Gra.get_object("NB_Menus")
        self.NB_Clientes = Gra.get_object("NB_Clientes")
        #Trees&Lists
        self.TreeMesas = Gra.get_object("Tree_Mesas")
        self.ListMesas = Gra.get_object("ListMesas")
        self.TreeClientes = Gra.get_object("TR_Clientes")
        self.ListClientes = Gra.get_object("LS_Clientes")
        self.ListPro = Gra.get_object("ListProvincias")
        self.ListCiu = Gra.get_object("ListCiudad")
        #Variables globales
        self.Selected = 0 #Mesa seleccionada
        self.CamID = 0 #ID del camarero logeado
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
                'on_BT_Modificar_clicked': self.ModUser,
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
        ################ BT Clientes #################
                'on_BT_FinalAdd_clicked': self.AñadirCliente,
        ################ LOGIN ####################
                'on_BT_LS_Login_clicked': self.Login,
                'on_ET_LS_Passwd_key_press_event': self.KeyLoggin,
        ################ OTROS ####################
                'on_EB_SearchU_key_press_event': self.KeySearch,
                'on_CB_C_Provincia_changed': self.LoadCBCiu,
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
    
    ####### Control de pestañas ########
    #Los siguientes metodos simplemente modifican la pestaña activa del "notebook"
    def Mesas(self, widget,data=None):
        self.NB_Principal.set_current_page(0)
    def Servicios(self, widget,data=None):
        self.NB_Principal.set_current_page(1)
    def Facturas(self, widget,data=None):
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
        ID = self.NB_Principal.get_current_page()
        ### Obtenemos una lista de todas las mesas y su estado.
        Res = BD_Conect.Load(ID)
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
        ResCli = BD_Conect.LoadCli()
        for i in ResCli:
            fila = (i[0],i[1],i[2])
            BD_Conect.AltaLista(self.TreeClientes, self.ListClientes, fila)
    def LoadCBPro(self):
        BD_Prov.Load(self.ListPro)
    def LoadCBCiu(self,widget,data=None):
        BD_Prov.LoadCiu(self.ListCiu,self.CB_C_Provincia.get_active())
            
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
            # Se cambia el estado de la columna "Ocupada" de la base de datos para la mesa seleccionada
            BD_Conect.Ocupped(self.Selected)
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
    
    def ModUser(self,widget,data=None):
        Model, ID = self.TreeClientes.get_selection().get_selected()
        ResC = BD_Conect.FindClient(self.ListClientes.get_value(ID,0))
        for i in ResC:
            fila = (i[0],i[1],i[2],i[3],i[4],i[5])
        
        self.EB_C_DNI.set_text(fila[0])
        self.EB_C_Apellidos.set_text(fila[1])
        self.EB_C_Nombre.set_text(fila[2])
        self.EB_C_Direccion.set_text(fila[3])
        
        self.NB_Clientes.set_current_page(1)
        
    def DelUser(self,widget,data=None):
        a = 0
    def KeySearch(self,widget,event):
        """Búsqueda rápida por apellido
        
        Mientras se escriba en la EntryBox del apartado de clientes cada vez que se teclee se realizará una búsqueda de los clientes mediante su apellido
        """
        ResCli = BD_Conect.SearchCli(self.EB_SearchC.get_text())
        self.ListClientes.clear()
        for i in ResCli:
            fila = (i[0],i[1],i[2])
            BD_Conect.AltaLista(self.TreeClientes, self.ListClientes, fila)
if __name__ == '__main__':
    main = Restaurante()
    Gtk.main()