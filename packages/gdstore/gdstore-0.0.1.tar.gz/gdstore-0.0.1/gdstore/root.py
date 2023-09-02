# -*- coding: utf-8 -*-
from google.oauth2.service_account import Credentials
from .tree import BrowseTree


class Root(BrowseTree):
    def __init__(self, creds:Credentials, root_id:str):
        """
        Root tree of gdstore system

        Parameters
        ----------
        creds: Credentials
            Credentials from google.oauth2.service_account
            (for detail information, see https://googleapis.dev/python/google-auth/latest/user-guide.html#service-account-private-key-files)
        root_id: str
            id of root(from google drive)
        """
        super().__init__(creds, root_id, "/", root_id)

    def __str__(self) -> str:
        return f"<gdstore.root.Root of '/'>"
