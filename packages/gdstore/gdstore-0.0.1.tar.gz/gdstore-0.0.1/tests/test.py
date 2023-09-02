# -*- coding: utf-8 -*-
import pathlib
from google.oauth2.service_account import Credentials
from gdstore import Root
from gdstore.tree import StoreTree

if __name__ == "__main__":
    root_dir = pathlib.Path(__file__).absolute().parent
    creds = Credentials.from_service_account_file(
        root_dir.joinpath("credentials.json").as_posix()
    )

    root = Root(creds, "1MdItZhJ6xN8Loc7tlYTLEllmMcTg0HIY")
    print(root)

    tree = root.tree("/test/test1/test2/test3/test4", "create")
    print(tree)

    store:StoreTree = tree.tree("test5.store", "create")
    print(store)

    val = store.tree("/test6/test7")
    val.set("12341234")
    print(val.get())

    store.delete()

    # store = tree.store("test5")
    # group = store["test6"]
    # print(store.groups())

    # val1 = group["val1"]
    # print(group.items())
    # val1.set("1234")
    # print(val1, val1.get())
    # val1.delete()
