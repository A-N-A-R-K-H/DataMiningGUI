from tkinter.ttk import Treeview
from tkinter import *
import xlrd
import pandas as pd


class PreviewDataTable:
    """
    PreviewDataTable
    show the user the head of the data that they have imported
    @methods:
    ----------
    update_table: remove column names and rows, get column names from ImportDataManager, append data to each row
    Problem: treeview is resizing to the width of the screen size, when it's told explcitly not to (stretch=False)
    """

    def __init__(self, mainframe):
        self.mainframe = mainframe
        self.treeview = Treeview(mainframe.root)
        self.treeview['columns'] = ("column 1", "column 2", "column 3", "column 4", "column 5")
        self.treeview['show'] = 'headings'  # removes empty identifier column
        for column in self.treeview['columns']:
            self.treeview.heading(column, text=str(column), anchor="w")
            self.treeview.column(column, anchor="center", width=80, stretch=False)
        for i in range(5):
            self.treeview.insert('', 'end')
            self.treeview.bind('<Button-1>', self.handle_click)

    def update_table(self, dataframe=None):
        if isinstance(dataframe, pd.DataFrame) or isinstance(self.mainframe.importExportDataManager.get_data(), pd.DataFrame):
            # delete everything from treeview
            for child in self.treeview.get_children():
                self.treeview.delete(child)
            # create columns
            self.treeview['columns'] = self.mainframe.importExportDataManager.get_column_names()
            for column in self.treeview['columns']:
                self.treeview.heading(column, text=str(column), anchor="center")
                self.treeview.column(column, anchor="center", width=80, stretch=False)

            # insert data from head of pandas dataframe
            if dataframe is None and self.mainframe.importExportDataManager.get_data() is not None:
                df = self.mainframe.importExportDataManager.get_data().copy()
            else:
                df = dataframe.copy()
            self.format_data(df)
            for i, j in df.head().iterrows():
                append_data = []
                for k in j:
                    append_data.append(k)
                self.treeview.insert('', 'end', value=append_data)

    def format_data(self, df):
        if isinstance(df, pd.DataFrame):
            for column in df.columns:
                if df[column].dtype == "float64":
                    df[column] = df[column].round(decimals=int(self.mainframe.optionsWindow.settings.get("decimal places")))

    # makes columns unresizeable
    def handle_click(self, event):
        if self.treeview.identify_region(event.x, event.y) == "separator":
            return "break"
