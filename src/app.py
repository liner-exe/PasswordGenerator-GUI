# ------------------------------------------------- IMPORTS --------------------------------------------------------- #

try:
    import customtkinter as ctk
except ImportError:
    import subprocess
    import sys

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
        import customtkinter as ctk
    except subprocess.CalledProcessError:
        print("Failed to install customtkinter. Please install it manually.")
        sys.exit(1)
    except ImportError:
        print("customtkinter is not installed and installation failed. Please install it manually.")
        sys.exit(1)


import platform
import random
import string
import configparser
import os
import pyautogui
import webbrowser
from PIL import ImageTk
from utils.i18n import Response

path = os.path.dirname(os.path.realpath(__file__))

# ------------------------------------------------- APP CLASS ---------------------------------------------------- #
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ------------------------------------------- APP SETTINGS ------------------------------------------------- #
        self.resolution_width = pyautogui.resolution().width
        self.resolution_height = pyautogui.resolution().height

        try:
            settings = configparser.ConfigParser()
            settings.read(f'{path}/settings.ini')
            
            self.geometry(str(settings['window']['geometry']))
            ctk.set_widget_scaling(float(settings['window']['widget_scaling']))
            ctk.set_window_scaling(float(settings['window']['window_scaling']))
            self.minsize(int(settings['window']['minsize'].split('x')[0]), int(settings['window']['minsize'].split('x')[1]))

            ctk.set_appearance_mode(settings['appearance']['theme_color'])
            ctk.set_default_color_theme(settings['appearance']['theme_accent'])

        except KeyError:
            settings['window'] = {
                'geometry': f'{(self.resolution_width) // 2}x{self.resolution_height // 2}+{self.resolution_width // 8}+{self.resolution_height // 8}',
                'window_scaling': 1.0,
                'widget_scaling': 1.0,
                'minsize': f'{self.resolution_width // 4}x{self.resolution_height // 4}'
            }
            settings['appearance'] = {
                'theme_color': 'system',
                'theme_accent': 'green'
            }
            settings['app'] = {
                'locale': 'en-us'
            }
            
            with open(f'{path}/settings.ini', 'w') as configfile:
                settings.write(configfile)

            self._set_appearance_mode(settings['appearance']['theme_color'])
            ctk.set_default_color_theme(settings['appearance']['theme_accent'])
            self.geometry(settings['window']['geometry'])
            self.minsize(int(settings['window']['minsize'].split('x')[0]), int(settings['window']['minsize'].split('x')[1]))
            ctk.set_widget_scaling(float(settings['window']['widget_scaling']))
            ctk.set_window_scaling(float(settings['window']['window_scaling']))

        self.response = Response(f"{path}/i18n", settings['app']['locale'])

        self.title(f'{self.response.get("app-title")} v2.0.0')
        self.iconbitmap(f'{path}/icon.ico')

        self.settings = configparser.ConfigParser()
        self.settings.read(f'{path}/settings.ini')

        fontname = 'Arial'
        if platform.system() == 'Linux':
            fontname = 'ubuntu'

        # ------------------------------------------- SETTINGS VARIABLES -------------------------------------------- #
            
        self.app_locale = settings['app']['locale']
        self.widget_scaling = settings['window']['widget_scaling']
        self.window_scaling = settings['window']['window_scaling']
        self.theme_color = settings['appearance']['theme_color']
        self.theme_accent = settings['appearance']['theme_accent']

        # ------------------------------------------- PASSWORD FRAME ------------------------------------------------ #

        self.password_frame = ctk.CTkFrame(self, fg_color=('#ffffff', '#323332'), bg_color=('#ffffff', '#323332'),
                                           corner_radius=0)
        self.password_frame.pack(fill='both', side='top', expand=True)

        self.password = ctk.CTkEntry(self.password_frame, width=500, font=(fontname, 24))
        self.password.grid(row=0, column=0, columnspan=5, padx=10, pady=10, stick='we')

        self.password_length = 6

        self.password_label = ctk.CTkLabel(self.password_frame, text=self.response.get("password-length"))
        self.password_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

        self.length_slider = ctk.CTkSlider(self.password_frame, from_=6, to=30,
                                           variable=ctk.IntVar(value=self.password_length),
                                           width=120,
                                           number_of_steps=24, command=self.update_password_length)
        self.length_slider.grid(row=1, column=1, columnspan=2, sticky='we', padx=10, pady=10)

        self.length_display = ctk.CTkLabel(self.password_frame, text=str(self.password_length), font=(fontname, 20))
        self.length_display.grid(row=1, column=3, padx=(0, 10), pady=10, sticky='w')

        # -------------------------------- BUTTONS (GENERATE, CLEAR, COPY) ------------------------------------------ #

        self.buttons = ctk.CTkFrame(self, corner_radius=0)
        self.buttons.pack(fill='both', side='left', expand=True)

        self.generate = ctk.CTkButton(self.buttons, text=self.response.get("button-generate"), font=(fontname, 15),
                                      command=self.generate_password)
        self.generate.grid(row=0, column=0, pady=10)

        self._clear = ctk.CTkButton(self.buttons, text=self.response.get("button-clear"), font=(fontname, 15), command=self.clear)
        self._clear.grid(row=1, column=0, pady=10)

        self.copy = ctk.CTkButton(self.buttons, text=self.response.get("button-copy"), font=(fontname, 15), command=self.copy_to_clipboard)
        self.copy.grid(row=2, column=0, pady=10, padx=10)

        # ------------------------------------------- SYMBOL SWITCHES ---------------------------------------------- #

        self.switches = ctk.CTkFrame(self, corner_radius=0)
        self.switches.pack(side='right', anchor='e')
        self.switches.pack(fill='both', side='left', expand=True)

        self.digits = ctk.CTkSwitch(self.switches, width=50, height=20, switch_width=40, switch_height=20,
                                    text=self.response.get("switch-digits"), font=(fontname, 20))
        self.digits.toggle()
        self.digits.grid(row=0, column=0, pady=5, padx=10, sticky='W')

        self.lowers = ctk.CTkSwitch(self.switches, width=50, height=20, switch_width=40, switch_height=20,
                                    text=self.response.get("switch-lowercase"), font=(fontname, 20))
        self.lowers.toggle()
        self.lowers.grid(row=1, column=0, pady=5, padx=10, sticky='W')

        self.uppers = ctk.CTkSwitch(self.switches, width=50, height=20, switch_width=40, switch_height=20,
                                    text=self.response.get("switch-uppercase"), font=(fontname, 20))
        self.uppers.toggle()
        self.uppers.grid(row=2, column=0, pady=5, padx=10, sticky='W')

        self.punctuation = ctk.CTkSwitch(self.switches, width=50, height=20, switch_width=40, switch_height=20,
                                         text=self.response.get("switch-punctuation"), font=(fontname, 20))
        self.punctuation.toggle()
        self.punctuation.grid(row=3, column=0, pady=5, padx=10, sticky='W')

        # -------------------------------------------- SETTINGS ----------------------------------------------------- #

        self.settings_frame = ctk.CTkFrame(self, corner_radius=0)
        self.settings_frame.pack(side='right', fill='both')

        self.settings_button = ctk.CTkButton(self.settings_frame, text=self.response.get("button-settings"), command=self.open_settings)
        self.settings_button.pack(padx=10, pady=10, anchor='center')

        # -------------------------------------------- ABOUT -------------------------------------------------------- #

        self.about_button = ctk.CTkButton(self.settings_frame, text=self.response.get("button-about"), command=self.open_about)
        self.about_button.pack(padx=10, pady=10, anchor='center')

    # ---------------------------------------------- FUNCTIONS -----------------------------------------------------#

    def generate_password(self):
        self.password.delete(0, ctk.END)
        symbols = ""
        if int(self.digits.get()) == 1:
            symbols += string.digits
        if int(self.lowers.get()) == 1:
            symbols += string.ascii_lowercase
        if int(self.uppers.get()) == 1:
            symbols += string.ascii_uppercase
        if int(self.punctuation.get()) == 1:
            symbols += string.punctuation

        try:
            password = ''
            for i in range(int(self.password_length)):
                password += random.choice(symbols)

            self.password.insert(index=0, string=password)

        except IndexError:
            self.open_error_window(self.response.get("error-message"))
        except Exception as err:
            print(err)

    def clear(self):
        self.password.delete(0, ctk.END)

    def copy_to_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.password.get())

    def open_error_window(self, error_text: str):
        error_window1 = ctk.CTkToplevel()
        error_window1.iconbitmap(f'{path}/icon.ico')
        error_window1.title(self.response.get("error-title"))
        error_window1.attributes('-topmost', True)
        error_window1.geometry(f'800x150+{(self.resolution_width - 700) // 2}+{(self.resolution_height - 400) // 2}')
        error_window1.resizable(False, False)
        error_window1.after(1500, error_window1.destroy)

        label = ctk.CTkLabel(error_window1, text=error_text, text_color='red',
                             font=('ubuntu' if platform.system() == 'Linux' else 'Arial', 20))
        label.pack()

    def open_settings(self):
        settings = ctk.CTkToplevel()
        settings.title(self.response.get("title-settings"))
        settings.attributes('-topmost', True)
        settings.resizable(False, False)
        settings.geometry(f'{int(450*float(self.settings["window"]["widget_scaling"]))}x{int(400*float(self.settings["window"]["widget_scaling"]))}'\
                          f'+{(self.resolution_width - 400) // 2}+{(self.resolution_height - 400) // 2}')

        customization = ctk.CTkFrame(settings)
        customization.pack(padx=20, pady=20, side='top', fill='both', expand=True)

        scale_window_label = ctk.CTkLabel(customization, text=self.response.get("dropdown-window-scaling"))
        scale_window_label.grid(row=0, column=0)

        scale_window_dropdown = ctk.CTkComboBox(customization,
                                                values=['100%', '150%', '200%'],
                                                command=lambda value: setattr(self, 'window_scaling', str(float(value.replace('%', '')) / 100.0)),
                                                font=('ubuntu' if platform.system() == 'Linux' else 'Arial', 20))

        window_scale_value = round(float(self.window_scaling) * 100)
        scale_window_dropdown.set(f'{window_scale_value}%')
        scale_window_dropdown.grid(row=1, column=0)

        scale_label = ctk.CTkLabel(customization, text=self.response.get("dropdown-widget-scaling"))
        scale_label.grid(row=2, column=0)

        scale_dropdown = ctk.CTkComboBox(customization,
                                         values=['100%', '150%', '200%'],
                                         command=lambda value: setattr(self, 'widget_scaling', str(float(value.replace('%', '')) / 100.0)),
                                         font=('ubuntu' if platform.system() == 'Linux' else 'Arial', 20))

        widget_scale_value = round(float(self.widget_scaling) * 100)
        scale_dropdown.set(f'{widget_scale_value}%')
        scale_dropdown.grid(row=3, column=0)

        amode_label = ctk.CTkLabel(customization, text=self.response.get("dropdown-theme-color"))
        amode_label.grid(row=4, column=0)

        amode_dropdown = ctk.CTkComboBox(customization,
                                         values=['dark', 'white', 'system'],
                                         command=lambda mode: lambda value: setattr(self, 'theme_color', value),
                                         font=('ubuntu' if platform.system() == 'Linux' else 'Arial', 20))
        
        amode_dropdown.set(self.theme_color)
        amode_dropdown.grid(row=5, column=0)

        accent_label = ctk.CTkLabel(customization, text=self.response.get("dropdown-theme-accent"))
        accent_label.grid(row=0, column=1, padx=50)

        accent_dropdown = ctk.CTkComboBox(customization,
                                         values=['green', 'blue', 'dark-blue'],
                                         command=lambda value: setattr(self, 'theme_accent', value),
                                         font=('ubuntu' if platform.system() == 'Linux' else 'Arial', 20))
        
        accent_dropdown.set(self.theme_accent)
        accent_dropdown.grid(row=1, column=1, padx=50)

        accent_label = ctk.CTkLabel(customization, text=self.response.get("dropdown-locale"))
        accent_label.grid(row=2, column=1, padx=50)

        locale_dropdown = ctk.CTkComboBox(customization,
                                         values=['en-us', 'ru-ru'],
                                         command=lambda value: setattr(self, 'app_locale', value),
                                         font=('ubuntu' if platform.system() == 'Linux' else 'Arial', 20))
        
        locale_dropdown.set(self.app_locale)
        locale_dropdown.grid(row=3, column=1, padx=50)

        save_button = ctk.CTkButton(settings, text=self.response.get("button-save"), command=self.save_settings)
        save_button.place(x=50, y=300)

        close_button = ctk.CTkButton(settings, text=self.response.get("button-close"), command=settings.destroy)
        close_button.place(x=210, y=300)                  


    def save_settings(self):
        config = configparser.ConfigParser()
        settings_file = f'{path}/settings.ini'

        if os.path.exists(settings_file):
            config.read(settings_file)

        config['app']['locale'] = self.app_locale
        config['window']['widget_scaling'] = self.widget_scaling
        config['window']['window_scaling'] = self.window_scaling
        config['appearance']['theme_color'] = self.theme_color
        config['appearance']['theme_accent'] = self.theme_accent

        with open(settings_file, 'w') as configfile:
            config.write(configfile)

        saved = ctk.CTkToplevel()
        saved.title(self.response.get("save-title"))
        saved.attributes('-topmost', True)
        saved.geometry(f'700x300+{(self.resolution_width - 800) // 2}+200')
        saved.resizable(False, False)
        saved.after(1000, saved.destroy)

        saved_label_text = self.response.get("save-message")
        saved_label = ctk.CTkLabel(saved, text=saved_label_text, font=('ubuntu' if platform.system() == 'Linux' else 'Arial', 20))
        saved_label.pack(padx=30)

    def open_about(self):
        about = ctk.CTkToplevel()
        about.title(self.response.get("about-title"))
        about.resizable(False, False)

        width = 800
        height = 500
        offset_x = self.resolution_width // 2 - width // 2
        offset_y = self.resolution_height // 2 - height // 2
        about.geometry(f'{width}x{height}+{offset_x}+{offset_y}')
        about.attributes('-topmost', True)

        about_frame = ctk.CTkFrame(about)
        about_frame.pack(padx=20, pady=20, side='top', fill='both', expand=True)

        filler_left = ctk.CTkLabel(about_frame, text="", font=('ubuntu' if platform.system() == 'Linux' else 'Arial', 20))
        filler_left.pack(side="top")

        filler_right = ctk.CTkLabel(about_frame, text="", font=('ubuntu' if platform.system() == 'Linux' else 'Arial', 20))
        filler_right.pack(side="top")

        about_label = ctk.CTkLabel(about_frame, text=self.response.get("about-label"),
                                   font=('ubuntu' if platform.system() == 'Linux' else 'Arial', 20))
        about_label.pack(side="top")

        github_label = ctk.CTkLabel(about_frame, text=self.response.get("about-open-github"), text_color="blue", cursor="hand2",
                                  font=('ubuntu' if platform.system() == 'Linux' else 'Arial', 20))
        github_label.pack(side="top")
        github_label.bind("<Button-1>", lambda e: self.url_open("https://github.com/r-liner/"))

        project_label = ctk.CTkLabel(about_frame, text=self.response.get("about-open-repository"), text_color="blue", cursor="hand2",
                                  font=('ubuntu' if platform.system() == 'Linux' else 'Arial', 20))
        project_label.pack(side="top")
        project_label.bind("<Button-1>", lambda e: self.url_open("https://github.com/r-liner/PasswordGenerator-GUI"))

        latest_label = ctk.CTkLabel(about_frame, text=self.response.get("about-see-latest"), text_color="blue", cursor="hand2",
                                  font=('ubuntu' if platform.system() == 'Linux' else 'Arial', 20))
        latest_label.pack(side="top")
        latest_label.bind("<Button-1>", lambda e: self.url_open("https://github.com/r-liner/PasswordGenerator-GUI/releases/latest"))

        close_button = ctk.CTkButton(about, text=self.response.get("button-close"), command=about.destroy)
        close_button.pack(pady=30)

    def update_password_length(self, value):
        value = int(value)
        self.password_length = value
        self.length_display.configure(text=value)

    def url_open(self, url):
        webbrowser.open_new(url)


if __name__ == "__main__":
    app = App()
    app.mainloop()
