<h1 align="center">
    gdstore
</h1>
<p align="center">
    simple data store using google drive
</p>
<br/>

<div align="center">
    <a href="https://github.com/oyajiDev/gdstore/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/oyajiDev/gdstore.svg" alt="MIT License" />
    </a>
    <a href="https://pypi.org/project/gdstore/">
        <img src="https://img.shields.io/pypi/v/gdstore.svg" alt="pypi" />
    </a>
</div>
<br/><br/>


## 🎛️ requirements
- python 3.9 or higher
- tested on

|        OS       | Tested | Pass |
| --------------- | ------ | ---- |
| Mac 13(Ventura) |   ✅   |  ✅  |
| Windows 10      |   🚫   |      |
| Linux(WSL)      |   🚫   |      |

<br/><br/>

## 🌐 install
### - using pip
```zsh
python -m pip install gdstore
```

### - using git(dev)
```zsh
python -m pip install git+https://github.com/oyajiDev/gdstore.git
```

<br/><br/>

## 🛠 usage
### get credentials
```python
from google.oauth2.service_account import Credentials

creds = Credentials.from_service_account_file(
    "{credential_file}"
)
```

### create root tree by id
```python
from gdstore import Root

root = Root(creds, "{google_drive_folder_id}")
```

### browse by tree
```python
# tree
tree = root.tree("/path/of/tree", "{error or create}")

# store
store = root.tree("/path/of/tree.store", "{error or create}")
```

### get, set item by tree from store
```python
# find item by tree
item = store.tree("/path/of/tree/item")
# set value to item
item.set({some value})
# get value from item
print(item.get())
```
