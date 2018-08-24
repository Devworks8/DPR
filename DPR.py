# Name: DPR.py
# Version: 0.5.3
# Date Created: 12/09/2017
# Description: Daily Progress Report.

import os.path
import tkinter as tk

import yaml

from DataParser.DataParser import DataParser

UPDATE_RATE = 1000


# Settings handler
class ConfigParser:
    def __init__(self):
        self.defaults = \
"""
font: [Courier, 10]
history: []
path: ./Projects/
title: "" 
previous: [0, 0, 0, 0, 0, 0]
"""
        self.settings = self.__loadSettings()
        self.psettings = self.settings

    def __loadSettings(self, project=False, path=None, title=None):
        """
        If settings.yaml exist, load settings, otherwise, create settings file and load defaults
        :return: Dict of settings
        """
        if project is False:
            if os.path.exists("./Data/settings.yaml"):
                with open("./Data/settings.yaml") as settings:
                    return yaml.load(settings)
            else:
                stream = open('./Data/settings.yaml', 'w')
                yaml.dump(yaml.load(self.defaults), stream)
                return yaml.load(self.defaults)
        elif project is True:
            self.psettings = self.__loadSettings()
            self.psettings['name'] = title
            self.psettings['path'] = path+title+'/'
            stream = open(self.psettings['path']+title+'.dpro', 'w')
            yaml.dump(self.psettings, stream)
            stream.close()

    def setup(self, path=None, title=None):
        self.__loadSettings(project=True, path=path, title=title)


# GUI Class
class Gui:
    def __init__(self, master):
        self.master = master
        self.config = ConfigParser()
        self.gui = None
        self.fields = []
        self.calcData = []
        self.create(master)
        self.data = DataParser()
        self.updater()

    def updater(self):
        self.__calculate(self.gui, self.fields, self.calcData, self.data)
        self.master.after(UPDATE_RATE, self.updater)

    def __calculate(self, gui, fields, calcdata, data):
        data.update(gui, fields, calcdata, data)

    def bringtoFront(self, root):
        root.attributes("-topmost", True)
        root.focus_force()

    def create(self, root):
        """
        Declare and position all widgets.
        :return: None
        """
        frame = VerticalScrolledFrame(root)
        frame.pack()
        self.gui = frame.interior
        """
        Create Menu
        """
        menuBar = tk.Menu(root)
        fileMenu = tk.Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="New Project", command=lambda: self.data.newProject(self.master,
                                                                                       frame.interior,
                                                                                       self.config,
                                                                                       self.data))
        fileMenu.add_command(label="Open Project", command=lambda: self.data.load(self.master, frame.interior,
                                                                                  settings=self.config,
                                                                                  project=True))
        fileMenu.add_command(label="Close Project", command=None)
        fileMenu.add_separator()
        fileMenu.add_command(label="New", command=lambda: self.data.dataMap(frame.interior, new=True))
        fileMenu.add_command(label="Open", command=lambda: self.data.load(self.master,
                                                                          frame.interior,
                                                                          self.config))
        fileMenu.add_command(label="Close", command=lambda: self.data.dataMap(frame.interior, new=True))
        fileMenu.add_separator()
        fileMenu.add_command(label="Print", command=None)
        fileMenu.add_separator()
        fileMenu.add_command(label="Save", command=lambda: self.data.save(self.gui,
                                                                          self.master,
                                                                          self.config.psettings['path'],
                                                                          self.data.dataMap(frame.interior),
                                                                          self.fields,
                                                                          self.config.psettings, saveas=False))

        fileMenu.add_command(label="Save As", command=lambda: self.data.save(self.gui,
                                                                             self.master,
                                                                             self.config.psettings['path'],
                                                                             self.data.dataMap(frame.interior),
                                                                             self.fields,
                                                                             self.config.psettings))
        fileMenu.add_separator()
        fileMenu.add_command(label="Quit", command=root.quit)
        menuBar.add_cascade(label="File", menu=fileMenu)

        exportMenu = tk.Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label='Export', menu=exportMenu)

        settingsMenu = tk.Menu(menuBar, tearoff=0)
        settingsMenu.add_command(label='Project', command=None)
        settingsMenu.add_separator()
        settingsMenu.add_command(label='System', command=None)
        menuBar.add_cascade(label='Settings', menu=settingsMenu)

        root.config(menu=menuBar)

        """
        Create Status Bar
        """
        statusBar = tk.Label(root, text="Ready", bd=3, relief=tk.RIDGE)
        statusBar.pack(side=tk.BOTTOM, fill=tk.X, expand=tk.TRUE)

        """
        First Section: Contains Header and Production Title.
        """
        frame1 = tk.Frame(frame.interior, padx=10, pady=10)
        frame1.pack()
        """
        Header
        """
        header = tk.Label(frame1, text="Script Supervisor Report")
        header.grid(row=0, columnspan=4)
        """
        Production Title
        """
        lblTitle = tk.Label(frame1, text="Title: ")
        entTitle = tk.Entry(frame1, width=49)
        lblTitle.grid(row=2, sticky=tk.E)
        entTitle.grid(row=2, column=1)

        """
        Second Section: Call Time, Meal Breaks, etc...
        """
        frame2 = tk.Frame(frame.interior)
        frame2.pack()
        """
        Declare widgets
        """
        lblDate = tk.Label(frame2, text="Date: ")
        entDate = tk.Entry(frame2)
        lblShoot = tk.Label(frame2, text="Shoot Day: ")
        entShoot = tk.Entry(frame2)
        lblCall = tk.Label(frame2, text="Call Time: ")
        entCall = tk.Entry(frame2)
        lblFirstAM = tk.Label(frame2, text="1st Shot AM: ")
        entFirstAM = tk.Entry(frame2)
        lblMeal1 = tk.Label(frame2, text="Meal Break: ")
        entMeal1 = tk.Entry(frame2)
        lblFirstPM = tk.Label(frame2, text="1st Shot PM: ")
        entFirstPM = tk.Entry(frame2)
        lblMeal2 = tk.Label(frame2, text="2nd Meal Break: ")
        entMeal2 = tk.Entry(frame2)
        lblWrap = tk.Label(frame2, text="Wrap: ")
        entWrap = tk.Entry(frame2)
        """
        Place widgets on grid
        """
        lblDate.grid(row=0, sticky=tk.E)
        entDate.grid(row=0, column=1, columnspan=2)
        lblShoot.grid(row=1, sticky=tk.E)
        entShoot.grid(row=1, column=1, columnspan=2)
        lblCall.grid(row=2, sticky=tk.E)
        entCall.grid(row=2, column=1, columnspan=2)
        lblFirstAM.grid(row=3, sticky=tk.E)
        entFirstAM.grid(row=3, column=1, columnspan=2)
        lblMeal1.grid(row=0, column=3, sticky=tk.E)
        entMeal1.grid(row=0, column=4, columnspan=2)
        lblFirstPM.grid(row=1, column=3, sticky=tk.E)
        entFirstPM.grid(row=1, column=4, columnspan=2)
        lblMeal2.grid(row=2, column=3, sticky=tk.E)
        entMeal2.grid(row=2, column=4, columnspan=2)
        lblWrap.grid(row=3, column=3, sticky=tk.E)
        entWrap.grid(row=3, column=4, columnspan=2)

        """
        Third Section: Entries for the day
        """
        frame3 = tk.Frame(frame.interior)
        frame3.pack()
        """
        Declare widgets
        """
        lblEntScenes = tk.Label(frame3, text="Scene")
        lblEntPages = tk.Label(frame3, text="Pages")
        lblEntErt = tk.Label(frame3, text="ERT")
        lblEntArt = tk.Label(frame3, text="ART")
        lblEntDelta = tk.Label(frame3, text="+/-")
        lblEntSetups = tk.Label(frame3, text="Setups")
        """
        Place widgets on grid
        """
        lblEntScenes.grid(row=0, column=0)
        lblEntPages.grid(row=0, column=1)
        lblEntErt.grid(row=0, column=2)
        lblEntArt.grid(row=0, column=3)
        lblEntDelta.grid(row=0, column=4)
        lblEntSetups.grid(row=0, column=5)
        height = 20
        width = 6
        for i in range(height):  # Rows
            for j in range(width):  # Columns
                b = tk.Entry(frame3, width=6)
                b.config(justify=tk.CENTER)
                b.grid(row=i + 1, column=j)
                # Create a nested list of lists containing 6 objects each representing a row of data.
                if len(self.fields) == 0:
                    self.fields.append([b])
                elif len(self.fields) > 0:
                    if len(self.fields[len(self.fields) - 1]) % 6 == 0:
                        self.fields.append([b])
                    else:
                        self.fields[len(self.fields)-1].append(b)

        """
        Fourth Section:
        """
        frame4 = tk.Frame(frame.interior)
        frame4.pack()
        """
        Declare widgets
        """
        subframe1 = tk.LabelFrame(frame4, text="Scenes Scheduled")
        subframe1.pack()
        txtScheduled = tk.Text(subframe1, height=2, bd=0, highlightthickness=0)
        txtScheduled.pack()
        subframe2 = tk.LabelFrame(frame4, text="Scenes Completed")
        subframe2.pack()
        txtCompleted = tk.Text(subframe2, height=2, bd=0, highlightthickness=0)
        txtCompleted.pack()
        subframe3 = tk.LabelFrame(frame4, text="Part Scenes Completed")
        subframe3.pack()
        txtPart = tk.Text(subframe3, height=2, bd=0, highlightthickness=0)
        txtPart.pack()
        subframe4 = tk.LabelFrame(frame4, text="Wild Tracks")
        subframe4.pack()
        txtWild = tk.Text(subframe4, height=2, bd=0, highlightthickness=0)
        txtWild.pack()
        subframe6 = tk.LabelFrame(frame4, text="Camera Rolls")
        subframe6.pack()
        txtCam = tk.Text(subframe6, height=2, bd=0, highlightthickness=0)
        txtCam.pack()
        subframe7 = tk.LabelFrame(frame4, text="Sound Rolls")
        subframe7.pack()
        txtSnd = tk.Text(subframe7, height=2, bd=0, highlightthickness=0)
        txtSnd.pack()
        subframe8 = tk.LabelFrame(frame4, text="Slates")
        subframe8.pack()
        txtSlates = tk.Text(subframe8, height=2, bd=0, highlightthickness=0)
        txtSlates.pack()

        """
        Fifth Section:
        """
        frame5 = tk.Frame(frame.interior)
        frame5.pack()
        """
        Define Widgets
        """
        lblScenes = tk.Label(frame5, text="Scenes")
        lblPages = tk.Label(frame5, text="Pages")
        lblErt = tk.Label(frame5, text="ERT")
        lblArt = tk.Label(frame5, text="ART")
        lblDelta = tk.Label(frame5, text="+/-")
        lblSetups = tk.Label(frame5, text="Setups")
        lblToday = tk.Label(frame5, text="Shot Today")
        entTodayScenes = tk.Entry(frame5, width=6)
        entTodayScenes.config(justify=tk.CENTER)
        entTodayPages = tk.Entry(frame5, width=6)
        entTodayPages.config(justify=tk.CENTER)
        entTodayErt = tk.Entry(frame5, width=6)
        entTodayErt.config(justify=tk.CENTER)
        entTodayArt = tk.Entry(frame5, width=6)
        entTodayArt.config(justify=tk.CENTER)
        entTodayDelta = tk.Entry(frame5, width=6)
        entTodayDelta.config(justify=tk.CENTER)
        entTodaySetups = tk.Entry(frame5, width=6)
        entTodaySetups.config(justify=tk.CENTER)
        self.calcData.append([entTodayScenes, entTodayPages, entTodayErt, entTodayArt, entTodayDelta, entTodaySetups])

        lblPrev = tk.Label(frame5, text="Shot Previous")
        entPrevScenes = tk.Entry(frame5, width=6)
        entPrevScenes.config(justify=tk.CENTER)
        entPrevPages = tk.Entry(frame5, width=6)
        entPrevPages.config(justify=tk.CENTER)
        entPrevErt = tk.Entry(frame5, width=6)
        entPrevErt.config(justify=tk.CENTER)
        entPrevArt = tk.Entry(frame5, width=6)
        entPrevArt.config(justify=tk.CENTER)
        entPrevDelta = tk.Entry(frame5, width=6)
        entPrevDelta.config(justify=tk.CENTER)
        entPrevSetups = tk.Entry(frame5, width=6)
        entPrevSetups.config(justify=tk.CENTER)
        self.calcData.append([entPrevScenes, entPrevPages, entPrevErt, entPrevArt, entPrevDelta, entPrevSetups])

        lblTotal = tk.Label(frame5, text="Total to Date")
        entTotalScenes = tk.Entry(frame5, width=6)
        entTotalScenes.config(justify=tk.CENTER)
        entTotalPages = tk.Entry(frame5, width=6)
        entTotalPages.config(justify=tk.CENTER)
        entTotalErt = tk.Entry(frame5, width=6)
        entTotalErt.config(justify=tk.CENTER)
        entTotalArt = tk.Entry(frame5, width=6)
        entTotalArt.config(justify=tk.CENTER)
        entTotalDelta = tk.Entry(frame5, width=6)
        entTotalDelta.config(justify=tk.CENTER)
        entTotalSetups = tk.Entry(frame5, width=6)
        entTotalSetups.config(justify=tk.CENTER)
        self.calcData.append([entTotalScenes, entTotalPages, entTotalErt, entTotalArt, entTotalDelta, entTotalSetups])

        lblScriptTtl = tk.Label(frame5, text="Script Total")
        entScriptTtlScenes = tk.Entry(frame5, width=6)
        entScriptTtlScenes.config(justify=tk.CENTER)
        entScriptTtlPages = tk.Entry(frame5, width=6)
        entScriptTtlPages.config(justify=tk.CENTER)
        entScriptTtlErt = tk.Entry(frame5, width=6)
        entScriptTtlErt.config(justify=tk.CENTER)
        self.calcData.append([entScriptTtlScenes, entScriptTtlPages, entScriptTtlErt])

        lblToBe = tk.Label(frame5, text="To be Shot")
        entToBeScenes = tk.Entry(frame5, width=6)
        entToBeScenes.config(justify=tk.CENTER)
        entToBePages = tk.Entry(frame5, width=6)
        entToBePages.config(justify=tk.CENTER)
        entToBeErt = tk.Entry(frame5, width=6)
        entToBeErt.config(justify=tk.CENTER)
        self.calcData.append([entToBeScenes, entToBePages, entToBeErt])

        lblTtlRun = tk.Label(frame5, text="Projected Total Running Time: ")
        entTtlRun = tk.Entry(frame5, width=6)
        entTtlRun.config(justify=tk.CENTER)
        """
        Place widgets on grid
        """
        lblScenes.grid(row=0, column=1)
        lblPages.grid(row=0, column=2)
        lblErt.grid(row=0, column=3)
        lblArt.grid(row=0, column=4)
        lblDelta.grid(row=0, column=5)
        lblSetups.grid(row=0, column=6)
        lblToday.grid(row=1, sticky=tk.E)
        entTodayScenes.grid(row=1, column=1)
        entTodayPages.grid(row=1, column=2)
        entTodayErt.grid(row=1, column=3)
        entTodayArt.grid(row=1, column=4)
        entTodayDelta.grid(row=1, column=5)
        entTodaySetups.grid(row=1, column=6)
        lblPrev.grid(row=2, column=0, sticky=tk.E)
        entPrevScenes.grid(row=2, column=1)
        entPrevPages.grid(row=2, column=2)
        entPrevErt.grid(row=2, column=3)
        entPrevArt.grid(row=2, column=4)
        entPrevDelta.grid(row=2, column=5)
        entPrevSetups.grid(row=2, column=6)
        lblTotal.grid(row=3, column=0, sticky=tk.E)
        entTotalScenes.grid(row=3, column=1)
        entTotalPages.grid(row=3, column=2)
        entTotalErt.grid(row=3, column=3)
        entTotalArt.grid(row=3, column=4)
        entTotalDelta.grid(row=3, column=5)
        entTotalSetups.grid(row=3, column=6)
        lblScriptTtl.grid(row=4, column=0, sticky=tk.E)
        entScriptTtlScenes.grid(row=4, column=1)
        entScriptTtlPages.grid(row=4, column=2)
        entScriptTtlErt.grid(row=4, column=3)
        lblToBe.grid(row=5, column=0, sticky=tk.E)
        entToBeScenes.grid(row=5, column=1)
        entToBePages.grid(row=5, column=2)
        entToBeErt.grid(row=5, column=3)
        lblTtlRun.grid(row=6, column=0, columnspan=3, sticky=tk.E)
        entTtlRun.grid(row=6, column=3)

        """
        Sixth Section: Contains Remarks Field
        """
        frame6 = tk.LabelFrame(frame.interior, text="Remarks", padx=10, pady=5)
        frame6.pack()
        entRemarks = tk.Text(frame6, height=5, wrap=tk.WORD, bd=0, highlightthickness=0)
        entRemarks.pack()
        self.gui = frame.interior

        #self.bringtoFront(root=root)


# GUI window scroll implementation
class VerticalScrolledFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    * Code fetched from https://gist.github.com/EugeneBakin/76c8f9bcec5b390e45df
    """
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, scrollregion=(0, 0, 800, 600), width=800, height=600, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

        def _on_mousewheel(event):
            canvas.yview_scroll(-1 * event.delta, 'units')

        #canvas.bind_all('<MouseWheel>', _on_mousewheel)


if __name__ == '__main__':
    # Parent Class
    class Dpr:
        def __init__(self, master):
            self.gui = Gui(master)


    master = tk.Tk()
    master.title('Untitled')
    _ = Dpr(master)
    master.mainloop()

