import json
import pathlib
import json
import importlib


class export:

    def __init__(self, file: pathlib.Path):
        self.file = file
        self.items = []

    def add(self, exportObject, name: str):
        otype = type(exportObject)
        try:
            info = exportObject.__export__()
        except AttributeError:
            info = str(exportObject)
        self.items.append({
            "name": name,
            "class_": str(exportObject.__class__.__name__),
            "module": str(exportObject.__class__.__module__),
            "information": info
        })

    def export_as_file(self):
        items = {}
        for object in self.items:
            name = object["name"]
            module = object["module"]
            information = object["information"]
            class_ = object["class_"]
            items[name] = {
                "class_": class_,
                "module": module,
                "information": information
            }
        with self.file.open("w") as f:
            f.write(json.dumps(items, indent=2))
            f.close()

class importer:

    def __init__(self, file: pathlib.Path):
        with file.open("r") as f:
            content = f.read()
            f.close()
        self.items = json.loads(content)

    def find(self, name: str):
        items = self.items[name]
        module = importlib.import_module(items["module"])
        class_ = getattr(module, items["class_"])
        instance = class_(**json.loads(items["information"]))
        return instance
