import customtkinter as ctk

ctk.set_appearance_mode("dark")


class Choices(ctk.CTkFrame):
    def __init__(self, master, values):
        super().__init__(master)

        self.choice = ctk.CTkLabel(self,
                                   text="Voulez vous directement 'rename' vos fichier dans le dossier existant ou alors les 'copy' dans un nouveau dossier pour les renommer ?\n"
                                        "Écrivez 'rename' ou 'copy' selon votre choix\n",
                                   padx=10,
                                   pady=10)
        self.choice.grid(row=0, column=0, columnspan=len(values) + 1, padx=20)

        self.choice = ctk.CTkLabel(self,
                                   text="Voulez vous directement 'rename' vos fichier dans le dossier existant ou alors les 'copy' dans un nouveau dossier pour les renommer ?\n"
                                        "Écrivez 'rename' ou 'copy' selon votre choix\n",
                                   padx=10,
                                   pady=10)
        self.choice.grid(row=0, column=0, columnspan=len(values) + 1, padx=20)

        self.values = values
        self.checkboxes = []

        for i, value in enumerate(self.values):
            checkbox = ctk.CTkCheckBox(self, text=value)
            checkbox.grid(row=1, column=i, padx=(150, 150), pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

        self.grid_columnconfigure(0, weight=1)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes


class ToolUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("900x400")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.title("Tool de renommage de fichiers")

        self.label_test = Choices(master=self, values=["rename", "copy"])
        self.label_test.grid(row=0, column=0, padx=20, pady=20, sticky="nsw")

        self.button = ctk.CTkButton(self, text="my button", command=self.button_callback)
        self.button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

    def button_callback(self):
        print("checked checkboxes:", self.label_test.get())


tool_ui = ToolUI()
tool_ui.mainloop()
