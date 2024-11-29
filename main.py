from pyswip import Prolog, Functor, Variable, Query, newModule, call
Prolog.consult("base_de_conhecimento.pl")

import wx
import wx.grid

'''Vari'aveis'''
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
podedoargenerico = Functor("podedoargenerico", 1)
mod = newModule("Mod1")

'''Frame principal'''
class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(800, 600))

        '''Ícone da janela'''
        self.SetIcon(wx.Icon("resources/icon.ico"))

        '''Inicializa as abas'''
        nb = wx.Notebook(self)
        nb.AddPage(Consulta(nb), "Consultar")
        nb.AddPage(TabelaCompatibilidade(nb), "Tabela de Compatibilidade")
        nb.AddPage(Dados(nb), "Banco de Dados")

'''Aba "Consultar" '''
class Consulta(wx.Panel):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)

        '''Organiza as posições dos elementos'''
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridBagSizer(hgap=5, vgap=5)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        '''Lista de todos os nomes na base de conhecimento'''
        self.nomesReceptor = [''] * 15
        '''Adiciona a opção "todos" na primeira posição da lista de nomes'''
        self.nomesReceptor[0] = 'todos'
        '''Faz a query no prolog'''
        q = Query(id(X,Y), module=mod)
        i = 1
        '''Passa os resultados para a lista de nomes'''
        while q.nextSolution():
            self.nomesReceptor[i] = str(Y.value)
            i+=1
        q.closeQuery()
        '''Lista de nomes sem a opção "todos" '''
        self.nomesDoador = self.nomesReceptor[1:]

        '''Label "Doador" '''
        self.lblDoador = wx.StaticText(self, label="Doador:")
        grid.Add(self.lblDoador,pos=(3,0))
        '''Combobox "Doador" '''
        self.editDoador = wx.ComboBox(self, size=(95, -1), choices=self.nomesDoador, style=wx.CB_DROPDOWN)
        grid.Add(self.editDoador,pos=(4,0))
        '''Botão para verificar receptores para o doador selecionado'''
        self.botaoReceptor = wx.Button(self, label="Verificar Receptor disponível")
        grid.Add(self.botaoReceptor,pos=(5,0))
        '''Função para quando apertar o botão'''
        self.Bind(wx.EVT_BUTTON, self.EvtClickReceptor, self.botaoReceptor)

        '''Label "Receptor" '''
        self.lblReceptor = wx.StaticText(self, label="Receptor:")
        grid.Add(self.lblReceptor,pos=(3,1))
        '''Combobox "Doador" '''
        self.editReceptor = wx.ComboBox(self, size=(95, -1), choices=self.nomesReceptor, style=wx.CB_DROPDOWN)
        grid.Add(self.editReceptor,pos=(4,1))
        '''Botão para verificar doadores para o receptor selecionado'''
        self.botaoDoador = wx.Button(self, label="Verificar Doador disponível")
        grid.Add(self.botaoDoador,pos=(5,1))
        '''Função para quando apertar o botão'''
        self.Bind(wx.EVT_BUTTON, self.EvtClickDoador, self.botaoDoador)

        '''Lista de tipos sanguíneos'''
        self.tipoSanguineo = ['A', 'B', 'AB', 'O']
        '''Label "Tipo Sanguíneo" '''
        self.lblTipo = wx.StaticText(self, label="Tipo Sanguíneo:")
        grid.Add(self.lblTipo,pos=(3,2))
        '''Combobox "Tipo Sanguíneo" '''
        self.editTipo = wx.ComboBox(self, size=(40, -1), choices=self.tipoSanguineo, style=wx.CB_DROPDOWN)
        grid.Add(self.editTipo,pos=(4,2))
        '''Botão para verificar pessoas com o tipo sanguíneo selecionado'''
        self.botaoTipo = wx.Button(self, label="Verificar Tipo Sanguíneo")
        grid.Add(self.botaoTipo,pos=(5,2))
        '''Função para quando apertar o botão'''
        self.Bind(wx.EVT_BUTTON, self.EvtClickTipo, self.botaoTipo)
        
        '''Lista de fatores RH'''
        self.fatorRH = ['+', '-']
        '''Label "Fator RH" '''
        self.lblRH = wx.StaticText(self, label="Fator RH:")
        grid.Add(self.lblRH,pos=(3,3))
        '''Combobox "Fator RH" '''
        self.editRH = wx.ComboBox(self, size=(40, -1), choices=self.fatorRH, style=wx.CB_DROPDOWN)
        grid.Add(self.editRH,pos=(4,3))
        '''Botão para verificar pessoas com o fator RH selecionado'''
        self.botaoRH = wx.Button(self, label="Verificar Fator RH")
        grid.Add(self.botaoRH,pos=(5,3))
        '''Função para quando apertar o botão'''
        self.Bind(wx.EVT_BUTTON, self.EvtClickRH, self.botaoRH)

        '''Criando a tabela para exibir os dados'''
        self.tabela = wx.grid.Grid(self)
        self.tabela.CreateGrid(15, 5)
        self.tabela.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.tabela.SetRowLabelSize(0)

        '''Labels das colunas da tabela'''
        self.tabela.SetColLabelValue(0,"Nome")
        self.tabela.SetColLabelValue(1,"Tipo")
        self.tabela.SetColLabelValue(2,"RH")
        self.tabela.SetColLabelValue(3,"Peso")
        self.tabela.SetColLabelValue(4,"Idade")

        grid.Add(self.tabela, pos=(6,0), span=(1,4))
        
        '''Organiza as posições dos elementos'''
        hSizer.Add(grid, 0, wx.ALIGN_CENTER, 10)
        mainSizer.Add(hSizer, 0, wx.ALIGN_CENTER, 10)
        self.SetSizerAndFit(mainSizer)

    '''Função para quando clica no botão "Verificar Receptor Disponível" '''
    def EvtClickReceptor(self,event):
        '''Remove a seleção das outras comboboxes'''
        self.editReceptor.SetValue('')
        self.editRH.SetValue('')
        self.editTipo.SetValue('')
        '''Limpa a tabela'''
        for i in range(14):
            for j in range(5):
                self.tabela.SetCellValue(i,j,'')
        '''Verifica se alguma opção foi selecionada'''
        if(self.editDoador.GetCurrentSelection() != -1 and self.editDoador.GetString(self.editDoador.GetCurrentSelection()) != ''):
            q = Query(podedoar(self.editDoador.GetString(self.editDoador.GetCurrentSelection()),Y), tipo(Y,X), rh(Y,R), peso(Y,P), idade(Y,I), module=mod)
            k = 0
            '''Preenche a tabela'''
            while q.nextSolution():
                self.tabela.SetCellValue(k,0,str(Y.value))
                self.tabela.SetCellValue(k,1,str(X.value).upper())
                self.tabela.SetCellValue(k,2,str(R.value))
                self.tabela.SetCellValue(k,3,str(P.value))
                self.tabela.SetCellValue(k,4,str(I.value))
                k+=1
            q.closeQuery()

    '''Função para quando clica no botão "Verificar Doador Disponível" '''
    def EvtClickDoador(self,event):
        '''Remove a seleção das outras comboboxes'''
        self.editDoador.SetValue('')
        self.editRH.SetValue('')
        self.editTipo.SetValue('')
        '''Limpa a tabela'''
        for i in range(14):
            for j in range(5):
                self.tabela.SetCellValue(i,j,'')
        '''Verifica se alguma opção foi selecionada'''
        if(self.editReceptor.GetCurrentSelection() != -1 and self.editReceptor.GetString(self.editReceptor.GetCurrentSelection()) != ''):
            '''Se a opção selecionada foi "todos", retorna todos os doadores disponíveis, senão retorna os doadores disponíveis para a pessoa selecionada'''
            if(self.editReceptor.GetString(self.editReceptor.GetCurrentSelection()) == 'todos'):
                q = Query(podedoargenerico(Y), tipo(Y,X), rh(Y,R), peso(Y,P), idade(Y,I), module=mod)
            else:
                q = Query(podedoar(Y,self.editReceptor.GetString(self.editReceptor.GetCurrentSelection())), tipo(Y,X), rh(Y,R), peso(Y,P), idade(Y,I), module=mod)
            k = 0
            '''Preenche a tabela'''
            while q.nextSolution():
                self.tabela.SetCellValue(k,0,str(Y.value))
                self.tabela.SetCellValue(k,1,str(X.value).upper())
                self.tabela.SetCellValue(k,2,str(R.value))
                self.tabela.SetCellValue(k,3,str(P.value))
                self.tabela.SetCellValue(k,4,str(I.value))
                k+=1
            q.closeQuery()

    '''Função para quando clica no botão "Verificar Tipo Sanguíneo" '''
    def EvtClickTipo(self, event):
        '''Remove a seleção das outras comboboxes'''
        self.editReceptor.SetValue('')
        self.editRH.SetValue('')
        self.editDoador.SetValue('')
        '''Limpa a tabela'''
        for i in range(14):
            for j in range(5):
                self.tabela.SetCellValue(i,j,'')
        '''Verifica se alguma opção foi selecionada'''
        if(self.editTipo.GetCurrentSelection() != -1 and self.editTipo.GetString(self.editTipo.GetCurrentSelection()) != ''):
            q = Query(tipo(Y,self.editTipo.GetString(self.editTipo.GetCurrentSelection()).lower()), tipo(Y,X), rh(Y,R), peso(Y,P), idade(Y,I), module=mod)
            k = 0
            '''Preenche a tabela'''
            while q.nextSolution():
                self.tabela.SetCellValue(k,0,str(Y.value))
                self.tabela.SetCellValue(k,1,str(X.value).upper())
                self.tabela.SetCellValue(k,2,str(R.value))
                self.tabela.SetCellValue(k,3,str(P.value))
                self.tabela.SetCellValue(k,4,str(I.value))
                k+=1
            q.closeQuery()

    '''Função para quando clica no botão "Verificar Fator RH" '''
    def EvtClickRH(self,event):
        '''Remove a seleção das outras comboboxes'''
        self.editReceptor.SetValue('')
        self.editDoador.SetValue('')
        self.editTipo.SetValue('')
        '''Limpa a tabela'''
        for i in range(14):
            for j in range(5):
                self.tabela.SetCellValue(i,j,'')
        '''Verifica se alguma opção foi selecionada'''
        if(self.editRH.GetCurrentSelection() != -1 and self.editRH.GetString(self.editRH.GetCurrentSelection()) != ''):
            q = Query(rh(Y,self.editRH.GetString(self.editRH.GetCurrentSelection())), tipo(Y,X), rh(Y,R), peso(Y,P), idade(Y,I), module=mod)
            k = 0
            '''Preenche a tabela'''
            while q.nextSolution():
                self.tabela.SetCellValue(k,0,str(Y.value))
                self.tabela.SetCellValue(k,1,str(X.value).upper())
                self.tabela.SetCellValue(k,2,str(R.value))
                self.tabela.SetCellValue(k,3,str(P.value))
                self.tabela.SetCellValue(k,4,str(I.value))
                k+=1
            q.closeQuery()

'''Aba "Tabela de Compatibilidade" '''
class TabelaCompatibilidade(wx.Panel):
    def __init__(self, parent):
        super(TabelaCompatibilidade, self).__init__(parent)

        '''Cria a tabela'''
        mygrid = wx.grid.Grid(self)
        mygrid.CreateGrid(8, 8)
        mygrid.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        '''Labels das linhas'''
        mygrid.SetRowLabelValue(0,"A+")
        mygrid.SetRowLabelValue(1,"A-")
        mygrid.SetRowLabelValue(2,"B+")
        mygrid.SetRowLabelValue(3,"B-")
        mygrid.SetRowLabelValue(4,"AB+")
        mygrid.SetRowLabelValue(5,"AB-")
        mygrid.SetRowLabelValue(6,"O+")
        mygrid.SetRowLabelValue(7,"O-")
        '''Labels das colunas'''
        mygrid.SetColLabelValue(0,"A+")
        mygrid.SetColLabelValue(1,"A-")
        mygrid.SetColLabelValue(2,"B+")
        mygrid.SetColLabelValue(3,"B-")
        mygrid.SetColLabelValue(4,"AB+")
        mygrid.SetColLabelValue(5,"AB-")
        mygrid.SetColLabelValue(6,"O+")
        mygrid.SetColLabelValue(7,"O-")

        '''Doador A+'''
        mygrid.SetCellValue(0,0,"✔") #Receptor A+
        mygrid.SetCellValue(0,1,"✖") #Receptor A-
        mygrid.SetCellValue(0,2,"✖") #Receptor B+
        mygrid.SetCellValue(0,3,"✖") #Receptor B-
        mygrid.SetCellValue(0,4,"✔") #Receptor AB+
        mygrid.SetCellValue(0,5,"✖") #Receptor AB-
        mygrid.SetCellValue(0,6,"✖") #Receptor O+
        mygrid.SetCellValue(0,7,"✖") #Receptor O-
        '''Doador A-'''
        mygrid.SetCellValue(1,0,"✔") #Receptor A+
        mygrid.SetCellValue(1,1,"✔") #Receptor A-
        mygrid.SetCellValue(1,2,"✖") #Receptor B+
        mygrid.SetCellValue(1,3,"✖") #Receptor B-
        mygrid.SetCellValue(1,4,"✔") #Receptor AB+
        mygrid.SetCellValue(1,5,"✔") #Receptor AB-
        mygrid.SetCellValue(1,6,"✖") #Receptor O+
        mygrid.SetCellValue(1,7,"✖") #Receptor O-
        '''#Doador B+'''
        mygrid.SetCellValue(2,0,"✖") #Receptor A+
        mygrid.SetCellValue(2,1,"✖") #Receptor A-
        mygrid.SetCellValue(2,2,"✔") #Receptor B+
        mygrid.SetCellValue(2,3,"✖") #Receptor B-
        mygrid.SetCellValue(2,4,"✔") #Receptor AB+
        mygrid.SetCellValue(2,5,"✖") #Receptor AB-
        mygrid.SetCellValue(2,6,"✖") #Receptor O+
        mygrid.SetCellValue(2,7,"✖") #Receptor O-
        '''Doador B-'''
        mygrid.SetCellValue(3,0,"✖") #Receptor A+
        mygrid.SetCellValue(3,1,"✖") #Receptor A-
        mygrid.SetCellValue(3,2,"✔") #Receptor B+
        mygrid.SetCellValue(3,3,"✔") #Receptor B-
        mygrid.SetCellValue(3,4,"✔") #Receptor AB+
        mygrid.SetCellValue(3,5,"✔") #Receptor AB-
        mygrid.SetCellValue(3,6,"✖") #Receptor O+
        mygrid.SetCellValue(3,7,"✖") #Receptor O-
        '''Doador AB+'''
        mygrid.SetCellValue(4,0,"✖") #Receptor A+
        mygrid.SetCellValue(4,1,"✖") #Receptor A-
        mygrid.SetCellValue(4,2,"✖") #Receptor B+
        mygrid.SetCellValue(4,3,"✖") #Receptor B-
        mygrid.SetCellValue(4,4,"✔") #Receptor AB+
        mygrid.SetCellValue(4,5,"✖") #Receptor AB-
        mygrid.SetCellValue(4,6,"✖") #Receptor O+
        mygrid.SetCellValue(4,7,"✖") #Receptor O-
        '''Doador AB-'''
        mygrid.SetCellValue(5,0,"✖") #Receptor A+
        mygrid.SetCellValue(5,1,"✖") #Receptor A-
        mygrid.SetCellValue(5,2,"✖") #Receptor B+
        mygrid.SetCellValue(5,3,"✖") #Receptor B-
        mygrid.SetCellValue(5,4,"✔") #Receptor AB+
        mygrid.SetCellValue(5,5,"✔") #Receptor AB-
        mygrid.SetCellValue(5,6,"✖") #Receptor O+
        mygrid.SetCellValue(5,7,"✖") #Receptor O-
        '''Doador O+'''
        mygrid.SetCellValue(6,0,"✔") #Receptor A+
        mygrid.SetCellValue(6,1,"✖") #Receptor A-
        mygrid.SetCellValue(6,2,"✔") #Receptor B+
        mygrid.SetCellValue(6,3,"✖") #Receptor B-
        mygrid.SetCellValue(6,4,"✔") #Receptor AB+
        mygrid.SetCellValue(6,5,"✖") #Receptor AB-
        mygrid.SetCellValue(6,6,"✔") #Receptor O+
        mygrid.SetCellValue(6,7,"✖") #Receptor O-
        '''Doador O-'''
        mygrid.SetCellValue(7,0,"✔") #Receptor A+
        mygrid.SetCellValue(7,1,"✔") #Receptor A-
        mygrid.SetCellValue(7,2,"✔") #Receptor B+
        mygrid.SetCellValue(7,3,"✔") #Receptor B-
        mygrid.SetCellValue(7,4,"✔") #Receptor AB+
        mygrid.SetCellValue(7,5,"✔") #Receptor AB-
        mygrid.SetCellValue(7,6,"✔") #Receptor O+
        mygrid.SetCellValue(7,7,"✔") #Receptor O-
        
        '''Organiza a posição dos elementos'''
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(mygrid, 1, wx.EXPAND)
        self.SetSizer(sizer)

'''Aba "Banco de Dados" '''
class Dados(wx.Panel):
    def __init__(self, parent):
        super(Dados, self).__init__(parent)

        '''Cria a tabela'''
        mygrid = wx.grid.Grid(self)
        mygrid.CreateGrid(14, 5)
        mygrid.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        mygrid.SetRowLabelSize(0)

        ''':abels das colunas'''
        mygrid.SetColLabelValue(0,"Nome")
        mygrid.SetColLabelValue(1,"Tipo")
        mygrid.SetColLabelValue(2,"RH")
        mygrid.SetColLabelValue(3,"Peso")
        mygrid.SetColLabelValue(4,"Idade")

        '''Busca e insere os nomes de todas as pessoas'''
        q = Query(id(X,Y), module=mod)
        i = 0
        while q.nextSolution():
            mygrid.SetCellValue(i,0,str(Y.value))
            i+=1
        q.closeQuery()

        '''Busca e insere o tipo sanguíneo de todas as pessoas'''
        q = Query(tipo(X,Y), module=mod)
        i = 0
        while q.nextSolution():
            mygrid.SetCellValue(i,1,str(Y.value).upper())
            i+=1
        q.closeQuery()

        '''Busca e insere o fator RH de todas as pessoas'''
        q = Query(rh(X,Y), module=mod)
        i = 0
        while q.nextSolution():
            mygrid.SetCellValue(i,2,str(Y.value).upper())
            i+=1
        q.closeQuery()

        '''Busca e insere o peso de todas as pessoas'''
        q = Query(peso(X,Y), module=mod)
        i = 0
        while q.nextSolution():
            mygrid.SetCellValue(i,3,str(Y.value).upper())
            i+=1
        q.closeQuery()

        '''Busca e insere a idade de todas as pessoas'''
        q = Query(idade(X,Y), module=mod)
        i = 0
        while q.nextSolution():
            mygrid.SetCellValue(i,4,str(Y.value).upper())
            i+=1
        q.closeQuery()
        
        '''Organiza a posição dos elementos'''
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(mygrid, 1, wx.EXPAND)
        self.SetSizer(sizer)

'''Inicializa a aplicação'''
class MyApp(wx.App):
    def OnInit(self):
        '''Inicializa o frame'''
        self.frame = MyFrame(parent=None, title="Compatibilidade para doação de sangue")
        self.frame.Show()
        return True

'''Inicia o programa'''
app = MyApp()
app.MainLoop()