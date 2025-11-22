import inspect
import sys
import io
import json
import os
import webview
from datetime import datetime
from contextlib import redirect_stdout, redirect_stderr

class Api:
    def __init__(self):
        self.globals = {}
        self.current_edb_path = "pcb.aedb"
        self.window = None
        self.config_path = "config.json"
        # Defer EDB loading to prevent CLR conflicts during startup

    def set_window(self, window):
        self.window = window
        
    def _load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error reading config: {e}")
        return {}

    def _save_config_file(self, config_data):
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config_data, f, indent=4)
        except Exception as e:
            print(f"Failed to save config: {e}")

    def get_app_config(self):
        """Returns the current configuration."""
        return self._load_config()

    def update_app_config(self, updates):
        """Updates the configuration with the provided dictionary."""
        config = self._load_config()
        config.update(updates)
        self._save_config_file(config)
        return config

    def pick_edb_folder(self):
        if not self.window:
            return {"status": "error", "message": "Window not attached."}
        
        # Open folder dialog
        result = self.window.create_file_dialog(webview.FOLDER_DIALOG)
        if result and len(result) > 0:
            new_path = result[0]
            return self.load_edb(new_path)
        return {"status": "cancelled", "message": "No folder selected."}

    def load_edb(self, path=None):
        if path:
            self.current_edb_path = path
            
        print(f"Loading EDB from {self.current_edb_path}...")

        # Close existing EDB if open
        if hasattr(self, 'edb') and self.edb:
            print("Closing existing EDB...")
            try:
                self.edb.close_edb()
                print("Existing EDB closed successfully.")
            except Exception as e:
                print(f"Error closing existing EDB: {e}")
            self.edb = None # Clear reference

        # Config setup
        config = self._load_config()
        saved_version = config.get("aedt_version")

        # Define versions to try
        # Default priority: Saved -> 2024.1 -> others
        current_year = datetime.now().year
        default_versions = []
        for year in range(2024, current_year + 1):
            default_versions.append(f"{year}.1")
            default_versions.append(f"{year}.2")

        versions_to_try = []
        
        if saved_version:
            versions_to_try.append(saved_version)
            
        for v in default_versions:
            if v != saved_version:
                versions_to_try.append(v)

        try:
            from pyedb import Edb
        except ImportError:
            print("pyedb not installed or failed to import.")
            self.globals['edb'] = "pyedb not installed"
            return {"status": "error", "message": "pyedb not installed"}

        last_error = None
        
        for v in versions_to_try:
            print(f"Trying to open EDB with AEDT version {v}...")
            try:
                self.edb = Edb(self.current_edb_path, version=v)
                self.globals['edb'] = self.edb
                print(f"EDB loaded successfully with version {v}.")
                
                # Save successful version
                self.update_app_config({"aedt_version": v})

                return {"status": "success", "message": f"EDB loaded (v{v}) from {os.path.basename(self.current_edb_path)}."}
            except Exception as e:
                print(f"Failed to load with version {v}: {e}")
                last_error = e
                # Continue to next version

        # If loop finishes, all failed
        error_msg = f"Failed to load EDB with any version. Last error: {last_error}"
        print(error_msg)
        self.globals['edb'] = error_msg
        return {"status": "error", "message": error_msg}

    def get_global_vars(self):
        """Returns a list of global variable names and their types."""
        vars_info = []
        for name, obj in self.globals.items():
            # Skip internal python vars if any (though we usually control self.globals)
            if name.startswith("__"): continue
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
                # To ensure variables defined in console are available globally (and thus in the UI tree),
                # we use self.globals for both locals and globals.
                exec(code, self.globals, self.globals)
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
            # Use self.globals for both globals and locals
            obj = eval(obj_path, self.globals, self.globals)
            
            obj_type = type(obj).__name__
            obj_doc = inspect.getdoc(obj) or "No documentation available."
            
            members = []
            # Use dir() then getattr() for more robust inspection of CLR/.NET objects
            # inspect.getmembers() fails if any property raises an error
            
            for name in dir(obj):
                if name.startswith("_"): continue # Skip private/magic methods
                
                try:
                    value = getattr(obj, name)
                    
                    kind = "property"
                    if callable(value) or inspect.isroutine(value):
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
                except Exception:
                    # If retrieving the attribute fails (common with some properties), skip it
                    pass
            
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
            obj = eval(obj_path, self.globals, self.globals)
            return {"value": str(obj), "type": type(obj).__name__}
        except Exception as e:
            return {"error": str(e)}
