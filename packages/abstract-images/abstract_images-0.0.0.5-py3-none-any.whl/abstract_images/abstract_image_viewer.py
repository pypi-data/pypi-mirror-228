import os
import json
import webbrowser
from abstract_gui import get_gui_fun,expandable,create_row_of_buttons,create_window_manager,get_window
from abstract_utilities.read_write_utils import read_from_file, write_to_file
from abstract_utilities.type_utils import ensure_integer
from .image_utils import resize_image
window_mgr,upload_bridge,script_name=create_window_manager(global_var=globals())
js_bridge = upload_bridge.return_global_variables(script_name=script_name)
def update_values(window:type(get_window())=None,key:str=None,args:dict={}):
    """
    Update the values in the window manager.

    Parameters:
    - window: The window object for which values need to be updated. Default is None.
    - key: The key for which the value needs to be updated.
    - args: Additional arguments.

    Returns:
    - None
    """
    if key == None:
        return
    window_mgr.update_values(window=window,key=key,args=args)
def get_bridge_value(key):
    """
    Fetch a value from the js_bridge using the provided key.

    Parameters:
    - key: The key to fetch the value for.

    Returns:
    - Value associated with the given key.
    """

    return js_bridge["all_list"][js_bridge["image_num"]][key]
def get_image(image_path:str=None):
    """
    Retrieve an image after resizing it based on the set max dimensions.

    Parameters:
    - image_path: The path to the image. If None, the default path is used.

    Returns:
    - Resized image.
    """
    if image_path == None:
        image_path = os.path.join(js_bridge["parent_directory"],get_bridge_value("image_save"))
    if os.path.isfile(image_path):
        return resize_image(image_path, max_width=js_bridge["image_dimensions"]["max_width"], max_height=js_bridge["image_dimensions"]["max_height"])
    
def change_image_num(k:int=1):
    """
    Change the current image number.

    Parameters:
    - k: Increment/decrement value for the image number. Default is 1.

    Returns:
    - Updated image number.
    """
    if k == 1:
        js_bridge["image_num"]+=k
    elif k == -1:
        js_bridge["image_num"]+=k
    if js_bridge["image_num"] <0:
        js_bridge["image_num"] = 0
    elif js_bridge["image_num"] > len(js_bridge["all_list"])-1:
        js_bridge["image_num"] = len(js_bridge["all_list"])-1
    return js_bridge["image_num"]
def event_while(event):
    """
    Handle events that occur within the GUI.

    Parameters:
    - event: The event that is triggered within the GUI.

    Returns:
    - None
    """
    if get_bridge_value("title") in js_bridge["nono_list"]["contents"]["opened"]:
            update_values(key="Download",args={"disabled":True})
    else:
        update_values(key="Download",args={"disabled":False})
    if event == "grave:49":
        update_values(key="-FRAME_INPUT-",args={"value":0})
    if event == "space:65":
        event = "Download"
    if event == "Shift_L:50":
        event = "skip"
    if event in "1:10,2:11,3:12,4:13,5:14,6:15,7:16,8:17,9:18,0:19".split(','):
        num = int(str(window_mgr.get_values()["-FRAME_INPUT-"])+str(event.split(':')[0]))
    if event in ['Left:113']:
        event = "Previous"
    elif event in ['Right:114']:
        event = "Next"

    if event in ["-FRAME_INPUT-","Download","Open Image","Previous","Next","Favorite","Remove","skip"]:
        if event == "Previous":
            change_image_num(k=-1)
        if event == "Next":
            change_image_num(k=1)
        if event == "-FRAME_INPUT-":
            val = ensure_integer(window_mgr.get_values()["-FRAME_INPUT-"],len(js_bridge["all_list"])-1)
            update_values(key="-FRAME_INPUT-",args={"value":val})
            if val > len(js_bridge["all_list"])-1:
                update_values(key="-FRAME_INPUT-",args={"value":len(js_bridge["all_list"])-1})
            if val < 0:
                update_values(key="-FRAME_INPUT-",args={"value":0})
        if event == "Open Image":
            webbrowser.open(get_bridge_value("image"), new=2)
        if event == "skip":
            js_bridge["image_num"] = int(window_mgr.get_values()["-FRAME_INPUT-"])
        if event == "Download":
            if js_bridge["all_list"][js_bridge["image_num"]]['title'] not in js_bridge["nono_list"]["contents"]["opened"]:
                webbrowser.open(get_bridge_value("download"), new=2)
                js_bridge["nono_list"]["contents"]["opened"].append(get_bridge_value("title"))
            write_to_file(filepath=js_bridge["nono_list"]["path"],contents=json.dumps(js_bridge["nono_list"]))
            change_image_num(k=1)
        if event in ["skip","Next","Previous","Download"]:
            try:
                update_values(key="-CURR_IMG-",args={"value":js_bridge["image_num"]})
                update_values(key="-IMAGE_TITLE-",args={"value": get_bridge_value("title")})
                update_values(key="-IMAGE_AUTHOR-",args={"value": get_bridge_value("user")})
                update_values(key="-IMAGE_PATH-",args={"value": get_bridge_value("download")})
                update_values(key="-IMAGE_COMPONENT-",args={"data": get_image()})
            except Exception as e:
                print(f"it didnt work: {e}")
def abstract_image_viewer_main(all_list_directory:list,parent_directory:str='',nono_list_directory:dict={"opened":[],"never":[]},window_size:tuple=(1200,1600),image_max_width:int=1000,image_max_height:int=800):
    """
    Main function to initialize and manage the Abstract Image Viewer GUI.

    Parameters:
    - all_list_directory: Directory containing the list of all images.
    - parent_directory: Parent directory for image and list paths.
    - nono_list_directory: Directory with lists of images that shouldn't be opened or downloaded.
    - window_size: Tuple representing the width and height of the GUI window.
    - image_max_width: Maximum width for displayed images.
    - image_max_height: Maximum height for displayed images.

    Returns:
    - None
    """
    js_bridge["image_num"] = 0
    js_bridge["parent_directory"]=parent_directory
    js_bridge["image_dimensions"]={"max_width":image_max_width,"max_height":image_max_height}
    js_bridge["all_list"]=json.loads(read_from_file(os.path.join(js_bridge["parent_directory"],all_list_directory)))
    js_bridge["nono_list"]={"path":os.path.join(js_bridge["parent_directory"],nono_list_directory)}
    js_bridge["nono_list"]["contents"]=json.loads(read_from_file(js_bridge["nono_list"]["path"]))
    js_bridge["nono_list"]["contents"]=js_bridge["nono_list"]["contents"]["contents"]
    layout = [[[[get_gui_fun("T",args={"text":"title","key":"-IMAGE_TITLE-"})],
        [get_gui_fun("T",args={"text":"author","key":"-IMAGE_AUTHOR-"})],
        [get_gui_fun("T",args={"text":"title","key":"-IMAGE_PATH-"})],
        [get_gui_fun("T",args={"text":"0","key":"-CURR_IMG-"}),get_gui_fun("T",args={"text":"of"}),get_gui_fun("T",args={"text":len(js_bridge["all_list"]),"key":"-MAX_IMG-"})]],
        [get_gui_fun("Image",args={"data":get_image(),"size":(None,None),"key":"-IMAGE_COMPONENT-"})],
        [create_row_of_buttons("Download","Open Image","Previous","Next","Favorite","Remove"),get_gui_fun("Frame",args={"title":"","layout":
                                   [[get_gui_fun("Input",args={"default_text":0,"size":(6,2),"key":"-FRAME_INPUT-","enable_events":True})]]})],create_row_of_buttons("skip"),]]
    window = window_mgr.get_new_window("Abstract Image Viewer",args={"layout":layout,"size": window_size,"event_function":"event_while",**expandable(),"return_keyboard_events":True})
    window_mgr.while_basic(window=window)
