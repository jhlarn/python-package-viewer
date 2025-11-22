# Todo List for LMZ EDB Explorer

## Phase 1: Project Initialization & UI Skeleton
- [ ] **Setup Environment**: Ensure `uv` or `pip` installs dependencies (`pyedb`, `pywebview`).
- [ ] **Basic Webview Window**: Create a simple `main.py` that opens a `pywebview` window with a basic HTML template.
- [ ] **Frontend Layout**: Design the 3-panel layout (Left: Global Vars, Right: Inspector/Help, Bottom: Console) using HTML/CSS (or a simple frontend framework/library).

## Phase 2: Backend Core (PyEDB Integration)
- [ ] **Load EDB**: Implement the function to load `pcb.aedb` (or fallback/mock if missing) as the initial `edb` object.
- [ ] **Object Introspection Service**: Create a Python class/API to be exposed to JS that can:
    - [ ] `get_type(obj_name)`: Return type info.
    - [ ] `get_members(obj_name)`: Return list of attributes/methods.
    - [ ] `get_doc(obj_name)`: Return docstrings for methods.
    - [ ] `get_value(obj_name)`: Return value for simple types or properties.
- [ ] **State Management**: Manage a dictionary of "global variables" including the loaded `edb`.

## Phase 3: Frontend Implementation
- [ ] **Left Panel (Global Vars)**:
    - [ ] Render a tree/list of global variables.
    - [ ] Click handler to set "Target Input".
- [ ] **Top Bar (Target Input)**:
    - [ ] Display the current object/expression path.
- [ ] **Right Panel (Inspector)**:
    - [ ] **Object View**: List attributes and methods. Clicking them updates "Target Input".
    - [ ] **Collection View**: If target is list/dict, show elements.
    - [ ] **Value View**: If target is a property/primitive, show its value.
    - [ ] **Help View**: If target is a method, show docstring.
- [ ] **Bottom Panel (Console)**:
    - [ ] Simple text input for Python code.
    - [ ] Send code to backend `exec()` context.
    - [ ] Display output/errors.
- [ ] **Refresh Functionality**: Implement "Refresh Objs" and "Refresh Vars" buttons to re-fetch state from backend.

## Phase 4: Polish & Testing
- [ ] **Error Handling**: Gracefully handle invalid EDB paths or non-inspectable objects.
- [ ] **Styling**: Improve UI aesthetics (dark mode, readable fonts).
- [ ] **Testing**: Verify `pyedb` interactions with the sample `pcb.aedb`.
