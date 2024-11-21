from pyswip import Prolog
Prolog.consult("lista3.pl")

import wx
import wx.grid

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(800, 600))

        # Set icon for the frame
        #self.SetIcon(wx.Icon("icon.png"))

        # Initialize panel
        nb = wx.Notebook(self)
        nb.AddPage(Consulta(nb), "Consulta")
        nb.AddPage(TabelaCompatibilidade(nb), "Tabela de Compatibilidade")
        nb.AddPage(Dados(nb), "Banco de Dados")

class Dados(wx.Panel):
    def __init__(self, parent):
        super(Dados, self).__init__(parent)

        # Create grid with 26 rows and 9 columns
        mygrid = wx.grid.Grid(self)
        mygrid.CreateGrid(14, 5)
        mygrid.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        #labels
        mygrid.SetColLabelValue(0,"Nome")
        mygrid.SetColLabelValue(1,"Tipo")
        mygrid.SetColLabelValue(2,"RH")
        mygrid.SetColLabelValue(3,"Peso")
        mygrid.SetColLabelValue(4,"Idade")

        #Nome
        nomes = Prolog.query("id(X,Y)")
        mygrid.SetCellValue(0,0,str(next(nomes).get('Y')))
        mygrid.SetCellValue(1,0,str(next(nomes).get('Y')))
        mygrid.SetCellValue(2,0,str(next(nomes).get('Y')))
        mygrid.SetCellValue(3,0,str(next(nomes).get('Y')))
        mygrid.SetCellValue(4,0,str(next(nomes).get('Y')))
        mygrid.SetCellValue(5,0,str(next(nomes).get('Y')))
        mygrid.SetCellValue(6,0,str(next(nomes).get('Y')))
        mygrid.SetCellValue(7,0,str(next(nomes).get('Y')))
        mygrid.SetCellValue(8,0,str(next(nomes).get('Y')))
        mygrid.SetCellValue(9,0,str(next(nomes).get('Y')))
        mygrid.SetCellValue(10,0,str(next(nomes).get('Y')))
        mygrid.SetCellValue(11,0,str(next(nomes).get('Y')))
        mygrid.SetCellValue(12,0,str(next(nomes).get('Y')))
        mygrid.SetCellValue(13,0,str(next(nomes).get('Y')))

        #Tipo
        #tipo = Prolog.query("tiposanguineo(X,Y)")
        #mygrid.SetCellValue(0,0,str(next(tipo).get('Y')))
        #mygrid.SetCellValue(1,0,str(next(tipo).get('Y')))
        #mygrid.SetCellValue(2,0,str(next(tipo).get('Y')))
        #mygrid.SetCellValue(3,0,str(next(tipo).get('Y')))
        #mygrid.SetCellValue(4,0,str(next(tipo).get('Y')))
        #mygrid.SetCellValue(5,0,str(next(tipo).get('Y')))
        #mygrid.SetCellValue(6,0,str(next(tipo).get('Y')))
        #mygrid.SetCellValue(7,0,str(next(tipo).get('Y')))
        #mygrid.SetCellValue(8,0,str(next(tipo).get('Y')))
        #mygrid.SetCellValue(9,0,str(next(tipo).get('Y')))
        #mygrid.SetCellValue(10,0,str(next(tipo).get('Y')))
        #mygrid.SetCellValue(11,0,str(next(tipo).get('Y')))
        #mygrid.SetCellValue(12,0,str(next(tipo).get('Y')))
        #mygrid.SetCellValue(13,0,str(next(tipo).get('Y')))
        
        # Create sizer to manage the layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(mygrid, 1, wx.EXPAND)
        self.SetSizer(sizer)

class Consulta(wx.Panel):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridBagSizer(hgap=5, vgap=5)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.texto = wx.StaticText(self, label="Insira a sua con", pos=(20,30))
        grid.Add(self.texto, pos=(0,0))

        self.logger = wx.TextCtrl(self, pos=(300,20), size=(400,600), style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.button = wx.Button(self, label="Save")
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)

        self.lblname = wx.StaticText(self, label="Your name:")
        grid.Add(self.lblname, pos=(1,0))
        self.editname = wx.TextCtrl(self, value="Enter here your name", size=(140,-1))
        grid.Add(self.editname, pos=(1,1))
        self.Bind(wx.EVT_TEXT, self.EvtText, self.editname)
        self.Bind(wx.EVT_CHAR, self.EvtChar, self.editname)

        self.sampleList = ['friends', 'advertising', 'web search', 'yellow pages']
        self.lblhear = wx.StaticText(self, label="How did you hear from us?")
        grid.Add(self.lblhear,pos=(3,0))
        self.edithear = wx.ComboBox(self, size=(95, -1), choices=self.sampleList, style=wx.CB_DROPDOWN)
        grid.Add(self.edithear,pos=(3,1))
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.edithear)
        self.Bind(wx.EVT_TEXT, self.EvtText, self.edithear)

        grid.Add((10,40), pos=(2,0))

        self.insure = wx.CheckBox(self, label="Do you want Insured Shipment?")
        grid.Add(self.insure, pos=(4,0), span=(1,2), flag=wx.BOTTOM, border=5)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.insure)

        radioList = ['blue', 'red', 'yellow', 'orange', 'green', 'purple', 'navy blue', 'black', 'gray']
        rb = wx.RadioBox(self, label="What color would you like?", choices=radioList, majorDimension=3, style=wx.RA_SPECIFY_COLS)
        grid.Add(rb, pos=(5,0), span=(1,2))
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, rb)

        hSizer.Add(grid, 0, wx.ALL, 5)
        hSizer.Add(self.logger)
        mainSizer.Add(hSizer, 0, wx.ALL, 5)
        mainSizer.Add(self.button, 0, wx.CENTER)
        self.SetSizerAndFit(mainSizer)

    def EvtRadioBox(self, event):
        self.logger.AppendText('EvtRadioBox: %d\n' % event.GetInt())
    def EvtComboBox(self, event):
        self.logger.AppendText('EvtComboBox: %s\n' % event.GetString())
    def OnClick(self,event):
        self.logger.AppendText(" Click on object with Id %d\n" %event.GetId())
    def EvtText(self, event):
        self.logger.AppendText('EvtText: %s\n' % event.GetString())
    def EvtChar(self, event):
        self.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
        event.Skip()
    def EvtCheckBox(self, event):
        self.logger.AppendText('EvtCheckBox: %d\n' % event.IsChecked())

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

class MyApp(wx.App):
    def OnInit(self):
        # Initialize frame with a title
        self.frame = MyFrame(parent=None, title="Compatibilidade para doação de sangue")

        self.frame.Show()
        return True

# Entry point of the application
app = MyApp()
app.MainLoop()