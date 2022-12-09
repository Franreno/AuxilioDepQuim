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
        self.sidebar_frame.grid(row=0, column=0, rowspan=8, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Interface Auxilios", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame, text="Mostrar tabelas", command= self.showTables, width=250)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = customtkinter.CTkButton(
            self.sidebar_frame, text="Rodar SQL",  command = self.runSQL, width=250)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_3 = customtkinter.CTkButton(
            self.sidebar_frame, text="Rodar Consultas.sql", command=self.runConsultas, width=250)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.sidebar_button_Func = customtkinter.CTkButton(
            self.sidebar_frame, text="Cadastrar Novo Funcionario", command = self.insertFunc, width=250)
        self.sidebar_button_Func.grid(row=4, column=0, padx=20, pady=10)

        self.sidebar_button_Emp = customtkinter.CTkButton(
            self.sidebar_frame, text="Cadastrar Empresa", command = self.cadEmpresa, width=250)
        self.sidebar_button_Emp.grid(row=5, column=0, padx=20, pady=10)

        self.sidebar_button_Centro = customtkinter.CTkButton(
            self.sidebar_frame, text="Inserir Centro", command = self.cadCentro, width=250)
        self.sidebar_button_Centro.grid(row=6, column=0, padx=20, pady=10)

        self.sidebar_button_Centro = customtkinter.CTkButton(
            self.sidebar_frame, text="Mostrar Informacoes", command = self.showInfo, width=250)
        self.sidebar_button_Centro.grid(row=7, column=0, padx=20, pady=10)
        # Create output box
        

        self.DisplayFrame = customtkinter.CTkFrame(self, width = 600, height = 720)
        self.DisplayFrame.grid(row = 0, column = 1, rowspan = 7, columnspan = 5, sticky = 'nsew')

        self.textbox = customtkinter.CTkTextbox(self.DisplayFrame, height=300, width = 720)
        self.textbox.grid(row=1, column=1, rowspan = 4, columnspan = 4,padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.textbox.insert("0.0", "Sistema De consultas\n\n" + "Opções de manipulação e Análise no seu menu esquerdo!.\n\n")
        self.textbox.configure(state='disabled')


    def showInfo(self):
        tableName = matchAndRun('tableNames')
        self.DisplayFrame.destroy()
        self.DisplayFrame = customtkinter.CTkFrame(self, width = 800, height = 1000)
        self.DisplayFrame.grid(row = 0, column = 1, rowspan = 7, columnspan = 3, sticky = 'nsew')

        self.textbox = customtkinter.CTkTextbox(self.DisplayFrame, height=300, width = 720)
        self.textbox.grid(row=2, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.textbox.configure(state='disabled')

        
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.DisplayFrame, dynamic_resizing=False,
                                                        values= tableName, command=self.selectColumn, width=250)
        self.optionmenu_1.grid(row=0, column=1, padx=20, pady=(20, 10))
    
    def queryData(self, coluna: str):
        data = (self.tempDataSelect, coluna)
        output = matchAndRun('directQuery', data)
        self.textbox.configure(state='normal')
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", output)
        self.textbox.configure(state='disabled')
        pass

    def selectColumn(self, table: str):
        self.tempDataSelect = table
        columnName = matchAndRun('columnNames', table)
        columnName.insert(0, '*')
        self.optionmenu_2 = customtkinter.CTkOptionMenu(self.DisplayFrame, dynamic_resizing=False,
                                                        values= columnName, command = self.queryData, width=250)
        self.optionmenu_2.grid(row=1, column=1, padx=5, pady=(20, 10))
        pass


    def getEntryCentro(self):
        nome = self.entryNome.get()
        cnpj = self.entryCnpj.get()
        caixa = self.entryCaixa.get()
        presidente = self.entryPresidente.get()
        local = self.entryLocal.get()
        data = (cnpj, caixa, nome, local, presidente)
        if matchAndRun('insertCentro', data) == -1:
            tkinter.messagebox.showinfo("ERRO", "Por favor, verificar a integridade das informações adicionadas")
        pass

    def showTables(self):
        self.DisplayFrame.destroy()
        self.DisplayFrame = customtkinter.CTkFrame(self, width = 800, height = 1200)
        self.DisplayFrame.grid(row = 0, column = 1, rowspan = 7, columnspan = 3, sticky = 'nsew')

        allTables = matchAndRun('listTables')
        
        self.showTablesLabel = customtkinter.CTkLabel(
            self.DisplayFrame, 
            text="Escolha a tabela",
            font=customtkinter.CTkFont(size=18)
        )
        self.showTablesLabel.grid(row=0, column=0, padx=(0,10), pady=(20,10))


        self.tableTextBox = customtkinter.CTkTextbox(self.DisplayFrame, width=800)
        self.tableTextBox.grid(row=3,column=0, padx=(0,10), pady=(20,10))

        self.updatedValues(allTables[0])

        self.optionMenu = customtkinter.CTkOptionMenu(
            self.DisplayFrame, 
            width=300, 
            values=allTables,
            command=self.updatedValues
        )
        self.optionMenu.grid(row=2, column=0, padx=(10,10), pady=(20,10))


    def updatedValues(self, table: str):
        tableSchema = matchAndRun('getTableSchema', table)
        self.updateValueOnShowTables(tableSchema)


    def updateValueOnShowTables(self, values):
        self.tableTextBox.configure(state='normal')
        self.tableTextBox.delete("0.0", "end")
        self.tableTextBox.insert("0.0", values)
        self.tableTextBox.configure(state='disabled')

    def cadCentro(self):
        self.DisplayFrame.destroy()
        self.DisplayFrame = customtkinter.CTkFrame(self, width = 800, height = 1000)
        #self.DisplayFrame.grid(row = 1, column = 1, sticky = 'nsew')
        self.DisplayFrame.grid(row = 0, column = 1, rowspan = 7, columnspan = 3, sticky = 'nsew')

        self.entryCnpj= customtkinter.CTkEntry(self.DisplayFrame, placeholder_text = "CNPJ")
        self.entryCnpj.grid(row=0, column= 3, columnspan = 1, padx=(10, 10), pady=(20,10), sticky="ew")

        self.entryNome= customtkinter.CTkEntry(self.DisplayFrame, placeholder_text = "Nome")
        self.entryNome.grid(row=0, column= 2, columnspan = 1, padx=(10, 10), pady=(20,10), sticky="ew")

        self.entryCaixa= customtkinter.CTkEntry(self.DisplayFrame, placeholder_text = "Caixa")
        self.entryCaixa.grid(row=2, column= 2, columnspan = 1, padx=(10, 10), pady=(20,10), sticky="ew")

        self.entryPresidente= customtkinter.CTkEntry(self.DisplayFrame, placeholder_text = "Presidente")
        self.entryPresidente.grid(row=3, column= 2, columnspan = 1, padx=(10, 10), pady=(20,10), sticky="ew")

        self.entryLocal= customtkinter.CTkEntry(self.DisplayFrame, placeholder_text = "Local")
        self.entryLocal.grid(row=2, column= 3, padx=(10, 10), pady=(20,10), sticky="ew")

        self.getInputButton = customtkinter.CTkButton(self.DisplayFrame,text = "Inserir", command = self.getEntryCentro)
        self.getInputButton.grid(row =3, column = 3, padx = 20, pady = 20)


    def getInputEmp(self):
        Nome = self.entryNome.get()
        Cnpj = self.entryCnpj.get()
        NumFunc = self.entryNumFunc.get()
        NumMax = self.entryNumFunc.get()
        data = (Nome, Cnpj, NumFunc, NumMax)
        if matchAndRun('insertEmp', data) == -1:
            tkinter.messagebox.showinfo("ERRO", "Por favor, verificar a integridade das informações adicionadas")
        pass


    def cadEmpresa(self):
        self.DisplayFrame.destroy()
        self.DisplayFrame = customtkinter.CTkFrame(self, width = 600, height = 720)
        self.DisplayFrame.grid(row = 0, column = 1, rowspan = 7, columnspan = 3, sticky = 'nsew')

        self.entryCnpj= customtkinter.CTkEntry(self.DisplayFrame, placeholder_text = "CNPJ")
        self.entryCnpj.grid(row=2, column= 3, columnspan = 1, padx=(10, 10), pady=(20,10), sticky="ew")

        self.entryNome= customtkinter.CTkEntry(self.DisplayFrame, placeholder_text = "Nome")
        self.entryNome.grid(row=2, column= 2, columnspan = 1, padx=(10, 10), pady=(20,10), sticky="ew")

        self.entryNumFunc= customtkinter.CTkEntry(self.DisplayFrame, placeholder_text = "Numero de Funcionarios")
        self.entryNumFunc.grid(row=3, column= 2, columnspan = 1, padx=(10, 10), pady=(20,10), sticky="ew")

        self.entryNumMax= customtkinter.CTkEntry(self.DisplayFrame, placeholder_text = "Numero Maximo de Funcionarios")
        self.entryNumMax.grid(row=4, column= 2, columnspan = 1, padx=(10, 10), pady=(20,10), sticky="ew")
        
        self.getInputButton = customtkinter.CTkButton(self.DisplayFrame,text = "Inserir", command = self.getInputEmp)
        self.getInputButton.grid(row =3, column = 3, padx = 20, pady = 20)


        pass

    


    def getInputFunc(self):
        nome = self.entryNome.get()
        CPF = self.entryCPF.get()
        Centro = self.entryCentro.get()
        data = [nome, CPF, Centro]
        if matchAndRun('insertFunc', data) == -1:
            tkinter.messagebox.showinfo("ERRO", "Por favor, verificar a integridade das informações adicionadas")
        return


    def insertFunc(self):   
        self.DisplayFrame.destroy()
        self.DisplayFrame = customtkinter.CTkFrame(self, width = 600, height = 720)
        #self.DisplayFrame.grid(row = 1, column = 1, sticky = 'nsew')
        self.DisplayFrame.grid(row = 0, column = 1, rowspan = 7, columnspan = 3, sticky = 'nsew')
        
        self.entryNome= customtkinter.CTkEntry(self.DisplayFrame, placeholder_text = "Nome")
        self.entryNome.grid(row=0, column = 1, columnspan = 2, padx=(10, 10), pady=(20,10), sticky="ew")

        self.entryCPF= customtkinter.CTkEntry(self.DisplayFrame, placeholder_text = "CPF")
        self.entryCPF.grid(row=0, column= 3, columnspan = 2, padx=(10, 10), pady=(20,10), sticky="ew")
        

        self.entryCentro = customtkinter.CTkEntry(self.DisplayFrame, placeholder_text = "Centro")
        self.entryCentro.grid(row = 1, column = 1, sticky = "ew", padx=(10, 10), pady=(20,10))
        
        
        self.getInputButton = customtkinter.CTkButton(self.DisplayFrame,text = "Inserir", command = self.getInputFunc)
        self.getInputButton.grid(row = 1, column = 2, padx = 20, pady = 20)
        pass

    def runConsultas(self):
        self.DisplayFrame.destroy()
        self.DisplayFrame = customtkinter.CTkFrame(self, width = 600, height = 720)
        self.DisplayFrame.grid(row = 0, column = 1, rowspan = 7, columnspan = 3, sticky = 'nsew')
        #self.DisplayFrame.grid(row = 1, column = 1, sticky = 'nsew')
        self.textbox = customtkinter.CTkTextbox(self.DisplayFrame, height=600, width = 720)
        self.textbox.grid(row=1, column=1, rowspan = 4, columnspan = 5,padx=(20, 20), pady=(20, 20), sticky="nsew")

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
        self.DisplayFrame.destroy()

        self.DisplayFrame = customtkinter.CTkFrame(self, width = 600, height = 720)
        self.DisplayFrame.grid(row = 0, column = 1, rowspan = 7, columnspan = 3, sticky = 'nsew')
        #self.DisplayFrame.grid(row = 1, column = 1, sticky = 'nsew')
        self.textbox = customtkinter.CTkTextbox(self.DisplayFrame, height=300, width = 720)
        self.textbox.grid(row=1, column=1, rowspan = 4, columnspan = 4,padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.textbox.configure(state='normal')
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Digite seu código em SQL abaixo")
        self.textbox.configure(state='disabled')
        
        self.textbox1 = customtkinter.CTkTextbox(self.DisplayFrame, height=100)
        self.textbox1.grid(row=5, column=1, columnspan = 4, padx=(20, 20), pady=(20, 10), sticky="ew")
        self.main_button_run = customtkinter.CTkButton(self.DisplayFrame, command = self.getCommand, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_run.grid(row=6, column=1, columnspan = 4, padx=(20, 20), pady=(0, 0), sticky="ew")
        self.main_button_run.configure(text="Rodar")
        pass



        


if __name__ == '__main__':

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")

    app = App(DatabaseHandler())

    app.mainloop()
