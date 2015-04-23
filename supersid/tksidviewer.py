"""
tkSidViewer class implements a graphical user interface for SID based on tkinter
"""
from __future__ import print_function
import matplotlib
# matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

# handle both Python 2 and 3
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

import supersid_plot as SSP
from config import FILTERED, RAW

class tkSidViewer(tk.Frame):
    '''
    Create the Tkinter GUI
    '''
    def __init__(self, controller):
        """SuperSID Viewer using Tkinter GUI for standalone and client.
        Creation of the Frame with menu and graph display using matplotlib
        """
        matplotlib.use('TkAgg')
        self.version = "1.3.2 20150421"
        self.controller = controller  # previously referred as 'parent'
        self.tk_root = tk.Tk()
        tk.Frame.__init__(self, parent=None, background="white")
        self.tk_root.title("supersid @ " + self.controller.config['site_name'])

        # All Menus creation

        # Frame
        self.pack(fill=tk.BOTH, expand=1)

        # FigureCanvas
        self.psd_figure = Figure(facecolor='beige')
        self.canvas = FigureCanvas(self.psd_figure, self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.bind('<Configure>', self.on_resize)

        self.toolbar = NavigationToolbar2TkAgg( self.canvas, self )
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.axes = self.psd_figure.add_subplot(111)
        self.axes.hold(True)

        # StatusBar
        self.statusbar_txt = tk.StringVar()
        self.label=tk.Label(self.tk_root, bd=1, relief=tk.SUNKEN, anchor=tk.W,
                           textvariable=self.statusbar_txt,
                           font=('arial',16,'normal'))
        self.statusbar_txt.set('Initialization...')
        self.label.pack(fill=tk.X)
        self.pack()

        # Default View

    def run(self):
        self.mainloop()

    def close(self):
        self.quit()


    def clear(self):
        self.axes.cla()  # erase previous curve before drawing the new one


    def status_display(self, message, level=0, field=0):
        """update the main frame by changing the message in status bar"""
        print(message)
        self.statusbar_txt.set(message)

    def get_psd(self, data, NFFT, FS):
        """By calling 'psd' within axes, it both calculates and plots the spectrum"""
        Pxx, freqs = self.axes.psd(data, NFFT = NFFT, Fs = FS)
        return Pxx, freqs

    def on_resize(self, event):
        w,h = event.width, event.height
        #self.config(width=w, height=h)
        print(w,h)
