edb_explorer
---

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