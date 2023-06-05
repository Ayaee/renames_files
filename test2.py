import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle


class MyTabView(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # create tabs
        self.tab1 = tk.Frame(self.notebook)
        self.tab2 = tk.Frame(self.notebook)

        self.notebook.add(self.tab1, text="Tab 1")
        self.notebook.add(self.tab2, text="Tab 2")

    def get_selected_tab(self):
        current_tab = self.notebook.select()
        tab_text = self.notebook.tab(current_tab, "text")
        return tab_text


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("My App")

        style = ThemedStyle(self)
        style.set_theme("black")

        self.tab_view = MyTabView(self)
        self.tab_view.pack(padx=20, pady=20)

        self.button = tk.Button(self, text="Get Selected Tab", command=self.button_callback)
        self.button.pack(padx=10, pady=10)

    def button_callback(self):
        selected_tab = self.tab_view.get_selected_tab()
        print("Selected tab:", selected_tab)
        return selected_tab

app = App()
app.mainloop()
