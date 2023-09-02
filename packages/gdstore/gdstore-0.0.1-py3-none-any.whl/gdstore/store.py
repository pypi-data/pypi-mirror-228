# -*- coding: utf-8 -*-
import gspread, codecs, pickle
from typing import Any


class Store:
    def __init__(self, sheet:gspread.Worksheet, ridx:int):
        """
        StoreItem from Google Spread Worksheet

        Parameters
        ----------
        sheet: gspread.Worksheet
            gspread worksheet from Google Spread Worksheet
        ridx: int
            row index of current StoreItem
        """
        self.__sheet, self.__ridx = sheet, ridx

    def __str__(self) -> str:
        return f"<gdstore.store.StoreItem '{self.name}' of '{self.__sheet.title}'>"

    @property
    def name(self) -> str:
        """
        Name of item
        """
        return self.__sheet.cell(self.__ridx, 1).value
    
    def get(self) -> Any:
        """
        Function to get value from cell(load by pickle)
        """
        return pickle.loads(codecs.decode(self.__sheet.cell(self.__ridx, 2).value.encode(), "base64"))
    
    def set(self, value:Any):
        """
        Function to set value on cell(dump by pickle)
        """
        self.__sheet.update_cell(self.__ridx, 2, codecs.encode(pickle.dumps(value), "base64").decode())

    def delete(self):
        """
        Function to delete item
        """
        self.__sheet.delete_row(self.__ridx)
