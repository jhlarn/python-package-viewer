import inspect
import sys
import io
from contextlib import redirect_stdout, redirect_stderr

class Api:
    def __init__(self):
        self.globals = {}
        self.locals = {}
        # Defer EDB loading to prevent CLR conflicts during startup

    def load_edb(self):
        print("Loading EDB...")
        try:
            from pyedb import Edb
            # Using the version specified in README, but defaulting to generic if needed
            # Assuming pcb.aedb is in the current working directory
            self.edb = Edb("pcb.aedb", version='2024.1')
            self.globals['edb'] = self.edb
            print("EDB loaded successfully.")
            return {"status": "success", "message": "EDB loaded."}
        except ImportError:
            print("pyedb not installed or failed to import.")
            self.globals['edb'] = "pyedb not installed"
            return {"status": "error", "message": "pyedb not installed"}
        except Exception as e:
            print(f"Failed to load EDB: {e}")
            self.globals['edb'] = f"Error loading EDB: {str(e)}"
            return {"status": "error", "message": str(e)}

    def get_global_vars(self):
        """Returns a list of global variable names and their types."""
        vars_info = []
        for name, obj in self.globals.items():
            vars_info.append({
                "name": name,
                "type": type(obj).__name__,
                "repr": str(obj)[:100]  # Truncate for initial view
            })
        return vars_info

    def evaluate(self, code):
        """Executes Python code and returns stdout/stderr."""
        f = io.StringIO()
        error_msg = None
        result = None
        
        # Capture stdout/stderr
        with redirect_stdout(f), redirect_stderr(f):
            try:
                # We use exec for statements and eval for expressions if possible, 
                # but for a console, usually exec is safer for general code blocks.
                # To allow "return" values from single expressions, we can try eval first
                # or just rely on printing.
                # For this implementation, we'll stick to exec and update globals.
                exec(code, self.globals, self.locals)
            except Exception as e:
                error_msg = str(e)
                print(f"Error: {e}")
        
        output = f.getvalue()
        return {"output": output, "error": error_msg}

    def get_object_info(self, obj_path):
        """
        Introspects an object based on its name/path in the globals.
        obj_path: string, e.g., 'edb.active_layout'
        """
        try:
            # Evaluate the object path to get the actual object
            obj = eval(obj_path, self.globals, self.locals)
            
            obj_type = type(obj).__name__
            obj_doc = inspect.getdoc(obj) or "No documentation available."
            
            members = []
            # Inspect members
            for name, value in inspect.getmembers(obj):
                if name.startswith("_"): continue # Skip private/magic methods
                
                kind = "property"
                if inspect.isroutine(value):
                    kind = "method"
                elif inspect.isclass(value):
                    kind = "class"
                elif isinstance(value, (list, tuple, dict)):
                    kind = "collection"
                
                members.append({
                    "name": name,
                    "kind": kind,
                    "type": type(value).__name__
                })
            
            # If it's a collection, we might want to send its items (or a subset)
            collection_items = None
            if isinstance(obj, (list, tuple)):
                collection_items = [{"index": i, "value": str(v)[:50], "type": type(v).__name__} for i, v in enumerate(obj[:100])] # Limit to 100
            elif isinstance(obj, dict):
                # Use repr(k) so it can be safely used in eval path (e.g. includes quotes for strings)
                collection_items = [{"key": repr(k), "value": str(v)[:50], "type": type(v).__name__} for k, v in list(obj.items())[:100]]

            return {
                "name": obj_path,
                "type": obj_type,
                "doc": obj_doc,
                "members": members,
                "is_collection": isinstance(obj, (list, tuple, dict)),
                "collection_items": collection_items,
                "value": str(obj) if not isinstance(obj, (list, tuple, dict)) and not inspect.isroutine(obj) and not inspect.isclass(obj) else None
            }
            
        except Exception as e:
            return {"error": str(e)}

    def get_object_value(self, obj_path):
        """Returns the value of an object if it's simple."""
        try:
            obj = eval(obj_path, self.globals, self.locals)
            return {"value": str(obj), "type": type(obj).__name__}
        except Exception as e:
            return {"error": str(e)}
