# -*- coding: utf-8 -*-
import gspread, tqdm, unix_os
from typing import List, Literal, Union
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from .store import Store


class BrowseTree:
    def __init__(self, creds:Credentials, tree_id:str, tree:str, root_id:str):
        """
        Tree to browse GoogleDrive with tree path.

        Parameters
        ----------
        creds: Credentials
            Credentials from google.oauth2.service_account
            (for detail information, see https://googleapis.dev/python/google-auth/latest/user-guide.html#service-account-private-key-files)
        tree_id: str
            id of tree(from google drive)
        tree: str
            tree path of current Tree
        root_id: str
            id of root to search tree path
        """
        if not tree.startswith("/"):
            raise ValueError("tree must starts with `/`!")

        if not creds.has_scopes("https://www.googleapis.com/auth/drive"):
            creds = creds.with_scopes([ "https://www.googleapis.com/auth/drive" ])

        self.__gdrive = build("drive", "v3", credentials = creds)
        self.__creds, self.__tree_id, self.__tree, self.__root_id =\
            creds, tree_id, tree, root_id

    def __str__(self) -> str:
        return f"<gdstore.tree.BrowseTree of '{self.current_tree}'>"


    def __parse_tree(self, tree:str) -> List[str]:
        return [
            item
            for item in tree.split("/")
            if not item == ""
        ]
    
    def __check_tree_exists(self, tree:str, mode:Literal["absolute", "relative"], use_tqdm:bool = True) -> bool:
        trees = self.__parse_tree(tree)
        root = self.__root_id if mode == "absolute" else self.__tree_id
        if use_tqdm:
            trees = tqdm.tqdm(self.__parse_tree(tree), "checking tree ")

        for idx, name in enumerate(trees):
            if idx == len(trees) - 1:
                if name.lower().endswith(".store"):
                    name = name.replace(".store", "")

            files = []
            page_token = None

            while True:
                resp = self.__gdrive.files().list(
                    q = f"'{root}' in parents and trashed = false",
                    fields = "nextPageToken, files(id, name)"
                ).execute()
                files.extend(resp.get("files", []))
                page_token = resp.get("nextPageToken", None)

                if page_token is None:
                    break

            exists = False
            for info in files:
                if info["name"] == name:
                    root = info["id"]
                    exists = True
                    break

            if not exists:
                if use_tqdm:
                    trees.clear()
                    trees.set_description("failed!")

                return False

        return True
    
    def __check_tree_type(self, tree_id:str) -> Literal["browse", "store", "unknown"]:
        resp = self.__gdrive.files().get(fileId = tree_id).execute()
        if resp["mimeType"] == "application/vnd.google-apps.folder":
            return "browse"
        elif resp["mimeType"] == "application/vnd.google-apps.spreadsheet":
            return "store"
        else:
            return "unknown"
    
    def __make_tree(self, tree:str, mode:Literal["absolute", "relative"]):
        trees = tqdm.tqdm(self.__parse_tree(tree), "creating tree ")
        root = self.__root_id if mode == "absolute" else self.__tree_id

        for idx, name in enumerate(trees):
            is_store = False
            if idx == len(trees) - 1:
                if name.lower().endswith(".store"):
                    name = name.replace(".store", "")
                    is_store = True

            files = []
            page_token = None

            while True:
                resp = self.__gdrive.files().list(
                    q = f"'{root}' in parents and trashed = false",
                    fields = "nextPageToken, files(id, name)"
                ).execute()
                files.extend(resp.get("files", []))
                page_token = resp.get("nextPageToken", None)

                if page_token is None:
                    break

            exists = False
            for info in files:
                if info["name"] == name:
                    root = info["id"]
                    exists = True
                    break

            if not exists:
                if is_store:
                    self.__gdrive.files().create(
                        body = {
                            "name": name,
                            "mimeType": "application/vnd.google-apps.spreadsheet",
                            "parents": [ root ]
                        },
                        fields = "id"
                    ).execute()
                else:
                    root = self.__gdrive.files().create(
                        body = {
                            "name": name,
                            "mimeType": "application/vnd.google-apps.folder",
                            "parents": [ root ]
                        },
                        fields = "id"
                    ).execute()["id"]

            if idx == len(trees) - 1:
                trees.clear()
                trees.set_description("finished!")
    
    def __get_tree_id(self, tree:str, mode:Literal["absolute", "relative"]) -> str:
        trees = self.__parse_tree(tree)
        root = self.__root_id if mode == "absolute" else self.__tree_id

        for idx, name in enumerate(trees):
            if idx == len(trees) - 1:
                if name.lower().endswith(".store"):
                    name = name.replace(".store", "")

            files = []
            page_token = None

            while True:
                resp = self.__gdrive.files().list(
                    q = f"'{root}' in parents and trashed = false",
                    fields = "nextPageToken, files(id, name)"
                ).execute()
                files.extend(resp.get("files", []))
                page_token = resp.get("nextPageToken", None)

                if page_token is None:
                    break

            for info in files:
                if info["name"] == name:
                    root = info["id"]
                    break

        return root


    @property
    def current_tree(self) -> str:
        return self.__tree

    def tree(self, tree:str, if_not_exists:Literal["error", "create"] = "error") -> Union["BrowseTree", "StoreTree"]:
        """
        Function to browse on google drive system

        Parameters
        ----------
        tree: str
            tree path to browse
            - absolute tree, starts with "/"
            - relative tree, not starts with "/"
            - if ends with ".store", use as store

        if_not_exists: Literal["error", "create"]
            next job for if tree not exists
            - if "error", raise error
            - if "create", create unexist tree
        """

        if tree.startswith("/"): # absolute tree
            absolute_tree = tree
        else:
            absolute_tree = unix_os.path.realpath(unix_os.path.join(self.current_tree, tree))

        if not self.__check_tree_exists(tree, "absolute" if tree.startswith("/") else "relative"):
            if if_not_exists == "error":
                raise ValueError("invalid tree!")
            else:
                self.__make_tree(tree, "absolute" if tree.startswith("/") else "relative")

        new_tree_id = self.__get_tree_id(tree, "absolute" if tree.startswith("/") else "relative")
        tree_type = self.__check_tree_type(new_tree_id)
        if tree_type == "browse":
            return BrowseTree(
                self.__creds,
                new_tree_id,
                absolute_tree, self.__root_id
            )
        elif tree_type == "store":
            return StoreTree(
                self.__gdrive, self.__creds, new_tree_id, absolute_tree
            )
        else:
            raise ValueError("unsupported item type!")
        
    def delete(self):
        """
        Function to delete current tree
        """
        self.__gdrive.files().delete(
            fileId = self.__tree_id
        ).execute()
        self.__gdrive.files().emptyTrash().execute()

class StoreTree:
    def __init__(self, gdrive, creds:Credentials, spread_id:str, tree:str):
        """
        StoreCollection from Google Spread

        Parameters
        ----------
        gdrive: Any
            Google Drive from credentials
        creds: Credentials
            Credentials from google.oauth2.service_account
            (for detail information, see https://googleapis.dev/python/google-auth/latest/user-guide.html#service-account-private-key-files)
        spread_id: str
            id of Google Spread
        tree: str
            tree path of current Tree
        """
        self.__gdrive = gdrive
        self.__client = gc = gspread.authorize(creds)
        self.__spread = spread = gc.open_by_key(spread_id)
        self.__sheet = sheet = spread.worksheets(True)[0]
        self.__tree = tree

        sheet.update_title("trees")
        sheet.resize(1, 2)
        sheet.update_cell(1, 1, "TREE")
        sheet.update_cell(1, 2, "VALUE")

    def __str__(self) -> str:
        return f"<gdstore.tree.StoreTree of '{self.current_tree}'>"
    

    @property
    def current_tree(self) -> str:
        return self.__tree

    def tree(self, tree:str) -> Store:
        """
        Function to get item of tree

        Parameters
        ----------
        tree: str
            tree path to get

        Return
        ------
        store: Store
            store searched
        """
        if not tree.startswith("/"):
            raise ValueError("tree must starts with `/`!")

        item_names = [ row[0] for row in self.__sheet.get_all_values()[1:] ]
        if tree in item_names:
            ridx = item_names.index(tree) + 2
        else:
            ridx = len(item_names) + 2
            self.__sheet.resize(self.__sheet.row_count + 1)
            self.__sheet.update_cell(ridx, 1, tree)

        return Store(self.__sheet, ridx)
    
    def delete(self):
        """
        Function to delete store tree
        """
        self.__client.del_spreadsheet(self.__spread.id)
        self.__gdrive.files().emptyTrash().execute()
