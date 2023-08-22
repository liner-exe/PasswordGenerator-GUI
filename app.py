import customtkinter as ctk
import string
import random
import platform


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        platform_name = platform.system()
	
        self.title(f'Password Generator v0.0.2 | for {platform_name}')
        self._set_appearance_mode('dark')
        ctk.set_default_color_theme('green')
        self.geometry('800x400')
        self.minsize(400, 280)
        self.maxsize(800, 400)
        
        fontname = 'Arial'
        if platform.system() == 'Linux':
            self.resizable(False, False)
            fontname = 'ubuntu'
            
        elif platform.system() == 'Windows':
            self.wm_iconbitmap('icon.ico')
        
        
        self.check_boxes = ctk.CTkFrame(self,
                                        fg_color=('#ffffff', '#323332'), bg_color=('#ffffff', '#323332'))
        self.check_boxes.pack(fill='both', side='top', expand=True)

        self.password = ctk.CTkEntry(self.check_boxes, width=600, font=(fontname, 24))
        self.password.grid(row=0, column=0, stick='we', pady=10, sticky='n')

        self.length = ctk.CTkEntry(self.check_boxes, 250, 30, placeholder_text="Enter password length",
                                   font=(fontname, 20))
        self.length.grid(row=1, column=0, columnspan=2, pady=10, sticky='s')

        self.error = ctk.CTkLabel(self, text='', fg_color=('#EBEBEB', '#2b2b2b'), font=(fontname, 30), text_color='red')
        self.error.pack(side='top', fill='both')

        self.switches = ctk.CTkFrame(self, border_width=0)
        self.switches.pack(side='right', anchor='e')
        self.switches.pack(fill='both', side='right', expand=True)

        self.digits = ctk.CTkSwitch(self.switches, width=50, height=20, switch_width=40, switch_height=20,
                                    text="Digits", font=(fontname, 20))
        self.digits.grid(row=0, column=0, pady=5, sticky='e')

        self.lowers = ctk.CTkSwitch(self.switches, width=50, height=20, switch_width=40, switch_height=20,
                                    text="Lowers", font=(fontname, 20))
        self.lowers.grid(row=1, column=0, pady=5)

        self.uppers = ctk.CTkSwitch(self.switches, width=50, height=20, switch_width=40, switch_height=20,
                                    text="Uppers", font=(fontname, 20))
        self.uppers.grid(row=2, column=0, pady=5)

        self.punctuation = ctk.CTkSwitch(self.switches, width=50, height=20, switch_width=40, switch_height=20,
                                         text="Punct", font=(fontname, 20))
        self.punctuation.grid(row=3, column=0, pady=5)

        self.buttons = ctk.CTkFrame(self, border_width=0)
        self.buttons.pack(fill='both', side='left', expand=True)

        self.generate = ctk.CTkButton(self.buttons, text="GENERATE", font=(fontname, 15), command=self.generate_password)
        self.generate.grid(row=0, column=0, pady=10)

        self.generate = ctk.CTkButton(self.buttons, text="CLEAR", font=(fontname, 15), command=self.clear)
        self.generate.grid(row=1, column=0, pady=10)

        self.copy = ctk.CTkButton(self.buttons, text="COPY", font=(fontname, 15), command=self.copy_to_clipboard)
        self.copy.grid(row=2, column=0, pady=10, padx=10)

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
            self.error.configure(text='')
        except ValueError:
            self.error.configure(text='ERROR. Empty password length.')
        except IndexError:
            self.error.configure(text='ERROR. Character switches are not used.')
        except Exception as err:
            print(err)

    def clear(self):
        self.password.delete(0, ctk.END)

    def copy_to_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.password.get())


if __name__ == "__main__":
    app = App()
    app.mainloop()
