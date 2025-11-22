# EDB Explorer

This tool provides a graphical user interface (GUI) to explore EDB (Electronic Database) files using PyEDB. It allows you to inspect objects, properties, methods, and interact with the EDB through a Python console.

---

## Installation

To set up the development environment and install the necessary dependencies, follow these steps:

1.  **Run the Installation Script**:
    The installation scripts (`install.bat` for Windows, `install.sh` for Linux) will automatically check for and install `uv` (a fast Python package installer and manager) if it's not found on your system. It will then create a Python virtual environment (`.venv`) if it doesn't exist and install all required packages (including `pyedb` and `pywebview`). If the `.venv` already exists, it will update the dependencies.

    *   **Windows**: Navigate to the project directory in your terminal and execute `install.bat`:
        ```shell
        install.bat
        ```

    *   **Linux**: Navigate to the project directory in your terminal, make the script executable, and then run `install.sh`:
        ```bash
        chmod +x install.sh
        ./install.sh
        ```

## Usage

Once the installation is complete, you can launch the EDB Explorer GUI:

1.  **Launch the GUI**:

    *   **Windows**: Execute `run.bat` from the project directory:
        ```shell
        run.bat
        ```
        This will open the EDB Explorer window without a console window.

    *   **Linux**: Navigate to the project directory in your terminal, make the script executable, and then run `run.sh`:
        ```bash
        chmod +x run.sh
        ./run.sh
        ```
        This will launch the EDB Explorer in the background.

2.  **Initial EDB Loading**:
    -   The application will attempt to load `pcb.aedb` by default.
    -   It will try various AEDT versions (e.g., '2024.1', '2024.2', up to the current year) to find a compatible installation.
    -   A successful version will be saved in `config.json` for faster loading in the future.

3.  **GUI Layout**:
    -   **Left Panel**: Displays "Global Variables" (the loaded `edb` object and variables from the console) and a "Favorites" section. You can click "Ref" to refresh the global variables.
    -   **Center Panel**: Shows "Object Details" (type, value, and formatted docstring) for the currently selected object. The docstring panel will dynamically fill available space.
    -   **Right Panel**: Displays "Members / Inspector" (properties and methods) of the selected object. It includes a regex filter input to search through members.
    -   **Bottom Panel**: A "Python Console" for interactive code execution. Its visibility can be toggled.

4.  **Interacting with Objects**:
    -   **Select an Object**: Click on an object in the "Global Variables" or "Favorites" tree to display its details in the Center Panel and its members in the Right Panel. The object's path will appear in the "Target" input field.
    -   **Navigate Members**: Click on a property or method in the "Members / Inspector" panel to append it to the "Target" input and inspect it further.
    -   **Undo/Redo Navigation**: Use the "Undo" and "Redo" buttons (to the right of the "Target" input) to navigate through your inspection history.
    -   **Add to Favorites**: Click the "★" button next to the "Target" input to add the current object path to your Favorites. Favorites are persisted in `config.json`.
    -   **Remove Favorite**: Click the "×" next to a favorite item to remove it.
    -   **Filter Members**: Use the regex input field in the "Members / Inspector" panel to filter the displayed properties and methods.

5.  **Loading EDB Files**:
    -   **Import**: Click the "Import" button to open a file dialog and select a different `.aedb` folder to load.
    -   **Reload**: Click the "Reload" button to close the current EDB and reload it. This is useful if the EDB file has changed externally. Each time a new EDB is loaded (via Import or Reload), `edb.close_edb()` is called to release resources.

6.  **Python Console**:
    -   **Toggle Visibility**: Click the "Console" button in the top bar to show or hide the console panel.
    -   Type Python code into the input field at the bottom.
    -   Press `Enter` to execute. (Use `Shift+Enter` for multi-line input without immediate execution).
    -   Output and errors will be displayed in the console output area.
    -   Variables defined in the console (e.g., `my_var = 123`) will appear in the "Global Variables" panel after execution.

7.  **Tunable Panel Borders**:
    -   Drag the gray separator lines between the Left/Center, Center/Right, and Global Vars/Favorites panels, as well as between the main content and the console, to adjust their sizes.
    -   Your preferred panel dimensions are automatically saved to `config.json` and restored on startup.

**Configuration Persistence**: Most user preferences, including AEDT version, Favorites, and panel sizes, are saved in `config.json`.
