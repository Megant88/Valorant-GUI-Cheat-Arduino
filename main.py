import tkinter as tk
import json, os, keyboard, time, requests, base64, ctypes, sys, wmi, datetime
from io import BytesIO
from PIL import ImageGrab, ImageTk, Image
from pynput import mouse
from ctypes import WinDLL
from cheese import *

NEPHRITIS_BUILD = "ARDUINO"

keyboard_key_vk_codes = {
    '1': "0x31",
    '2': "0x32",
    '3': "0x33",
    '4': "0x34",
    '5': "0x35",
    '6': "0x36",
    '7': "0x37",
    '8': "0x38",
    '9': "0x39",
    '0': "0x30",
    'a': "0x41",
    'b': "0x42",
    'c': "0x43",
    'd': "0x44",
    'e': "0x45",
    'f': "0x46",
    'g': "0x47",
    'h': "0x48",
    'i': "0x49",
    'j': "0x4A",
    'k': "0x4B",
    'l': "0x4C",
    'm': "0x4D",
    'n': "0x4E",
    'o': "0x4F",
    'p': "0x50",
    'q': "0x51",
    'r': "0x52",
    's': "0x53",
    't': "0x54",
    'u': "0x55",
    'v': "0x56",
    'w': "0x57",
    'x': "0x58",
    'y': "0x59",
    'z': "0x5A",
    'tab': "0x09",
    'caps_lock':"0x14",
    'shift_l':"0xA0",
    'shift_r':"0xA1",
    'control_l':"0xA2",
    'control_r':"0xA3",
    'alt_l':"0xA4",
    "alt_r":"0xA5",
    "space":"0x20"
}

class CustomButton:
    def __init__(self, canvas, x, y, width, height, corner_radius, fill_color, text, on_change):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.fill_color = fill_color
        self.text = text
        self.on_change = on_change

        self.component_ids = []

        self.draw_rounded_rectangle()

        self.center_x = self.x + self.width / 2
        self.center_y = self.y + self.height / 2

        self.text_id = self.canvas.create_text(self.center_x, self.center_y, text=self.text, fill="white",
                                              font=("Helvetica", 12))

        self.canvas.bind("<Button-1>", self.button_click)

    def draw_rounded_rectangle(self):
        self.component_ids.append(self.canvas.create_rectangle(
            self.x + self.corner_radius, self.y,
            self.x + self.width - self.corner_radius, self.y + self.height,
            fill=self.fill_color,
            outline=self.fill_color
        ))
        self.component_ids.append(self.canvas.create_rectangle(
            self.x, self.y + self.corner_radius,
            self.x + self.width, self.y + self.height - self.corner_radius,
            fill=self.fill_color,
            outline=self.fill_color
        ))

        self.component_ids.append(self.canvas.create_arc(
            self.x, self.y,
            self.x + self.corner_radius * 2, self.y + self.corner_radius * 2,
            start=90, extent=90,
            fill=self.fill_color,
            outline=self.fill_color
        ))
        self.component_ids.append(self.canvas.create_arc(
            self.x + self.width - self.corner_radius * 2, self.y,
            self.x + self.width, self.y + self.corner_radius * 2,
            start=0, extent=90,
            fill=self.fill_color,
            outline=self.fill_color
        ))
        self.component_ids.append(self.canvas.create_arc(
            self.x, self.y + self.height - self.corner_radius * 2,
            self.x + self.corner_radius * 2, self.y + self.height,
            start=180, extent=90,
            fill=self.fill_color,
            outline=self.fill_color
        ))
        self.component_ids.append(self.canvas.create_arc(
            self.x + self.width - self.corner_radius * 2, self.y + self.height - self.corner_radius * 2,
            self.x + self.width, self.y + self.height,
            start=270, extent=90,
            fill=self.fill_color,
            outline=self.fill_color
        ))

    def button_click(self, event):
        if self.is_inside_button(event):
            print("Button Clicked!")
            time.sleep(0.5)
            self.set_hotkey()


    def set_hotkey(self):
        self.canvas.focus_set()
        self.canvas.bind("<Key>", self.handle_keypress)
        self.mouse_listener = mouse.Listener(on_click=self.handle_mouse_click)
        self.mouse_listener.start()

    def handle_keypress(self, event):
        if event.keysym.lower() == 'escape':
            self.canvas.unbind("<Key>")
            self.mouse_listener.stop()
        else:
            hotkey = event.keysym.lower()
            vk_code = get_keyboard_key_vk_code(hotkey)
            if vk_code != -1:
                self.canvas.unbind("<Key>")
                self.mouse_listener.stop()
                print(f"Hotkey set to: {hotkey} (VK Code: {vk_code})")
                self.set_text(vk_code)
                self.on_change(vk_code)

                

            else:
                print("cock")

    def handle_mouse_click(self, x, y, button, pressed):
        if not pressed:
            return

        # mapped mouse keys
        button_vk_codes = {
            mouse.Button.left: "0x01",
            mouse.Button.right: "0x02",
            mouse.Button.middle: "0x04",
            mouse.Button.x1: "0x05",
            mouse.Button.x2: "0x06",
        }

        button_name = {
            mouse.Button.left: "left",
            mouse.Button.right: "right",
            mouse.Button.middle: "middle",
            mouse.Button.x1: "x1",
            mouse.Button.x2: "x2",
        }.get(button, "unknown")

        vk_code = button_vk_codes.get(button, -1)
        if vk_code != -1:
            hotkey = f"Mouse {button_name}"
            keyboard.unhook_all()
            self.mouse_listener.stop()
            print(f"Hotkey set to: {hotkey} (VK Code: {vk_code})")
            self.set_text(vk_code)
            self.on_change(vk_code)

    def button_delete(self,event):
        self.canvas.unbind("<Button-1>")
        self.canvas.delete(self.text_id)
        for item_id in self.component_ids:
            self.canvas.delete(item_id)
    
    def set_text(self, new_text):
        self.text = new_text
        self.canvas.itemconfig(self.text_id, text=self.text)

    def is_inside_button(self, event):
        return self.x <= event.x <= self.x + self.width and self.y <= event.y <= self.y + self.height


def get_keyboard_key_vk_code(key):
    return keyboard_key_vk_codes.get(key, -1)

class CustomSlider(tk.Canvas):
    def __init__(self, master, width, height, min_value, max_value, initial_value, value_format="raw", on_value_change=None):
        super().__init__(master, width=width, height=height, highlightthickness=0)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.on_value_change = on_value_change
        self.value_format = value_format  
        self.width = width
        self.height = height

        self.background_color = "#D9D9D9"
        self.fill_color = "#DE2828"
        self.text_color = "#000000"  
        self.corner_radius = 10  

        self.slider_width = 10
        self.slider_height = height

        self.create_rounded_rectangle(0, 0, width, height, self.corner_radius, fill=self.background_color, outline="")
        
        self.slider_handle = self.create_rectangle(0, 0, self.slider_width, self.slider_height, fill=self.fill_color, outline="")
        self.fill_rectangle = self.create_rectangle(0, 0, 0, self.slider_height, fill=self.fill_color, outline="")

        if self.value_format == "raw":
            self.value_text = self.create_text(width, height // 2, anchor="e", fill=self.text_color, font=("Inter Bold", 10))
        elif self.value_format == "raw2":
            self.value_text = self.create_text(width, height // 2, anchor="e", fill=self.text_color, font=("Inter Bold", 10))
        elif self.value_format == "percentage":
            self.value_text = self.create_text(width, height // 2, anchor="e", fill=self.text_color, font=("Inter Bold", 10))
        elif self.value_format == "integer":
            self.value_text = self.create_text(width, height // 2, anchor="e", fill=self.text_color, font=("Inter Bold", 10))

        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)

        self.move_slider_to_value() 

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        self.create_arc(x1, y1, x1 + 2 * radius, y1 + 2 * radius, start=90, extent=90, **kwargs)
        self.create_arc(x2 - 2 * radius, y1, x2, y1 + 2 * radius, start=0, extent=90, **kwargs)
        self.create_arc(x1, y2 - 2 * radius, x1 + 2 * radius, y2, start=180, extent=90, **kwargs)
        self.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2, start=270, extent=90, **kwargs)
        self.create_rectangle(x1 + radius, y1, x2 - radius, y2, **kwargs)

    def on_click(self, event):
        self.set_value(event.x)
        self.move_slider_to_value()

    def on_drag(self, event):
        self.set_value(event.x)
        self.move_slider_to_value()

    def set_value(self, x):
        normalized_x = max(0, min(x, self.winfo_width()))
        self.value = (normalized_x / self.winfo_width()) * (self.max_value - self.min_value) + self.min_value
        if self.on_value_change:
            self.on_value_change(self.value)

    def move_slider_to_value(self):
        x = (self.value - self.min_value) / (self.max_value - self.min_value) * self.width
        #print(x)
        #print(self.winfo_width())
        self.coords(self.slider_handle, x, 0, x + self.slider_width, self.slider_height)
        fill_width = x
        #print(fill_width)
        self.coords(self.fill_rectangle, 0, 0, fill_width, self.slider_height)
            
        if self.value_format == "raw":
            value_display = f"{self.value:.4f}"
        elif self.value_format == "raw2":
            value_display = f"{self.value:.2f}"
        elif self.value_format == "percentage":
            value_display = f"{int(self.value * 100)}%"
        elif self.value_format == "integer":
            value_display = str(int(self.value))
        self.itemconfig(self.value_text, text=value_display)

class CheatGUI:
    def __init__(self, root):
        self.content_elements = {}
        self.root = root
        self.root.geometry("633x384")
        self.root.configure(bg="#0F1014")
        self.config_path = "config.json"

        self.canvas = tk.Canvas(
            self.root,
            bg="#0F1014",
            height=384,
            width=633,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.image_image_1 = ImageTk.PhotoImage(self.get_image_from_url("https://i.ibb.co/QfTV6yD/image-1.png"))
        self.image_1 = self.canvas.create_image(
            195.0,
            190.0,
            image=self.image_image_1
        )

        self.button_image_1 = ImageTk.PhotoImage(self.get_image_from_url("https://i.ibb.co/Lvx7DHX/button-1.png"))
        self.button_1 = tk.Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.run_cheese,
            relief="flat"
        )
        self.button_1.place(
            x=310.0,
            y=333.0,
            width=63.0,
            height=38.0
        )

        self.button_image_2 = ImageTk.PhotoImage(self.get_image_from_url("https://i.ibb.co/C89QRmD/button-2.png"))
        self.button_2 = tk.Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.load_content_1,
            relief="flat"
        )
        self.button_2.place(
            x=9.0,
            y=16.0,
            width=111.0,
            height=55.0
        )

        self.button_image_3 = ImageTk.PhotoImage(self.get_image_from_url("https://i.ibb.co/C180syT/button-3.png"))
        self.button_3 = tk.Button(
            self.canvas,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.load_content_2,
            relief="flat"
        )
        self.button_3.place(
            x=5.0,
            y=82.0,
            width=111.0,
            height=55.0
        )

        self.button_image_4 = ImageTk.PhotoImage(self.get_image_from_url("https://i.ibb.co/1rgcqqc/button-4.png"))
        self.button_4 = tk.Button(
            self.canvas,
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.load_content_3,
            relief="flat"
        )
        self.button_4.place(
            x=5.0,
            y=150.0,
            width=111.0,
            height=55.0
        )

        self.button_image_5 = ImageTk.PhotoImage(self.get_image_from_url("https://i.ibb.co/9pn2QBV/button-5.png"))
        self.button_5 = tk.Button(
            self.canvas,
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=self.load_content_4,
            relief="flat"
        )
        self.button_5.place(
            x=4.0,
            y=213.0,
            width=111.0,
            height=55.0
        )
        self.load_images()
        self.load_config()
        self.load_content_1()
        self.drag_region = (0, 0, 633, 2)
        self._drag_data = {"x": 0, "y": 0, "dragging": False}
        self.root.bind("<ButtonPress-1>", self.startmove)
        self.root.bind("<ButtonRelease-1>", self.stopmove)
        self.root.bind("<B1-Motion>", self.onmove)
    
    def load_config(self):
        with open(self.config_path) as json_file:
            data = json.load(json_file)
        try:
            self.enable_triggerbot = data["triggerbot"]["enable_triggerbot"]
            self.trigger_hotkey = data["triggerbot"]["trigger_hotkey"]
            self.trigger_delay = data["triggerbot"]["trigger_delay"]
            self.base_delay = data["triggerbot"]["base_delay"]
            self.always_enabled = data["triggerbot"]["always_enabled"]
            self.color_tolerance = data["triggerbot"]["color_tolerance"]

            self.enable_aimbot = data["aimbot"]["enable_aimbot"]
            self.enable_rcs = data["aimbot"]["enable_rcs"]
            self.x_only = data["aimbot"]["x_only"]
            self.aimbot_hotkey = data["aimbot"]["aimbot_hotkey"]
            self.experimental_filtering = data["aimbot"]["experimental_filtering"]
            self.anti_astra = data["aimbot"]["anti_astra"]
            self.x_fov = data["aimbot"]["x_fov"]
            self.y_fov = data["aimbot"]["y_fov"]
            self.cop = data["aimbot"]["cop"]
            self.x_speed = data["aimbot"]["x_speed"]
            self.y_speed = data["aimbot"]["y_speed"]
            self.custom_yoffset = data["aimbot"]["custom_yoffset"]

            self.enable_instantlocker = data["instantlocker"]["enable_instantlocker"]
            self.region = data["instantlocker"]["region"]
            self.preferred_agent = data["instantlocker"]["preferred_agent"]

            self.monitor_id = data["arduino_settings"]["monitor_id"]
            self.com_port = data["arduino_settings"]["com_port"]
            self.serial_id = data["arduino_settings"]["serial_id"]
        except:
            exiting()
            pass

    def startmove(self, event):
        if self.is_inside_drag_region(event.x, event.y):
            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y
            self._drag_data["dragging"] = True

    def stopmove(self, event):
        self._drag_data["dragging"] = False

    def onmove(self, event):
        if self._drag_data["dragging"]:
            x, y = event.x - self._drag_data["x"], event.y - self._drag_data["y"]
            self.root.geometry(f"+{self.root.winfo_x() + x}+{self.root.winfo_y() + y}")

    def is_inside_drag_region(self, x, y):
        x1, y1, x2, y2 = self.drag_region
        return x1 <= x <= x2 and y1 <= y <= y2

    def get_image_from_url(self, url):
        response = requests.get(url)
        image_data = response.content
        return Image.open(BytesIO(image_data))
    
    def update_config(self, section, key_to_update, new_value):
        with open(self.config_path, 'r') as config_file:
            config = json.load(config_file)

        if section in config:
            if key_to_update in config[section]:

                config[section][key_to_update] = new_value
            else:
                raise ValueError(f"'{key_to_update}' does not exist in the '{section}' section")
        else:
            raise ValueError(f"'{section}' section does not exist in the configuration")

        with open(self.config_path, 'w') as config_file:
            json.dump(config, config_file, indent=4)
            print(f'updated {key_to_update}')

    def change_config(self,configname):
        self.config_path = configname
        print(self.config_path)
        try:
            self.load_config()
        except:
            print('retard')
        else:
            print("changed config to " +configname)
            
    

    
    def list_json_files_in_folder(self,folder_path="."):
        try:
            json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]

            combined_json_files = "\n".join(json_files)

            return combined_json_files

        except Exception as e:
            return str(e)


    def cleanup_previous_content(self, elements_to_cleanup):
        if elements_to_cleanup:
            for element in elements_to_cleanup:
                if isinstance(element, CustomButton):
                    element.button_delete("kekw")
                elif isinstance(element, int):
                    print(str(element) + "  int")
                    self.canvas.delete(element)
                elif isinstance(element, tk.Widget):
                    print(f"Destroyed widget: {element}")
                    element.destroy()
                elif isinstance(element, tk.PhotoImage):
                    print(f"Deleted PhotoImage: {element}")
                    del element

        elements_to_cleanup.clear()

    def load_images(self):
        #aimbot
        self.not_pressed_image = ImageTk.PhotoImage(self.get_image_from_url("https://i.ibb.co/x7SmV63/trigger-button.png"))
        self.pressed_button_cock = ImageTk.PhotoImage(self.get_image_from_url("https://i.ibb.co/vcBpm10/pressedcock.png"))
        self.placeholde_image = ImageTk.PhotoImage(self.get_image_from_url("https://i.ibb.co/2sBrsmD/placeholder.png"))


        #trigger
        self.trigger_button_image = ImageTk.PhotoImage(self.get_image_from_url("https://i.ibb.co/x7SmV63/trigger-button.png"))
        self.button_pressed_image = ImageTk.PhotoImage(self.get_image_from_url("https://i.ibb.co/m0HSJg4/pressed-button.png"))
        self.always_enabled_button_image = ImageTk.PhotoImage(self.get_image_from_url("https://i.ibb.co/x7SmV63/trigger-button.png"))
        self.button_pressed2 = ImageTk.PhotoImage(self.get_image_from_url("https://i.ibb.co/m0HSJg4/pressed-button.png"))

        #instantlocker
        self.button_lock_image1_normal = ImageTk.PhotoImage(self.get_image_from_url("https://i.ibb.co/HKXzzKP/lock-button.png"))
        self.button_lock_image1_pressed = ImageTk.PhotoImage(self.get_image_from_url("https://i.ibb.co/m0HSJg4/pressed-button.png"))
        self.image_lock_image1 = ImageTk.PhotoImage(self.get_image_from_url("https://i.ibb.co/1K75nJ1/lock-image1.png"))
        self.image_lock_image2 = ImageTk.PhotoImage(self.get_image_from_url("https://i.ibb.co/1K75nJ1/lock-image1.png"))

        #settingspage
        self.image_settings_1 = ImageTk.PhotoImage(self.get_image_from_url("https://i.ibb.co/SQRyZR6/settings-1.png"))
        self.image_settings_2 = ImageTk.PhotoImage(self.get_image_from_url("https://i.ibb.co/G2V8QTP/settings-2.png"))
        self.image_settings_3 = ImageTk.PhotoImage(self.get_image_from_url("https://i.ibb.co/tHqG16r/settings-3.png"))
        self.image_settings_4 = ImageTk.PhotoImage(self.get_image_from_url("https://i.ibb.co/PzgHGXd/settings-4.png"))
        self.button_settings_1 = ImageTk.PhotoImage(self.get_image_from_url("https://i.ibb.co/HGPRhXL/load-cfg.png"))
        self.button_settings_2 = ImageTk.PhotoImage(self.get_image_from_url("https://i.ibb.co/8jY8J6H/save-cfg.png"))
        self.button_settings_3 = ImageTk.PhotoImage(self.get_image_from_url("https://i.ibb.co/ZX94rrP/del-cfg.png"))
                

    def run_cheese(self):
        self.root.destroy()
        set_config(self.config_path)
        cheese_start()

    def load_content_1(self):
        print("AIM CLICKED")
        previous_elements = self.content_elements.get('load_content_3', [])
        self.cleanup_previous_content(previous_elements)
        
        self.content_elements['load_content_3'] = []

        current_elements4 = []


        def xfov_change(value):
            self.update_config("aimbot",'x_fov',int(value))
            self.x_fov = int(value)
            #print(f"Slider value: {value}")

        self.xfov_slider = CustomSlider(self.canvas, width=571.0 - 236.0, height=116.0 - 98.0, min_value=0, max_value=200, initial_value=self.x_fov,value_format="integer", on_value_change=xfov_change)
        self.xfov_slider.place(x=236.0, y=98.0)

        def yfov_change(value):
            self.update_config("aimbot",'y_fov',int(value))
            self.y_fov = int(value)
            #print(f"Slider value: {value}")

        self.yfov_slider = CustomSlider(self.canvas, width=571.0 - 236.0, height=153.0 - 135.0, min_value=0, max_value=200, initial_value=self.y_fov,value_format="integer", on_value_change=yfov_change)
        self.yfov_slider.place(x=236.0, y=135.0)

        def xspeed_change(value):
            self.update_config("aimbot",'x_speed',round(value,2))
            self.x_speed = round(value,2)
            #print(f"Slider value: {value}")

        self.xspeed_slider = CustomSlider(self.canvas, width=571.0 - 236.0, height=189.0 - 171.0, min_value=0.01, max_value=2, initial_value=self.x_speed,value_format="raw2", on_value_change=xspeed_change)
        self.xspeed_slider.place(x=236.0, y=171.0)

        def yspeed_change(value):
            self.update_config("aimbot",'y_speed',round(value,2))
            self.y_speed = round(value,2)
            #print(f"Slider value: {value}")

        self.yspeed_slider = CustomSlider(self.canvas, width=571.0 - 236.0, height=226.0 - 208.0, min_value=0.01, max_value=2, initial_value=self.y_speed,value_format="raw2", on_value_change=yspeed_change)
        self.yspeed_slider.place(x=236.0, y=208.0)



        self.enable_aim_text = self.canvas.create_text(
            192.0,
            47.0,
            anchor="nw",
            text="Enable Aim",
            fill="#FFFFFF",
            font=("Inter", 15 * -1)
        )

        self.only_xaxis_text = self.canvas.create_text(
            313.0,
            47.0,
            anchor="nw",
            text="Only Horizontal Axis",
            fill="#FFFFFF",
            font=("Inter", 15 * -1)
        )

        self.enable_rcs_text = self.canvas.create_text(
            497.0,
            47.0,
            anchor="nw",
            text="Recoil Control",
            fill="#FFFFFF",
            font=("Inter", 15 * -1)
        )

        self.xfov_text = self.canvas.create_text(
            174.0,
            98.0,
            anchor="nw",
            text="X-Fov",
            fill="#FFFFFF",
            font=("Inter", 15 * -1)
        )

        self.yfov_text = self.canvas.create_text(
            174.0,
            135.0,
            anchor="nw",
            text="Y-Fov",
            fill="#FFFFFF",
            font=("Inter", 15 * -1)
        )

        self.xspeed_text = self.canvas.create_text(
            156.0,
            171.0,
            anchor="nw",
            text="X-Speed",
            fill="#FFFFFF",
            font=("Inter", 15 * -1)
        )

        self.yspeed_text = self.canvas.create_text(
            156.0,
            207.0,
            anchor="nw",
            text="Y-Speed",
            fill="#FFFFFF",
            font=("Inter", 15 * -1)
        )

        def aimbot_key_change(keyw):
            self.update_config("aimbot","aimbot_hotkey",keyw)
            self.aimbot_hotkey = keyw

        x, y, width, height = 512.0, 235.0, 59.0, 35.0  
        corner_radius = 8 
        fill_color = "#DE2828"  
        self.change_aimkey_button = CustomButton(self.canvas, x, y, width, height, corner_radius, fill_color, self.aimbot_hotkey,aimbot_key_change)

        
        
        self.is_button_aimbot_pressed = self.enable_aimbot
        def toggle_aimact_button():
            self.is_button_aimbot_pressed = not self.is_button_aimbot_pressed
            if self.is_button_aimbot_pressed:
                self.enable_aim_button.config(image=self.pressed_button_cock)
            else:
                self.enable_aim_button.config(image=self.not_pressed_image)
            self.update_config("aimbot", "enable_aimbot",self.is_button_aimbot_pressed)
            self.enable_aimbot = self.is_button_aimbot_pressed

        if self.is_button_aimbot_pressed is True:
            self.cockholder = self.pressed_button_cock
        else:
            self.cockholder = self.not_pressed_image
        
        self.enable_aim_button = tk.Button(
            image=self.cockholder,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: toggle_aimact_button(),
            relief="flat"
        )

        self.enable_aim_button.place(x=166.0,y=47.0,width=16.0,height=16.941177368164062)



        self.is_button_xaxis_pressed = self.x_only
        def toggle_xaxis_button():
            self.is_button_xaxis_pressed = not self.is_button_xaxis_pressed
            if self.is_button_xaxis_pressed:
                self.only_xaxis_button.config(image=self.pressed_button_cock)
            else:
                self.only_xaxis_button.config(image=self.not_pressed_image)
            self.update_config("aimbot", "x_only",self.is_button_xaxis_pressed)
            self.x_only = self.is_button_xaxis_pressed

        if self.is_button_xaxis_pressed is True:
            self.cockholder2 = self.pressed_button_cock
        else:
            self.cockholder2 = self.not_pressed_image

        self.only_xaxis_button = tk.Button(
            image=self.cockholder2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: toggle_xaxis_button(),
            relief="flat"
        )

        self.only_xaxis_button.place(x=288.0,y=47.0,width=16.0,height=16.941177368164062)



        self.is_button_rcs_pressed = self.enable_rcs
        def toggle_rcs_button():
            self.is_button_rcs_pressed = not self.is_button_rcs_pressed
            if self.is_button_rcs_pressed:
                self.rcs_button.config(image=self.pressed_button_cock)
            else:
                self.rcs_button.config(image=self.not_pressed_image)
            self.update_config("aimbot", "enable_rcs",self.is_button_rcs_pressed)
            self.enable_rcs = self.is_button_rcs_pressed

        if self.is_button_rcs_pressed is True:
            self.cockholder3 = self.pressed_button_cock
        else:
            self.cockholder3 = self.not_pressed_image

        self.rcs_button = tk.Button(
            image=self.cockholder3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: toggle_rcs_button(),
            relief="flat"
        )
        self.rcs_button.place(x=473.0,y=47.0,width=16.0,height=16.941177368164062)


        current_elements4.extend([
            self.xfov_slider,
            self.yfov_slider,
            self.xspeed_slider,
            self.yspeed_slider,
            self.enable_aim_text,
            self.only_xaxis_text,
            self.enable_rcs_text,
            self.xfov_text,
            self.yfov_text,
            self.xspeed_text,
            self.yspeed_text,
            self.enable_aim_button,
            self.only_xaxis_button,
            self.rcs_button,
            self.change_aimkey_button



        ])
        self.content_elements['load_content_3'] = current_elements4






    def load_content_2(self):
        print("TRIGGER CLICKED")
        previous_elements = self.content_elements.get('load_content_3', [])
        self.cleanup_previous_content(previous_elements)
        
        self.content_elements['load_content_3'] = []

        current_elements3 = []


        
        def base_delay_change(value):
            self.update_config("triggerbot",'base_delay',round(value,4))
            self.base_delay = round(value,4)
            #print(f"Slider value: {value}")

        self.base_delay_slider = CustomSlider(self.canvas, width=335, height=18, min_value=0.0001, max_value=0.1, initial_value=self.base_delay, value_format="raw", on_value_change=base_delay_change)
        self.base_delay_slider.place(x=241, y=95)
        
        def delay_change(value):
            value2 = value *100
            self.update_config("triggerbot",'trigger_delay',int(value2))
            self.trigger_delay = int(value2)
            #print(f"Slider value: {int(value2)}")

        self.delay_slider = CustomSlider(self.canvas, width=335, height=18, min_value=0, max_value=1, initial_value=self.trigger_delay /100, value_format="percentage", on_value_change=delay_change)
        self.delay_slider.place(x=241, y=128)

        def tolerance_change(value):
            self.update_config("triggerbot",'color_tolerance',int(value))
            self.color_tolerance = int(value)
            #print(f"Slider value: {value}")

        self.tolernace_slider = CustomSlider(self.canvas, width=335, height=18, min_value=1, max_value=100, initial_value=self.color_tolerance, value_format="integer", on_value_change=tolerance_change)
        self.tolernace_slider.place(x=241, y=163)

        self.enable_trigger_text = self.canvas.create_text(
            177.0,
            46.0,
            anchor="nw",
            text="Enable Trigger",
            fill="#FFFFFF",
            font=("Inter", 15 * -1)
        )

        self.always_enabled_text = self.canvas.create_text(
            316.0,
            46.0,
            anchor="nw",
            text="Always Enabled",
            fill="#FFFFFF",
            font=("Inter", 15 * -1)
        )

        self.base_delay_text = self.canvas.create_text(
            152.0,
            95.0,
            anchor="nw",
            text="Base Delay",
            fill="#FFFFFF",
            font=("Inter", 15 * -1)
        )

        self.delay_text = self.canvas.create_text(
            191.0,
            128.0,
            anchor="nw",
            text="Delay",
            fill="#FFFFFF",
            font=("Inter", 15 * -1)
        )

        self.tolernace_text = self.canvas.create_text(
            161.0,
            161.0,
            anchor="nw",
            text="Tolerance",
            fill="#FFFFFF",
            font=("Inter", 15 * -1)
        )

        self.is_button_trigger_pressed = self.enable_triggerbot
        def toggle_trigger_button():
            self.is_button_trigger_pressed = not self.is_button_trigger_pressed
            if self.is_button_trigger_pressed:
                self.trigger_button.config(image=self.button_pressed_image)
            else:
                self.trigger_button.config(image=self.trigger_button_image)
            self.update_config("triggerbot", "enable_triggerbot",self.is_button_trigger_pressed)
            self.enable_triggerbot = self.is_button_trigger_pressed

        if self.is_button_trigger_pressed is True:
            self.placeholder_var2 = self.button_pressed_image
        else:
            self.placeholder_var2 = self.trigger_button_image
        
        self.trigger_button = tk.Button(
            image=self.placeholder_var2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: toggle_trigger_button(),
            relief="flat"
        )
        self.trigger_button.place(x=151.0, y=46.0, width=16.0, height=16.941177368164062)


        
        self.is_button_always_on_pressed = self.always_enabled
        def toggle_trigger_mode():
            self.is_button_always_on_pressed = not self.is_button_always_on_pressed
            if self.is_button_always_on_pressed:
                self.always_enabled_button.config(image=self.button_pressed2)
            else:
                self.always_enabled_button.config(image=self.always_enabled_button_image)
            self.update_config("triggerbot", "always_enabled",self.is_button_always_on_pressed)
            self.always_enabled = self.is_button_always_on_pressed

        if self.is_button_always_on_pressed is True:
            self.placeholder_var3 = self.button_pressed2
        else:
            self.placeholder_var3 = self.always_enabled_button_image
        

        self.always_enabled_button = tk.Button(
            image=self.placeholder_var3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: toggle_trigger_mode(),
            relief="flat"
        )
        self.always_enabled_button.place(x=290.0, y=46.0, width=16.0, height=16.941177368164062)




        def trigger_key_change(keyw):
            self.update_config("triggerbot","trigger_hotkey",keyw)
            self.trigger_hotkey = keyw

        x, y, width, height = 517.0, 192.0, 59.0, 35.0  
        corner_radius = 8  
        fill_color = "#DE2828"  
        self.change_hotkey_button = CustomButton(self.canvas, x, y, width, height, corner_radius, fill_color, self.trigger_hotkey,trigger_key_change)


        current_elements3.extend([
            self.base_delay_slider,
            self.delay_slider,
            self.tolernace_slider,
            self.enable_trigger_text,
            self.always_enabled_text,
            self.base_delay_text,
            self.delay_text,
            self.tolernace_text,
            self.trigger_button,
            self.always_enabled_button,
            self.change_hotkey_button,



        ])
        self.content_elements['load_content_3'] = current_elements3


        

    def load_content_3(self): 
        print("INSTANT LOCK CLICKED")
        previous_elements = self.content_elements.get('load_content_3', [])
        self.cleanup_previous_content(previous_elements)
        self.content_elements.get('load_content_3', [].clear())
        current_elements2 = []


        self.lock_image1 = self.canvas.create_image(
            228.0,
            110.0,
            image=self.image_lock_image1
        )

        

        def region_update(event):
            self.region = self.region_entry.get()
            self.update_config("instantlocker","region",self.region)

        self.region_entry = tk.Entry(
            bd=0,
            bg="#14161B",
            fg="#ffffff",
            highlightthickness=0
        )
        self.region_entry.place(
            x=160.0,
            y=96.0,
            width=133.0,
            height=27.0
        )
        self.region_entry.insert(0,self.region)
        self.region_entry.bind("<KeyRelease>", region_update)


        self.lock_image2 = self.canvas.create_image(
            228.0,
            163.0,
            image=self.image_lock_image2
        )

        

        def agent_update(event):
            self.preferred_agent = self.agent_entry.get()
            self.update_config("instantlocker","preferred_agent",self.preferred_agent)

        self.agent_entry = tk.Entry(
            bd=0,
            bg="#14161B",
            fg="#ffffff",
            highlightthickness=0
        )
        self.agent_entry.place(
            x=160.0,
            y=146.0,
            width=133.0,
            height=30.0
        )
        self.agent_entry.insert(0,self.preferred_agent)
        self.agent_entry.bind("<KeyRelease>", agent_update)


        self.il_text = self.canvas.create_text(
            177.0,
            46.0,
            anchor="nw",
            text="Enable Instant Locker",
            fill="#FFFFFF",
            font=("Inter", 15 * -1)
        )
        current_elements2.extend([
        self.lock_image1,
        self.region_entry,
        self.lock_image2,
        self.agent_entry,
        self.il_text,
    ])

        self.is_button_pressed = self.enable_instantlocker

        def toggle_button_state():
            self.is_button_pressed = not self.is_button_pressed
            if self.is_button_pressed:
                self.lock_button.config(image=self.button_lock_image1_pressed)
            else:
                self.lock_button.config(image=self.button_lock_image1_normal)
            self.update_config("instantlocker", "enable_instantlocker",self.is_button_pressed)
            self.enable_instantlocker = self.is_button_pressed

        if self.is_button_pressed is True:
            self.placeholder_var = self.button_lock_image1_pressed
        else:
            self.placeholder_var = self.button_lock_image1_normal
        self.lock_button = tk.Button(
            image=self.placeholder_var,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: toggle_button_state(),
            relief="flat"
        )
        self.lock_button.place(
            x=151.0,
            y=47.94117736816406,
            width=16.0,
            height=16.058822631835938
        )
        
        current_elements2.append(self.lock_button)

        self.content_elements['load_content_3'] = current_elements2



    
    def load_content_4(self):
        print("Settings clicked")
        previous_elements = self.content_elements.get('load_content_3', [])
        self.cleanup_previous_content(previous_elements)
        self.content_elements.get('load_content_3', [].clear())
        current_elements = []
    
        #self.settings_1 = self.canvas.create_image(
        #    205.0,
        #    284.0,
        #    image=self.image_settings_1
        #)
        

        #self.com_entry = tk.Entry(
        #    self.canvas,
        #    bd=0,
        #    bg="#14161B",
        #    fg="#ffffff",
        #    highlightthickness=0
        #)

        #def comport_update(event):
        #    self.com_port = self.com_entry.get()
        #    self.update_config("arduino_settings","com_port",self.com_port)

        #self.com_entry.place(
        #    x=147.0,
        #    y=277.0,
        #    width=110.0,
        #    height=12.0
        #)
        #self.com_entry.insert(0, self.com_port)
        #self.com_entry.bind("<KeyRelease>", comport_update)

        
        
        
        #self.settings_2 = self.canvas.create_image(
        #    205.0,
        #    321.0,
        #    image=self.image_settings_2
        #)
        
        
        
        #def serial_update(event):
        #    self.serial_id = self.serial_entry.get()
        #    self.update_config("arduino_settings","serial_id",self.serial_id)

        #self.serial_entry = tk.Entry(
        #    self.canvas,
        #    bd=0,
        #    bg="#14161B",
        #    fg="#ffffff",
        #    highlightthickness=0
        #)
        #self.serial_entry.place(
        #    x=147.0,
        #    y=315.0,
        #    width=110.0,
        #    height=9.0
        #)
        #self.serial_entry.insert(0, self.serial_id)
        #self.serial_entry.bind("<KeyRelease>", serial_update)

        
        self.settings_3 = self.canvas.create_image(
            208.0,
            245.0,
            image=self.image_settings_3
        )

        
        self.config_name_entry = tk.Entry(
            bd=0,
            bg="#14161B",
            fg="#ffffff",
            highlightthickness=0
        )
        self.config_name_entry.place(
            x=149.0,
            y=235.0,
            width=123.0,
            height=19.0
        )
        self.config_name_entry.insert(0,self.config_path)
        

        self.settings_4 = self.canvas.create_image(
            373.0,
            127.0,
            image=self.image_settings_4
        )

        self.config_list = self.canvas.create_text(
            148.75051879882812,
            47.49467468261719,
            anchor="nw",
            text=self.list_json_files_in_folder(),
            fill="#FFFFFF",
            font=("Inter", 13 * -1)
        )

        def delete_file(file_path):
            try:
                os.remove(file_path)
                print(f"File '{file_path}' has been successfully deleted.")
            except OSError as e:
                print(f"Error deleting file '{file_path}': {e}")
                print("retard")
            self.canvas.itemconfig(self.config_list,text=self.list_json_files_in_folder())
            pass

        def save_json_file(source_file, destination_file):
            try:
                with open(source_file, 'r') as source:
                    data = json.load(source)

                with open(destination_file, 'w') as destination:
                    json.dump(data, destination, indent=4) 

                print(f"JSON content copied from '{source_file}' to '{destination_file}' successfully.")
            except Exception as e:
                print(f"Error copying JSON file: {e}")
            self.canvas.itemconfig(self.config_list,text=self.list_json_files_in_folder())

        self.button_1 = tk.Button(
            self.canvas,
            image=self.button_settings_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.change_config(self.config_name_entry.get()),
            relief="flat"
        )
        self.button_1.place(
            x=394.0,
            y=229.0,
            width=99.0,
            height=36.0
        )
        self.button_2 = tk.Button(
            image=self.button_settings_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: save_json_file(self.config_path,self.config_name_entry.get()),
            relief="flat"
        )
        self.button_2.place(
            x=286.0,
            y=229.0,
            width=99.0,
            height=36.0
        )


        self.button_3 = tk.Button(
            image=self.button_settings_3,
            borderwidth=0,
            highlightthickness=0,   
            command=lambda: delete_file(self.config_name_entry.get()),
            relief="flat"
        )
        self.button_3.place(
            x=509.0,
            y=229.0,
            width=99.0,
            height=36.0
        )
        current_elements.extend([
        #self.settings_1,
        #self.settings_2,
        self.settings_3,
        self.settings_4,
        #self.com_entry,
        #self.serial_entry,
        self.config_name_entry,
        self.button_1,
        self.button_2,
        self.button_3,
        self.config_list
    ])
        self.content_elements["load_content_3"] = current_elements
    
            


class LoginGUI():
    def __init__(self, root):
        self.root = root
        self.drag_region = (0, 0, 426, 20)
        self._drag_data = {"x": 0, "y": 0, "dragging": False}
        self.root.bind("<ButtonPress-1>", self.startmove)
        self.root.bind("<ButtonRelease-1>", self.stopmove)
        self.root.bind("<B1-Motion>", self.onmove)


        self.root.geometry("426x350")
        self.root.configure(bg="#0F1014")

        self.canvas = tk.Canvas(
            self.root,
            bg="#0F1014",
            height=350,
            width=426,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.pack()

        self.status_label = tk.Label(
            self.canvas,
            text="",
            bg="#0F1014",
            fg="#FFFFFF",
            font=("Inter", 12),
            anchor="center"
        )
        self.status_label.place(relx=0.5, rely=1.0, anchor="s")
        image_data = self.get_image_from_url("https://i.ibb.co/nLWDRVH/image-1.png")
        self.image_image_1 = ImageTk.PhotoImage(image_data)
        self.image_1 = self.canvas.create_image(
            37.0,
            38.0,
            image=self.image_image_1
        )

        self.canvas.create_rectangle(
            8.0,
            73.0,
            419.0,
            75.0,
            fill="#DE2727",
            outline=""
        )

        self.canvas.create_text(
            115.0,
            23.0,
            anchor="nw",
            text="Nephritis Private",
            fill="#959596",
            font=("Inter", 25 * -1)
        )
        image_data = requests.get("https://i.ibb.co/Dg09BnV/button-1.png").content
        
        image = Image.open(BytesIO(image_data))
        self.button_image_1 = ImageTk.PhotoImage(image)
        self.button_1 = tk.Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.login,
            relief="flat"
        )
        self.button_1.place(
            x=152.0,
            y=178.0,
            width=123.0,
            height=50.0
        )

        image_data = requests.get("https://i.ibb.co/pzsjcv0/button-2.png").content

        
        image = Image.open(BytesIO(image_data))
        self.button_image_2 = ImageTk.PhotoImage(image)
        self.button_2 = tk.Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: exiting(),
            relief="flat"
        )
        self.button_2.place(
            x=152.0,
            y=236.0,
            width=123.0,
            height=50.0
        )

        image2_data = self.get_image_from_url("https://i.ibb.co/g7PtK7w/image-2.png")
        self.image_image_2 = ImageTk.PhotoImage(image2_data)
        self.image_2 = self.canvas.create_image(
            213.0,
            126.0,
            image=self.image_image_2
        )
        image3_data = self.get_image_from_url("https://i.ibb.co/2YyJxky/image-3.png")
        self.image_image_3 = ImageTk.PhotoImage(image3_data)
        self.image_3 = self.canvas.create_image(
            75.0,
            127.0,
            image=self.image_image_3
        )
        entry_data = self.get_image_from_url("https://i.ibb.co/vxH5477/entry-1.png")
        self.entry_image_1 = ImageTk.PhotoImage(entry_data)
        self.entry_bg_1 = self.canvas.create_image(
            222.0,
            127.0,
            image=self.entry_image_1
        )
        license_value = self.load_license_value()

        self.entry_1 = tk.Entry(
            self.canvas,
            bd=0,
            bg="#14161B",
            fg="#ffffff",
            highlightthickness=0
        )
        self.entry_1.place(
            x=87.0,
            y=111.0,
            width=270.0,
            height=30.0
        )
        self.entry_1.insert(tk.END, license_value)


    def get_image_from_url(self, url):
        response = requests.get(url)
        image_data = response.content
        return Image.open(BytesIO(image_data))


    def startmove(self, event):
        if self.is_inside_drag_region(event.x, event.y):
            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y
            self._drag_data["dragging"] = True

    def stopmove(self, event):
        self._drag_data["dragging"] = False

    def onmove(self, event):
        if self._drag_data["dragging"]:
            x, y = event.x - self._drag_data["x"], event.y - self._drag_data["y"]
            self.root.geometry(f"+{self.root.winfo_x() + x}+{self.root.winfo_y() + y}")
    
    def is_inside_drag_region(self, x, y):
        # check if coords inside drag region
        x1, y1, x2, y2 = self.drag_region
        return x1 <= x <= x2 and y1 <= y <= y2

    def load_license_value(self):
        config_file = r"files\license.json" 
        try:
            with open(config_file, "r") as file:
                config_data = json.load(file)
                return config_data.get("license", "")
        except:
            return ""
    def write_license_value(self, license_value):
        config_file = r"files\license.json"  
        with open(config_file, "r") as file:
            config_data = json.load(file)

        if len(config_data.get("license", "")) == 0:
            config_data["license"] = license_value
            with open(config_file, "w") as file:
                json.dump(config_data, file, indent=4)
                # Write the updated data back to the config file
        else:
            pass

    #def get_hwid(self):
    #    self.c = wmi.WMI()
    #    self.system_uuid = self.c.Win32_ComputerSystemProduct()[0].UUID
    #    return self.system_uuid
            
    def login(self):
        self.canvas.update_idletasks()
        self.license_key = self.entry_1.get()
        
        self.status_label.config(text=f"Successfully verified license, loading cheeto...", fg="#4ee44e", bg="#0F1014")
        self.canvas.update_idletasks()
        time.sleep(3)
        self.root.destroy()
        load_gui()
                                
def load_gui():
    rooot = tk.Tk()
    app = CheatGUI(rooot)
    rooot.overrideredirect(True)
    rooot.attributes('-topmost', True)

    rooot.mainloop()


#if __name__ == "__main__":
#    load_gui()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginGUI(root)
    root.resizable(False, False)
    root.overrideredirect(True)

    # Set the window as topmost
    root.attributes('-topmost', True)
    root.mainloop()
