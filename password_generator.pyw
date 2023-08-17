import customtkinter as ctk
import string
import random


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Password Generator v0.1')
        self._set_appearance_mode('dark')
        ctk.set_default_color_theme('green')
        self.geometry('800x400')
        self.minsize(400, 280)
        self.maxsize(800, 400)
        self.wm_iconbitmap('icon.ico')

        self.check_boxes = ctk.CTkFrame(self,
                                        fg_color=('#ffffff', '#000000'), bg_color=('#ffffff', '#000000'))
        self.check_boxes.columnconfigure(all([0, 1]), minsize=40, weight=1)
        self.check_boxes.rowconfigure(all([i for i in range(8)]), minsize=20)
        self.check_boxes.pack(fill='both', side='top', expand=True)

        self.password = ctk.CTkEntry(self.check_boxes, width=600, font=('Arial', 24))
        self.password.grid(row=0, column=0, stick='we', pady=10, sticky='n')

        self.length = ctk.CTkEntry(self.check_boxes, 250, 30, placeholder_text="Enter password length",
                                   font=('Arial', 20))
        self.length.grid(row=1, column=0, columnspan=2, pady=10, sticky='s')

        self.error = ctk.CTkLabel(self, text='', font=('Arial', 30), text_color='red')
        self.error.pack(side='top', fill='both')

        self.switches = ctk.CTkFrame(self)
        self.switches.pack(side='right', anchor='e')
        self.switches.pack(fill='both', side='right', expand=True)

        self.digits = ctk.CTkSwitch(self.switches, width=50, height=20, switch_width=40, switch_height=20,
                                    text="Digits")
        self.digits.grid(row=0, column=0, pady=5, sticky='e')

        self.lowers = ctk.CTkSwitch(self.switches, width=50, height=20, switch_width=40, switch_height=20,
                                    text="Lowers")
        self.lowers.grid(row=1, column=0, pady=5)

        self.uppers = ctk.CTkSwitch(self.switches, width=50, height=20, switch_width=40, switch_height=20,
                                    text="Uppers")
        self.uppers.grid(row=2, column=0, pady=5)

        self.punctuation = ctk.CTkSwitch(self.switches, width=50, height=20, switch_width=40, switch_height=20,
                                         text="Punct")
        self.punctuation.grid(row=3, column=0, pady=5)

        self.buttons = ctk.CTkFrame(self)
        self.buttons.pack(fill='both', side='left', expand=True)

        self.generate = ctk.CTkButton(self.buttons, text="GENERATE", command=self.generate_password)
        self.generate.grid(row=0, column=0, pady=10)

        self.generate = ctk.CTkButton(self.buttons, text="CLEAR", command=self.clear)
        self.generate.grid(row=1, column=0, pady=10)

        self.copy = ctk.CTkButton(self.buttons, text="COPY", command=self.copy_to_clipboard)
        self.copy.grid(row=2, column=0, pady=10)

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
            self.password.insert(index=0, string=''.join(random.sample(symbols, int(self.length.get()))))
            self.error.configure(text='')
        except ValueError:
            print(self.error.winfo_screen())
            self.error.configure(text='ERROR')
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
