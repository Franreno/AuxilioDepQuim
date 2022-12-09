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
        self.geometry(f"{1200}x{720}")

        # Configure grid Layout
        self.grid_columnconfigure(1, weight=1)
        
        self.grid_rowconfigure((0, 1, 2,3), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=7, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Interface Auxilios", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame, text="Mostrar tabelas")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = customtkinter.CTkButton(
            self.sidebar_frame, text="Rodar SQL",  command = self.runSQL)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_3 = customtkinter.CTkButton(
            self.sidebar_frame, text="Rodar Consultas.sql", command=self.runConsultas)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.sidebar_button_Func = customtkinter.CTkButton(
            self.sidebar_frame, text="Inserir Funcionario", command = self.insertFunc)
        self.sidebar_button_Func.grid(row=4, column=0, padx=20, pady=10)

        self.sidebar_button_Emp = customtkinter.CTkButton(
            self.sidebar_frame, text="Inserir Empresa")
        self.sidebar_button_Emp.grid(row=5, column=0, padx=20, pady=10)

        self.sidebar_button_Centro = customtkinter.CTkButton(
            self.sidebar_frame, text="Inserir Centro")
        self.sidebar_button_Centro.grid(row=6, column=0, padx=20, pady=10)
        # Create output box
        self.DisplayFrame = customtkinter.CTkFrame(self, width = 600, corner_radius = 0)
        self.DisplayFrame.grid_rowconfigure((0,1,2), weight=1)
        self.DisplayFrame.grid(row = 0, column = 1, rowspan = 7, sticky = "nsew")

        self.textbox = customtkinter.CTkTextbox(self, height=400)
        self.textbox.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
        self.textbox.configure(state='disabled')

    def insertFunc(self):

        
        self.textbox.destroy()
        self.grid_columnconfigure((1,2,3), weight = 1)
        self.grid_rowconfigure((0,1,2,3), weight = 1)
        self.entryNome= customtkinter.CTkEntry(self, placeholder_text = "Nome")
        self.entryNome.grid(row=0, column = 1, columnspan = 2, padx=(10, 10), pady=(20,10), sticky="nsew")

        self.entryCPF= customtkinter.CTkEntry(self, placeholder_text = "CPF")
        self.entryCPF.grid(row=0, column= 3, columnspan = 1, padx=(10, 10), pady=(20,10), sticky="nsew") 
        return

    def runConsultas(self):
        output = matchAndRun('consultas')
        self.textbox.configure(state='normal')
        self.textbox.delete("0.0", "end")
        unpackedString = '\n'.join(output)
        self.textbox.insert("0.0", unpackedString)
        self.textbox.configure(state='disabled')
        pass

    def getCommand(self):
        inp = self.textbox1.get("1.0", "end-1c")
        output = matchAndRun('runSQL', inp)
        self.textbox.configure(state='normal')
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", output)
        self.textbox.configure(state='disabled')
        self.textbox1.delete("0.0", "end")
        return inp 



    def runSQL(self):
        self.textbox.configure(state='normal')
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Digite seu código em SQL abaixo")
        self.textbox.configure(state='disabled')
        
        self.textbox1 = customtkinter.CTkTextbox(self, height=100)
        self.textbox1.grid(row=2, column=1, padx=(20, 20), pady=(20, 10), sticky="nsew")
        self.main_button_run = customtkinter.CTkButton(self, command = self.getCommand, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_run.grid(row=3, column=1, padx=(20, 20), pady=(0, 0), sticky="nsew")
        self.main_button_run.configure(text="Rodar")
        pass



        


if __name__ == '__main__':

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")

    app = App(DatabaseHandler())

    app.mainloop()
