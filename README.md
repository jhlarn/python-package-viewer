# EDB Explorer

This tool provides a graphical user interface (GUI) to explore EDB (Electronic Database) files using PyEDB. It allows you to inspect objects, properties, methods, and interact with the EDB through a Python console.

---

## Installation

To set up the development environment and install the necessary dependencies, follow these steps:

1.  **Prerequisites**: Ensure you have `uv` installed. If not, you can install it via `pip`:
    ```shell
    pip install uv
    ```
    (Alternatively, you can manually create a virtual environment and install dependencies using `pip`.)

2.  **Run the Installation Script**: Navigate to the project directory in your terminal and execute `install.bat`:
    ```shell
    install.bat
    ```
    This script will create a Python virtual environment (`.venv`) if it doesn't exist and install all required packages (including `pyedb` and `pywebview`). If the `.venv` already exists, it will update the dependencies.

## Usage

Once the installation is complete, you can launch the EDB Explorer GUI:

1.  **Launch the GUI**: Execute `run.bat` from the project directory:
    ```shell
    run.bat
    ```
    This will open the EDB Explorer window.

2.  **Initial EDB Loading**:
    -   The application will attempt to load `pcb.aedb` by default.
    -   It will try various AEDT versions (e.g., '2024.1', '2024.2', etc.) to find a compatible installation.
    -   A successful version will be saved in `config.json` for faster loading in the future.

3.  **GUI Layout**:
    -   **Left Panel**: Displays "Global Variables", including the loaded `edb` object and any variables you define in the console. You can click the "Ref" button to refresh this list.
    -   **Center Panel**: Shows "Object Details" (type, value, and formatted docstring) for the currently selected object.
    -   **Right Panel**: Displays "Members / Inspector" (properties and methods) of the selected object. It includes a regex filter input to search through members.
    -   **Bottom Panel**: A "Python Console" for interactive code execution.

4.  **Interacting with Objects**:
    -   **Select an Object**: Click on an object in the "Global Variables" tree to display its details in the Center Panel and its members in the Right Panel. The object's path will appear in the "Target" input field.
    -   **Navigate Members**: Click on a property or method in the "Members / Inspector" panel to append it to the "Target" input and inspect it further.
    -   **Undo/Redo Navigation**: Use the "Undo" and "Redo" buttons (to the right of the "Target" input) to navigate through your inspection history.
    -   **Filter Members**: Use the regex input field in the "Members / Inspector" panel to filter the displayed properties and methods.

5.  **Loading EDB Files**:
    -   **Import**: Click the "Import" button to open a file dialog and select a different `.aedb` folder to load.
    -   **Reload**: Click the "Reload" button to close the current EDB and reload it. This is useful if the EDB file has changed externally. Each time a new EDB is loaded (via Import or Reload), `edb.close_edb()` is called to release resources.

6.  **Python Console**:
    -   Type Python code into the input field at the bottom.
    -   Press `Enter` to execute. (Use `Shift+Enter` for multi-line input without immediate execution).
    -   Output and errors will be displayed in the console output area.
    -   Variables defined in the console (e.g., `my_var = 123`) will appear in the "Global Variables" panel after execution.

---

### Original README Content:

1. the tool defaultly load pcb.aedb with the command:
    ```shell
    from pyedb import Edb
    edb = Edb("pcb.aedb", version='2024.1')
    ```
2. the load object edb is shown in objs tree in left side panel "Global Variables" in pywebview GUI. when I click the edb object, it will be shown in target input on topside of GUI. 
3. target input could be object, method or property.
4. if target is object, the properties and methods of target object are shown in the right side panel. ignore the private properties and methods start with "_".

5. I can click the property or method of target object to show it in target input.
6. if target is method, the help info of method is shown in Help panel in right side panel. 

7. if target is property, the value of property is shown in target input. if the property is object, I can click it to show in target input.

8. if target is list, dict, or tuple, the elements are shown in right side panel. I can click the element to show it in target input.

8. At bottom side panel, is the python console, I can input any python code to interact with edb object. or define variables in console. the variable will be shown in global variables tree in left side panel. I can click the variable to show it in target input.

9. I can refresh the global objs tree and global variables tree by clicking the "Refresh Objs" and "Refresh Vars" button on topside of GUI.
