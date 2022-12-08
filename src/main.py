import tkinter
import customtkinter
from database_handler import DatabaseHandler
from psycopg2._psycopg import connection, cursor, OperationalError
from tabulate import tabulate
from utils import matchAndRun
import sys


class App(customtkinter.CTk):


    def __init__(self, dbHandler: DatabaseHandler) -> None:
        super().__init__()

        self.dbHandler = dbHandler

        # Configure Window
        self.title("Interface Auxilios")
        self.geometry(f"{1100}x{580}")

        # Configure grid Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2,3), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Interface Auxilios", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame, text="Mostrar tabelas")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = customtkinter.CTkButton(
            self.sidebar_frame, text="Rodar SQL")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_3 = customtkinter.CTkButton(
            self.sidebar_frame, text="Rodar Consultas.sql", command=self.runConsultas)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        # Create output box
        self.textbox = customtkinter.CTkTextbox(self, height=200)
        self.textbox.grid(row=4, column=1, padx=(
            20, 20), pady=(20, 20), sticky="nsew")
        self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
        self.textbox.configure(state='disabled')

    def runConsultas(self):
        output = matchAndRun('consultas')
        
        self.textbox.configure(state='normal')
        self.textbox.delete("0.0", "end")
        unpackedString = '\n'.join(output)
        self.textbox.insert("0.0", unpackedString)
        self.textbox.configure(state='disabled')

        pass




if __name__ == '__main__':

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")

    app = App(DatabaseHandler())

    app.mainloop()
