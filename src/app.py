# ------------------------------------------------- IMPORTS --------------------------------------------------------- #


try:
    import customtkinter as ctk

except:
    import subprocess
    subprocess.check_call(["pip3", "install", "customtkinter"])

    import customtkinter as ctk


import string
import random
import platform


# ------------------------------------------------- APP CLASS ---------------------------------------------------- #
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ------------------------------------------- APP SETTINGS ------------------------------------------------- #
        platform_name = platform.system()

        self.title(f'Password Generator v1.2 | for {platform_name}')
        self._set_appearance_mode('dark')
        ctk.set_default_color_theme('green')
        self.geometry('1070x640+200+200')
        self.minsize(1070, 640)
        ctk.set_widget_scaling(2.0)

        fontname = 'Arial'
        if platform.system() == 'Linux':
            fontname = 'ubuntu'

        # ------------------------------------------- PASSWORD FRAME ------------------------------------------------ #

        self.password_frame = ctk.CTkFrame(self, fg_color=('#ffffff', '#323332'), bg_color=('#ffffff', '#323332'),
                                           corner_radius=0)
        self.password_frame.columnconfigure(all([0, 1]), minsize=40, weight=1)
        self.password_frame.rowconfigure(all([i for i in range(8)]), minsize=20)
        self.password_frame.pack(fill='both', side='top', expand=True)

        self.password = ctk.CTkEntry(self.password_frame, width=600, font=(fontname, 24))
        self.password.grid(row=0, column=0, stick='we', pady=10, sticky='n')

        self.length = ctk.CTkEntry(self.password_frame, 250, 30, placeholder_text="Enter password length",
                                   font=(fontname, 20))
        self.length.grid(row=1, column=0, columnspan=2, pady=10, sticky='s')

        # -------------------------------- BUTTONS (GENERATE, CLEAR, COPY) ------------------------------------------ #

        self.buttons = ctk.CTkFrame(self, corner_radius=0)
        self.buttons.pack(fill='both', side='left', expand=True)

        self.generate = ctk.CTkButton(self.buttons, text="GENERATE", font=(fontname, 15),
                                      command=self.generate_password)
        self.generate.grid(row=0, column=0, pady=10)

        self.generate = ctk.CTkButton(self.buttons, text="CLEAR", font=(fontname, 15), command=self.clear)
        self.generate.grid(row=1, column=0, pady=10)

        self.copy = ctk.CTkButton(self.buttons, text="COPY", font=(fontname, 15), command=self.copy_to_clipboard)
        self.copy.grid(row=2, column=0, pady=10, padx=10)

        # ------------------------------------------- SYMBOL SWITCHES ---------------------------------------------- #

        self.switches = ctk.CTkFrame(self, corner_radius=0)
        self.switches.pack(side='right', anchor='e')
        self.switches.pack(fill='both', side='left', expand=True)

        self.digits = ctk.CTkSwitch(self.switches, width=50, height=20, switch_width=40, switch_height=20,
                                    text="digits", font=(fontname, 20))
        self.digits.grid(row=0, column=0, pady=5, padx=10, sticky='W')

        self.lowers = ctk.CTkSwitch(self.switches, width=50, height=20, switch_width=40, switch_height=20,
                                    text="lowercase", font=(fontname, 20))
        self.lowers.grid(row=1, column=0, pady=5, padx=10, sticky='W')

        self.uppers = ctk.CTkSwitch(self.switches, width=50, height=20, switch_width=40, switch_height=20,
                                    text="uppercase", font=(fontname, 20))
        self.uppers.grid(row=2, column=0, pady=5, padx=10, sticky='W')

        self.punctuation = ctk.CTkSwitch(self.switches, width=50, height=20, switch_width=40, switch_height=20,
                                         text="punctuation", font=(fontname, 20))
        self.punctuation.grid(row=3, column=0, pady=5, padx=10, sticky='W')

        # -------------------------------------------- SETTINGS ----------------------------------------------------- #

        self.settings_frame = ctk.CTkFrame(self, corner_radius=0)
        self.settings_frame.pack(side='right', fill='both')

        self.settings_button = ctk.CTkButton(self.settings_frame, text='SETTINGS', command=self.open_settings)
        self.settings_button.pack(padx=10, pady=10, anchor='center')

        # -------------------------------------------- ABOUT -------------------------------------------------------- #

        self.about_button = ctk.CTkButton(self.settings_frame, text='ABOUT', command=self.open_about)
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
            for i in range(int(self.length.get())):
                password += random.choice(symbols)

            self.password.insert(index=0, string=password)

        except ValueError:
            self.open_error_window('ERROR. Empty password length.')
        except IndexError:
            self.open_error_window('ERROR. Character switches are not used.')
        except Exception as err:
            print(err)

    def clear(self):
        self.password.delete(0, ctk.END)

    def copy_to_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.password.get())

    @staticmethod
    def open_error_window(error_text: str):
        error_window1 = ctk.CTkToplevel()
        error_window1.title('ERROR')
        error_window1.attributes('-topmost', True)
        error_window1.geometry('700x400+0+0')

        label = ctk.CTkLabel(error_window1, text=error_text, text_color='red',
                             font=('ubuntu' if platform.system() == 'Linux' else 'Arial', 20))
        label.pack()
        button = ctk.CTkButton(error_window1, text='CLOSE', command=error_window1.destroy)
        button.pack()

    @staticmethod
    def open_settings():
        settings = ctk.CTkToplevel()
        settings.title('Settings')
        settings.attributes('-topmost', True)
        settings.geometry('880x800+0+0')

        customization = ctk.CTkFrame(settings)
        customization.pack(padx=20, pady=20, side='top', fill='both', expand=True)

        scale_window_label = ctk.CTkLabel(customization, text='Set window scaling')
        scale_window_label.grid()

        scale_window_dropdown = ctk.CTkComboBox(customization,
                                                values=['75%', '100%', '150%', '200%', '250%', '300%'],
                                                command=lambda scale:
                                                ctk.set_window_scaling(float(scale_window_dropdown.get()[:-1]) / 100),
                                                font=('ubuntu' if platform.system() == 'Linux' else 'Arial', 20))

        scale_window_dropdown.set('100%')
        scale_window_dropdown.grid()

        scale_label = ctk.CTkLabel(customization, text='Set widget scaling')
        scale_label.grid()

        scale_dropdown = ctk.CTkComboBox(customization,
                                         values=['75%', '100%', '150%', '200%', '250%', '300%'],
                                         command=lambda scale:
                                         ctk.set_widget_scaling(float(scale_dropdown.get()[:-1]) / 100),
                                         font=('ubuntu' if platform.system() == 'Linux' else 'Arial', 20))

        scale_dropdown.set('100%')
        scale_dropdown.grid()

        amode_label = ctk.CTkLabel(customization, text='Set color')
        amode_label.grid()

        amode_dropdown = ctk.CTkComboBox(customization,
                                         values=['dark', 'white', 'system'],
                                         command=lambda mode:
                                         ctk.set_appearance_mode(mode),
                                         font=('ubuntu' if platform.system() == 'Linux' else 'Arial', 20))
        amode_dropdown.set('system')
        amode_dropdown.grid()

        hint = ctk.CTkLabel(customization, text='\n'.join(
            ['Hint: Use same window and widget scale for better experience.',
             '',
             'Notice: '
             'This options are experimental. Don`t use if you aren`t sure',
             ' what you do.',
             'It won`t be updated.'],
        ))
        hint.grid()

        close_button = ctk.CTkButton(settings, text='CLOSE', command=settings.destroy)
        close_button.pack(pady=30)

    @staticmethod
    def open_about():
        about = ctk.CTkToplevel()
        about.title('About')
        about.attributes('-topmost', True)
        about.geometry('880x800+0+0')

        about_frame = ctk.CTkFrame(about)
        about_frame.pack(padx=20, pady=20, side='top', fill='both', expand=True)

        about_label = ctk.CTkLabel(about_frame, text='Developer GitHub: r-liner')
        about_label.grid()

        close_button = ctk.CTkButton(about, text='CLOSE', command=about.destroy)
        close_button.pack(pady=30)


if __name__ == "__main__":
    app = App()
    app.mainloop()
