from pyswip import Prolog, Functor, Variable, Query, newModule, call
Prolog.consult("base_de_conhecimento.pl")

import wx
import wx.grid

_ = Prolog()  # not strictly required, but helps to silence the linter
X = Variable()
Y = Variable()
R = Variable()
P = Variable()
I = Variable()
id = Functor("id", 2)
tipo = Functor("tiposanguineo", 2)
rh = Functor("fatorrh", 2)
rh2 = Functor("rh", 2)
peso = Functor("peso", 2)
idade = Functor("idade", 2)
podedoar = Functor("podedoar", 2)
mod = newModule("Mod1")

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(800, 600))

        # Set icon for the frame
        self.SetIcon(wx.Icon("resources/icon.ico"))

        # Initialize panel
        nb = wx.Notebook(self)
        nb.AddPage(Consulta(nb), "Consultar")
        nb.AddPage(TabelaCompatibilidade(nb), "Tabela de Compatibilidade")
        nb.AddPage(Dados(nb), "Banco de Dados")

class Consulta(wx.Panel):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridBagSizer(hgap=5, vgap=5)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.nomes = [0] * 14
        q = Query(id(X,Y), module=mod)
        i = 0
        while q.nextSolution():
            self.nomes[i] = str(Y.value)
            i+=1
        q.closeQuery()
        self.lblDoador = wx.StaticText(self, label="Doador:")
        grid.Add(self.lblDoador,pos=(3,0))
        self.editDoador = wx.ComboBox(self, size=(95, -1), choices=self.nomes, style=wx.CB_DROPDOWN)
        grid.Add(self.editDoador,pos=(4,0))
        self.botaoReceptor = wx.Button(self, label="Verificar Receptor disponível")
        grid.Add(self.botaoReceptor,pos=(5,0))
        self.Bind(wx.EVT_BUTTON, self.EvtClickReceptor, self.botaoReceptor)

        self.lblReceptor = wx.StaticText(self, label="Receptor:")
        grid.Add(self.lblReceptor,pos=(3,1))
        self.editReceptor = wx.ComboBox(self, size=(95, -1), choices=self.nomes, style=wx.CB_DROPDOWN)
        grid.Add(self.editReceptor,pos=(4,1))
        self.botaoDoador = wx.Button(self, label="Verificar Doador disponível")
        grid.Add(self.botaoDoador,pos=(5,1))
        self.Bind(wx.EVT_BUTTON, self.EvtClickDoador, self.botaoDoador)

        self.tipoSanguineo = ['A', 'B', 'AB', 'O']
        self.lblTipo = wx.StaticText(self, label="Tipo Sanguíneo:")
        grid.Add(self.lblTipo,pos=(3,2))
        self.editTipo = wx.ComboBox(self, size=(40, -1), choices=self.tipoSanguineo, style=wx.CB_DROPDOWN)
        grid.Add(self.editTipo,pos=(4,2))
        self.botaoTipo = wx.Button(self, label="Verificar Tipo Sanguíneo")
        grid.Add(self.botaoTipo,pos=(5,2))
        self.Bind(wx.EVT_BUTTON, self.EvtClickTipo, self.botaoTipo)
        
        self.fatorRH = ['+', '-']
        self.lblRH = wx.StaticText(self, label="Fator RH:")
        grid.Add(self.lblRH,pos=(3,3))
        self.editRH = wx.ComboBox(self, size=(40, -1), choices=self.fatorRH, style=wx.CB_DROPDOWN)
        grid.Add(self.editRH,pos=(4,3))
        self.botaoRH = wx.Button(self, label="Verificar Fator RH")
        grid.Add(self.botaoRH,pos=(5,3))
        self.Bind(wx.EVT_BUTTON, self.EvtClickRH, self.botaoRH)

        #grid.Add((10,40), pos=(2,0))

        self.tabela = wx.grid.Grid(self)
        self.tabela.CreateGrid(14, 5)
        self.tabela.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.tabela.SetRowLabelSize(0)

        #labels
        self.tabela.SetColLabelValue(0,"Nome")
        self.tabela.SetColLabelValue(1,"Tipo")
        self.tabela.SetColLabelValue(2,"RH")
        self.tabela.SetColLabelValue(3,"Peso")
        self.tabela.SetColLabelValue(4,"Idade")

        grid.Add(self.tabela, pos=(6,0), span=(1,4))
        
        hSizer.Add(grid, 0, wx.ALIGN_CENTER, 10)
        mainSizer.Add(hSizer, 0, wx.ALIGN_CENTER, 10)
        self.SetSizerAndFit(mainSizer)

    def EvtClickReceptor(self,event):
        #remove a seleção das outras comboboxes
        self.editReceptor.SetValue('')
        self.editRH.SetValue('')
        self.editTipo.SetValue('')
        #limpa a tabela
        for i in range(14):
            for j in range(5):
                self.tabela.SetCellValue(i,j,'')
        #preenche a tabela
        q = Query(podedoar(self.editDoador.GetString(self.editDoador.GetCurrentSelection()),Y), tipo(Y,X), rh(Y,R), peso(Y,P), idade(Y,I), module=mod)
        k = 0
        while q.nextSolution():
            self.tabela.SetCellValue(k,0,str(Y.value))
            self.tabela.SetCellValue(k,1,str(X.value).upper())
            self.tabela.SetCellValue(k,2,str(R.value))
            self.tabela.SetCellValue(k,3,str(P.value))
            self.tabela.SetCellValue(k,4,str(I.value))
            k+=1
        q.closeQuery()
    def EvtClickDoador(self,event):
        #remove a seleção das outras comboboxes
        self.editDoador.SetValue('')
        self.editRH.SetValue('')
        self.editTipo.SetValue('')
        #limpa a tabela
        for i in range(14):
            for j in range(5):
                self.tabela.SetCellValue(i,j,'')
        #preenche a tabela
        q = Query(podedoar(Y,self.editReceptor.GetString(self.editReceptor.GetCurrentSelection())), tipo(Y,X), rh(Y,R), peso(Y,P), idade(Y,I), module=mod)
        k = 0
        while q.nextSolution():
            self.tabela.SetCellValue(k,0,str(Y.value))
            self.tabela.SetCellValue(k,1,str(X.value).upper())
            self.tabela.SetCellValue(k,2,str(R.value))
            self.tabela.SetCellValue(k,3,str(P.value))
            self.tabela.SetCellValue(k,4,str(I.value))
            k+=1
        q.closeQuery()
    def EvtClickTipo(self, event):
        #remove a seleção das outras comboboxes
        self.editReceptor.SetValue('')
        self.editRH.SetValue('')
        self.editDoador.SetValue('')
        #limpa a tabela
        for i in range(14):
            for j in range(5):
                self.tabela.SetCellValue(i,j,'')
        #preenche a tabela
        q = Query(tipo(Y,self.editTipo.GetString(self.editTipo.GetCurrentSelection()).lower()), tipo(Y,X), rh(Y,R), peso(Y,P), idade(Y,I), module=mod)
        k = 0
        while q.nextSolution():
            self.tabela.SetCellValue(k,0,str(Y.value))
            self.tabela.SetCellValue(k,1,str(X.value).upper())
            self.tabela.SetCellValue(k,2,str(R.value))
            self.tabela.SetCellValue(k,3,str(P.value))
            self.tabela.SetCellValue(k,4,str(I.value))
            k+=1
        q.closeQuery()
    def EvtClickRH(self,event):
        #remove a seleção das outras comboboxes
        self.editReceptor.SetValue('')
        self.editDoador.SetValue('')
        self.editTipo.SetValue('')
        #limpa a tabela
        for i in range(14):
            for j in range(5):
                self.tabela.SetCellValue(i,j,'')
        #preenche a tabela
        q = Query(rh(Y,self.editRH.GetString(self.editRH.GetCurrentSelection())), tipo(Y,X), rh(Y,R), peso(Y,P), idade(Y,I), module=mod)
        k = 0
        while q.nextSolution():
            self.tabela.SetCellValue(k,0,str(Y.value))
            self.tabela.SetCellValue(k,1,str(X.value).upper())
            self.tabela.SetCellValue(k,2,str(R.value))
            self.tabela.SetCellValue(k,3,str(P.value))
            self.tabela.SetCellValue(k,4,str(I.value))
            k+=1
        q.closeQuery()
    
class TabelaCompatibilidade(wx.Panel):
    def __init__(self, parent):
        super(TabelaCompatibilidade, self).__init__(parent)

        # Create grid with 26 rows and 9 columns
        mygrid = wx.grid.Grid(self)
        mygrid.CreateGrid(8, 8)
        mygrid.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        #labels
        mygrid.SetRowLabelValue(0,"A+")
        mygrid.SetRowLabelValue(1,"A-")
        mygrid.SetRowLabelValue(2,"B+")
        mygrid.SetRowLabelValue(3,"B-")
        mygrid.SetRowLabelValue(4,"AB+")
        mygrid.SetRowLabelValue(5,"AB-")
        mygrid.SetRowLabelValue(6,"O+")
        mygrid.SetRowLabelValue(7,"O-")
        mygrid.SetColLabelValue(0,"A+")
        mygrid.SetColLabelValue(1,"A-")
        mygrid.SetColLabelValue(2,"B+")
        mygrid.SetColLabelValue(3,"B-")
        mygrid.SetColLabelValue(4,"AB+")
        mygrid.SetColLabelValue(5,"AB-")
        mygrid.SetColLabelValue(6,"O+")
        mygrid.SetColLabelValue(7,"O-")

        #Doador A+
        mygrid.SetCellValue(0,0,"✔") #Receptor A+
        mygrid.SetCellValue(0,1,"✖") #Receptor A-
        mygrid.SetCellValue(0,2,"✖") #Receptor B+
        mygrid.SetCellValue(0,3,"✖") #Receptor B-
        mygrid.SetCellValue(0,4,"✔") #Receptor AB+
        mygrid.SetCellValue(0,5,"✖") #Receptor AB-
        mygrid.SetCellValue(0,6,"✖") #Receptor O+
        mygrid.SetCellValue(0,7,"✖") #Receptor O-
        #Doador A-
        mygrid.SetCellValue(1,0,"✔") #Receptor A+
        mygrid.SetCellValue(1,1,"✔") #Receptor A-
        mygrid.SetCellValue(1,2,"✖") #Receptor B+
        mygrid.SetCellValue(1,3,"✖") #Receptor B-
        mygrid.SetCellValue(1,4,"✔") #Receptor AB+
        mygrid.SetCellValue(1,5,"✔") #Receptor AB-
        mygrid.SetCellValue(1,6,"✖") #Receptor O+
        mygrid.SetCellValue(1,7,"✖") #Receptor O-
        #Doador B+
        mygrid.SetCellValue(2,0,"✖") #Receptor A+
        mygrid.SetCellValue(2,1,"✖") #Receptor A-
        mygrid.SetCellValue(2,2,"✔") #Receptor B+
        mygrid.SetCellValue(2,3,"✖") #Receptor B-
        mygrid.SetCellValue(2,4,"✔") #Receptor AB+
        mygrid.SetCellValue(2,5,"✖") #Receptor AB-
        mygrid.SetCellValue(2,6,"✖") #Receptor O+
        mygrid.SetCellValue(2,7,"✖") #Receptor O-
        #Doador B-
        mygrid.SetCellValue(3,0,"✖") #Receptor A+
        mygrid.SetCellValue(3,1,"✖") #Receptor A-
        mygrid.SetCellValue(3,2,"✔") #Receptor B+
        mygrid.SetCellValue(3,3,"✔") #Receptor B-
        mygrid.SetCellValue(3,4,"✔") #Receptor AB+
        mygrid.SetCellValue(3,5,"✔") #Receptor AB-
        mygrid.SetCellValue(3,6,"✖") #Receptor O+
        mygrid.SetCellValue(3,7,"✖") #Receptor O-
        #Doador AB+
        mygrid.SetCellValue(4,0,"✖") #Receptor A+
        mygrid.SetCellValue(4,1,"✖") #Receptor A-
        mygrid.SetCellValue(4,2,"✖") #Receptor B+
        mygrid.SetCellValue(4,3,"✖") #Receptor B-
        mygrid.SetCellValue(4,4,"✔") #Receptor AB+
        mygrid.SetCellValue(4,5,"✖") #Receptor AB-
        mygrid.SetCellValue(4,6,"✖") #Receptor O+
        mygrid.SetCellValue(4,7,"✖") #Receptor O-
        #Doador AB-
        mygrid.SetCellValue(5,0,"✖") #Receptor A+
        mygrid.SetCellValue(5,1,"✖") #Receptor A-
        mygrid.SetCellValue(5,2,"✖") #Receptor B+
        mygrid.SetCellValue(5,3,"✖") #Receptor B-
        mygrid.SetCellValue(5,4,"✔") #Receptor AB+
        mygrid.SetCellValue(5,5,"✔") #Receptor AB-
        mygrid.SetCellValue(5,6,"✖") #Receptor O+
        mygrid.SetCellValue(5,7,"✖") #Receptor O-
        #Doador O+
        mygrid.SetCellValue(6,0,"✔") #Receptor A+
        mygrid.SetCellValue(6,1,"✖") #Receptor A-
        mygrid.SetCellValue(6,2,"✔") #Receptor B+
        mygrid.SetCellValue(6,3,"✖") #Receptor B-
        mygrid.SetCellValue(6,4,"✔") #Receptor AB+
        mygrid.SetCellValue(6,5,"✖") #Receptor AB-
        mygrid.SetCellValue(6,6,"✔") #Receptor O+
        mygrid.SetCellValue(6,7,"✖") #Receptor O-
        #Doador O-
        mygrid.SetCellValue(7,0,"✔") #Receptor A+
        mygrid.SetCellValue(7,1,"✔") #Receptor A-
        mygrid.SetCellValue(7,2,"✔") #Receptor B+
        mygrid.SetCellValue(7,3,"✔") #Receptor B-
        mygrid.SetCellValue(7,4,"✔") #Receptor AB+
        mygrid.SetCellValue(7,5,"✔") #Receptor AB-
        mygrid.SetCellValue(7,6,"✔") #Receptor O+
        mygrid.SetCellValue(7,7,"✔") #Receptor O-
        
        # Create sizer to manage the layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(mygrid, 1, wx.EXPAND)
        self.SetSizer(sizer)

class Dados(wx.Panel):
    def __init__(self, parent):
        super(Dados, self).__init__(parent)

        # Create grid with 26 rows and 9 columns
        mygrid = wx.grid.Grid(self)
        mygrid.CreateGrid(14, 5)
        mygrid.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        mygrid.SetRowLabelSize(0)

        #labels
        mygrid.SetColLabelValue(0,"Nome")
        mygrid.SetColLabelValue(1,"Tipo")
        mygrid.SetColLabelValue(2,"RH")
        mygrid.SetColLabelValue(3,"Peso")
        mygrid.SetColLabelValue(4,"Idade")

        #Nome
        q = Query(id(X,Y), module=mod)
        i = 0
        while q.nextSolution():
            mygrid.SetCellValue(i,0,str(Y.value))
            i+=1
        q.closeQuery()

        #Tipo
        q = Query(tipo(X,Y), module=mod)
        i = 0
        while q.nextSolution():
            mygrid.SetCellValue(i,1,str(Y.value).upper())
            i+=1
        q.closeQuery()

        #RH
        q = Query(rh(X,Y), module=mod)
        i = 0
        while q.nextSolution():
            mygrid.SetCellValue(i,2,str(Y.value).upper())
            i+=1
        q.closeQuery()

        #Peso
        q = Query(peso(X,Y), module=mod)
        i = 0
        while q.nextSolution():
            mygrid.SetCellValue(i,3,str(Y.value).upper())
            i+=1
        q.closeQuery()

        #Idade
        q = Query(idade(X,Y), module=mod)
        i = 0
        while q.nextSolution():
            mygrid.SetCellValue(i,4,str(Y.value).upper())
            i+=1
        q.closeQuery()
        
        # Create sizer to manage the layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(mygrid, 1, wx.EXPAND)
        self.SetSizer(sizer)

class MyApp(wx.App):
    def OnInit(self):
        # Initialize frame with a title
        self.frame = MyFrame(parent=None, title="Compatibilidade para doação de sangue")
        self.frame.Show()
        return True

# Entry point of the application
app = MyApp()
app.MainLoop()