# -*- coding: utf-8 -*-
from Game_interface import Game_interface
from Utility.Utilities import Utilities
import wx


class MyDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(MyDialog, self).__init__(parent, title=title, size=(250, 150))
        panel = wx.Panel(self)
        self.btn = wx.Button(
            panel, wx.ID_OK, label="ok", size=(50, 20), pos=(150, 150)
        )


class Gui(wx.Frame):
    input_text = ""

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="TradeGame")
        utilities = Utilities()
        self.utilities = utilities
        self.game_interface = Game_interface(utilities)

        self.run_gui()

        self.content = self.game_interface.utilities.text_package
        self.content_text.SetLabel(self.content)
        self.targeted_function = None

    def define_window(self):
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour("white")

    def set_sizers(self):
        self.editname = wx.TextCtrl(self.panel, size=(140, -1))
        self.windowSizer = wx.BoxSizer()
        self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)

        self.sizer = wx.GridBagSizer(200, 400)
        self.sizer.Add(self.quote, (0, 0))
        self.sizer.Add(self.result, (0, 1))
        self.sizer.Add(self.lblname, (1, 0))
        self.sizer.Add(self.editname, (1, 1))
        self.sizer.Add(self.button, (2, 0), (1, 2), flag=wx.EXPAND)

        self.border = wx.BoxSizer()
        self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 5)

        self.panel.SetSizerAndFit(self.border)
        self.SetSizerAndFit(self.windowSizer)

    def run_gui(self):
        self.content = None
        self.define_window()

        self.btn1 = wx.Button(self.panel, label="Travel")
        self.Bind(wx.EVT_BUTTON, self.run_function, self.btn1)
        
        self.text = wx.TextCtrl(
            self.panel, size=(250, 25), pos=(50, 50), style=wx.TE_READONLY
        )
        self.button = wx.Button(self.panel, label="Enter")

        self.lblname = wx.StaticText(self.panel, label=">:")
        self.content_text = wx.StaticText(self.panel, pos=(0, 120), label="")
        self.player_wealth_text = wx.StaticText(
            self.panel,
            -1,
            pos=(550, 20),
            label=f"አ {self.game_interface.world.player.wallet}"
        )
        self.player_wealth_text = wx.StaticText(
            self.panel,
            pos=(550, 40),
            label=f"{self.game_interface.world.player.current_town.name}"
        )
        self.quote = wx.StaticText(
            self.panel,
            pos=(0, 200),
            label="Last Action:"
        )
        self.result = wx.StaticText(self.panel, pos=(0, 200), label="")
        self.result.SetForegroundColour(wx.RED)

        self.set_sizers()
        self.button.Bind(wx.EVT_BUTTON, self.OnButton)

    def OnButton(self, e):
        self.result.SetLabel(self.editname.GetValue())
        self.utilities.text_input = self.result.LabelText
        print(self.utilities.text_input)

        self.current_context = self.game_interface.main_interface
        self.current_context()  # needs to change depending on the context
        self.content = self.game_interface.utilities.text_package
        self.content_text.SetLabel(self.content)

    def OnClick(self, e):
        dlg = wx.TextEntryDialog(self, 'Where to go?', 'Travel')

        self.text.SetValue(dlg.GetValue())
        self.input_text = dlg.GetValue()
        print(dlg.GetValue())
        if dlg.ShowModal() == wx.ID_OK:
            self.text.SetValue("Destination:"+dlg.GetValue())
        dlg.Destroy()

    def OnModal(self, event):
        dlg = wx.TextEntryDialog(self, 'Where to go?', 'Travel')

        if dlg.ShowModal() == wx.ID_OK:
            self.text.SetValue("Destination:"+dlg.GetValue())
            self.input_text = dlg.GetValue()
        dlg.Destroy()

    def run_function(self, event):
        self.OnModal(event)
        self.game_interface.world.travel(self.input_text)

    def LoadImages(self):
        self.rotunda = wx.StaticBitmap(
            self.panel,
            wx.ID_ANY,
            wx.Bitmap(
                r"C:\PythonProgrammes\TradeGame\rotunda.jpg",
                wx.BITMAP_TYPE_ANY
            )
        )


app = wx.App(False)
frame = Gui(None)
frame.Show()
app.MainLoop()
