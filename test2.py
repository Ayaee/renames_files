import customtkinter as ctk


# Fenêtre
ctk.set_appearance_mode("dark")
tool_ui = ctk.CTk()
tool_ui.title("Tool de renommage de fichiers")
tool_ui.geometry("800x400")

# Frame
frame = ctk.CTkFrame(tool_ui)
frame.pack()

# Widgets
choice = ctk.CTkLabel(
    frame,
    text="Voulez vous directement 'rename' vos fichier dans le dossier existant ou alors les 'copy' dans un nouveau dossier pour les renommer ?\n"
         "Écrivez 'rename' ou 'copy' selon votre choix\n")
choice.pack(padx=10, pady=10,)

tool_ui.mainloop()