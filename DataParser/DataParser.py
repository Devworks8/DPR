import collections
import datetime
import os.path
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog

import pickle
import yaml

from DataParser.Calculate import Calculate


class DataParser(Calculate):
    def __init__(self):
        super().__init__()
        self.data = []
        self.saveTemplate = self.__setupSaveTemplate()
        self.fmtData = None
        self.fname = None

    def __setupSaveTemplate(self):
        """
        Create template of OrderedDict of OrderedDicts to be used by the Calculate class.
        :return: OrderedDict(OrderedDict())
        """
        hlist = ['scenes', 'pages', 'ert', 'art', 'pm', 'setups']
        slist = ['scenes', 'pages', 'ert']
        dlist = ['previous', 'todate', 'script', 'tobe', 'projected']
        headers = collections.OrderedDict()
        for key in hlist:
            headers[key] = 0
        subHeaders = collections.OrderedDict()
        for key in slist:
            subHeaders[key] = 0
        template = collections.OrderedDict()
        count = 0
        for key in dlist:
            if count < 2:
                template[key] = headers
                count += 1
            else:
                template[key] = subHeaders

        return template

    def __timeDelta(self, fields):
        deltaMap = {}

        for row in range(2, 22):

            lstItems = []
            for col in range(2, 5):
                if col == 4:
                    lstItems.append(fields[row - 2][col])
                else:
                    lstItems.append(self.fmtData[row][col])

            # Do calculation Ert - Art -> Delta
            if len(lstItems[0]) > 2 and len(lstItems[1]) > 2:
                ert = datetime.datetime.strptime(lstItems[0], '%M:%S')
                art = datetime.datetime.strptime(lstItems[1], '%M:%S')
                diff = ert - art
                delta = diff.total_seconds()
                lstItems[2].delete(0, tk.END)
                if diff < datetime.timedelta(0):
                    lstItems[2].insert(0, '-{}:{}'.format(int(-delta / 60), int(-delta % 60)))
                else:
                    lstItems[2].insert(0, '{}:{}'.format(int(delta / 60), int(delta % 60)))

                # Map the delta information using a dict of lists.
                deltaMap[row] = [ert.timetuple().tm_min * 60 + ert.timetuple().tm_sec]
                deltaMap[row].append(art.timetuple().tm_min * 60 + art.timetuple().tm_sec)
                deltaMap[row].append(int(diff.total_seconds()))

        return deltaMap

    def __pageTotal(self, data):
        """
        Calculate total pages in eighths.
        :param fields:
        :param data:
        :return: page totals
        """
        pageTotal = ""

        for row in range(2, 22):
            if len(data[row][1]) == 5:
                if pageTotal == "":
                    pageTotal = self.convert(data[row][1], reverse=True)
                # do reverse convert
                else:
                    pageTotal = self.process(pageTotal, self.convert(data[row][1], reverse=True))

            elif len(data[row][1]) == 1:
                if ' ' not in data[row][1]:
                    if pageTotal == "":
                        pageTotal = data[row][1]
                    else:
                        pageTotal = self.process(str(pageTotal), self.convert(data[row][1]))
            elif len(data[row][1]) == 3:
                if ' ' not in data[row][1]:
                    if pageTotal == "":
                        pageTotal = data[row][1]
                    else:
                        pageTotal = self.process(pageTotal, data[row][1])

        return str(pageTotal)

    def __otherTotal(self, data):
        otherTotal = [0, 0]

        for row in range(2, 22):
            if len(data[row][0]) > 0:
                otherTotal[0] = otherTotal[0] + 1

            if len(data[row][5]) > 0:
                otherTotal[1] = otherTotal[1] + int(data[row][5])

        return otherTotal

    def __deltaTotal(self, deltaMap):
        totals = []
        for value in deltaMap.values():
            if len(totals) == 0:
                totals = value
            else:
                index = 0
                for item in value:
                    totals[index] = totals[index] + item
                    index += 1

        return totals

    def __calcTotals(self, fields, data, calcdata):
        deltaTotals = self.__deltaTotal(self.__timeDelta(fields))
        pageTotals = self.__pageTotal(data)
        otherTotals = self.__otherTotal(data)
        if len(deltaTotals) == 0 or len(pageTotals) == 0 or len(otherTotals) == 0:
            pass
        else:
            totals = [otherTotals[0], pageTotals, deltaTotals[0], deltaTotals[1], deltaTotals[2], otherTotals[1]]

            # Update days totals
            index = 0
            for itm in calcdata[0]:
                itm.delete(0, tk.END)
                if index == 1:
                    # convert to mix fraction
                    if len(totals[index]) > 4:
                        itm.insert(0, self.convert(self.convert(totals[index], reverse=True)))
                    else:
                        itm.insert(0, self.convert(str(totals[index])))
                    index += 1

                elif index == 0 or index == 5:
                    itm.insert(0, totals[index])
                    index += 1

                else:
                    # format time
                    if totals[index] < 0:
                        itm.insert(0, '-{}:{}'.format(int(-totals[index] / 60), int(-totals[index] % 60)))
                    else:
                        itm.insert(0, '{}:{}'.format(int(totals[index] / 60), int(totals[index] % 60)))

                    index += 1

        """
        Projected total -> script total ert+ total delta
        """

        # Update total to date

        # Update to be shot

    def dataMap(self, gui, datamap=None, new=False):
        """
        Recursively iterate widgets and create list of field values.
        :param gui: The parent canvas widgets are located.
        :return: List of widget field values.
        """
        data = []
        index = 0
        for f in gui.winfo_children():
            if isinstance(f, tk.Frame) or isinstance(f, tk.LabelFrame):
                for w in f.winfo_children():
                    if isinstance(w, tk.Frame) or isinstance(w, tk.LabelFrame):
                        for e in w.winfo_children():
                            if isinstance(e, tk.Entry):
                                if datamap is None and new is False:
                                    data.append(e.get())
                                else:
                                    if new is False:
                                        e.insert(0, datamap[index])
                                        index += 1
                                    else:
                                        e.delete(0, tk.END)
                            elif isinstance(e, tk.Text):
                                if datamap is None and new is False:
                                    data.append(e.get("1.0", tk.END))
                                else:
                                    if new is False:
                                        e.insert("1.0", datamap[index])
                                        index += 1
                                    else:
                                        e.delete("1.0", tk.END)
                    elif isinstance(w, tk.Entry):
                        if datamap is None and new is False:
                            data.append(w.get())
                        else:
                            if new is False:
                                w.insert(0, datamap[index])
                                index += 1
                            else:
                                w.delete(0, tk.END)
                    elif isinstance(w, tk.Text):
                        if datamap is None and new is False:
                            data.append(w.get("1.0", tk.END))
                        else:
                            if new is False:
                                w.insert("1.0", datamap[index])
                                index += 1
                            else:
                                w.delete("1.0", tk.END)

        return data

    def update(self, gui, fields, calcdata,  data):
        self.fmtData = self.formatData(data.dataMap(gui), self.saveTemplate)
        """
                fmtData index key: 0 = title
                                   1 = 
                                   2 = daily entries
                                   3 = 
                                   4 = OrderedDict
                                   5 = comments
        """
        if self.fmtData is not None and len(self.fmtData) > 1:
            if len(self.fmtData[0][0]) > 0: #TODO: REplace with checkbox value
                self.__calcTotals(fields, self.fmtData, calcdata)

                # print(fmtData[4]['previous']['scenes'])
            else:
                # Disable automatic calculations.
                pass

    def load(self, root, gui, settings=None, project=False):
        if project is False:
            filename = filedialog.askopenfilename(initialdir=settings.psettings['path']+'/Reports',
                                                  title="Open Report")
            if filename is not '':
                lfile = open(filename, 'rb')
                self.data = pickle.load(lfile)
                lfile.close()
                self.dataMap(gui, new=True)
                self.dataMap(gui, self.data)
                root.title(settings.psettings['title'] + '.dpro' + ' - ' + os.path.split(filename)[1])
        elif project is True:

            filename = filedialog.askopenfilename(initialdir=settings.settings['path'],
                                                  title="Open Project")
            if filename is not '':
                self.fname = filename
                stream = open(filename, 'r')
                settings.psettings = yaml.load(stream)
                self.dataMap(gui, new=True)
                root.title(os.path.split(filename)[1])

    def export(self, file=None):
        if file and os.path.exists(file):
            #self.data = opxl.load_workbook(file)
            pass
        else:
            #TODO: Display Message window
            pass

    def save(self, gui, root, spath=None, datamap=None, template=None, settings=None, saveas=True):
        path = spath+'/Reports'
        if not os.path.exists(path):
            os.makedirs(path)
        p, d, files = next(os.walk(path))
        day = str(len(files)+1)

        if saveas or '.p' not in root.title():
            filename = filedialog.asksaveasfilename(initialdir=path, defaultextension='p', initialfile='Day'+day,
                                                    title="Save As")

            if filename is not '':
                settings['history'].append(os.path.split(filename)[1])
                root.title(datamap[0] + '.dpro' + ' - ' + settings['history'][-1])
                self.fname = filename

        datamap = self.dataMap(gui)

        for index in range(6):
            settings['previous'][index] = datamap[142+index]

        stream = open(spath + datamap[0] + '.dpro', 'w')
        yaml.dump(settings, stream)
        stream.close()
        sfile = open(self.fname, 'wb')
        pickle.dump(datamap, sfile)
        sfile.close()

    def newProject(self, root, gui, settings, data):
        title = simpledialog.askstring("New Project", "Project name", parent=gui)
        # Create project directories
        path = settings.settings['path']
        os.makedirs(path+title)
        os.makedirs(path+title+'/Reports')
        # Create project file
        settings.setup(path=path, title=title)
        data.dataMap(gui, new=True)
        root.title(title+'.dpro')