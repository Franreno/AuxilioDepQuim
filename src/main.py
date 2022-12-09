import tkinter
import customtkinter
from database_handler import DatabaseHandler
from psycopg2._psycopg import connection, cursor, OperationalError
from tabulate import tabulate
from utils import matchAndRun
import sys


class App(customtkinter.CTk):


    def __init__(self, dbHandler: DatabaseHandler) -> None:
        """Gerador inicial do GUI. Cria-se os botões a esquerda, titulos e espaço DisplayFrame, onde o usuario interage

        Args:
            dbHandler (DatabaseHandler): Handler criado para manipulação da database
        """
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
            self.sidebar_frame, text="Mostrar tabelas")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = customtkinter.CTkButton(
            self.sidebar_frame, text="Rodar/Debugar  SQL",  command = self.runSQL)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_3 = customtkinter.CTkButton(
            self.sidebar_frame, text="Rodar Consultas.sql", command=self.runConsultas)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.sidebar_button_Func = customtkinter.CTkButton(
            self.sidebar_frame, text="Cadastrar Novo Funcionario", command = self.insertFunc)
        self.sidebar_button_Func.grid(row=4, column=0, padx=20, pady=10)

        self.sidebar_button_Emp = customtkinter.CTkButton(
            self.sidebar_frame, text="Cadastrar Empresa", command = self.cadEmpresa)
        self.sidebar_button_Emp.grid(row=5, column=0, padx=20, pady=10)

        self.sidebar_button_Centro = customtkinter.CTkButton(
            self.sidebar_frame, text="Inserir Centro", command = self.cadCentro)
        self.sidebar_button_Centro.grid(row=6, column=0, padx=20, pady=10)

        self.sidebar_button_Centro = customtkinter.CTkButton(
            self.sidebar_frame, text="Mostrar Informacoes", command = self.showInfo)
        self.sidebar_button_Centro.grid(row=7, column=0, padx=20, pady=10)
        # Create output box
        

        self.DisplayFrame = customtkinter.CTkFrame(self, width = 600, height = 720)
        self.DisplayFrame.grid(row = 0, column = 1, rowspan = 7, columnspan = 5, sticky = 'nsew')

        self.textbox = customtkinter.CTkTextbox(self.DisplayFrame, height=300, width = 720)
        self.textbox.grid(row=1, column=1, rowspan = 4, columnspan = 4,padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.textbox.insert("0.0", "Sistema De consultas\n\n" + "Opções de manipulação e Análise no seu menu esquerdo!.\n\n")
        self.textbox.configure(state='disabled')


    def showInfo(self):
        """Função que procura todas as tabelas da database, retornando uma lista no dropdown onde o usuario poderá selecionar o atributo que deseja consultar
        """
        tableName = matchAndRun('tableNames')
        self.DisplayFrame.destroy()
        self.DisplayFrame = customtkinter.CTkFrame(self, width = 800, height = 1000)
        self.DisplayFrame.grid(row = 0, column = 1, sticky = 'nsew')

        self.textbox = customtkinter.CTkTextbox(self.DisplayFrame, height=300, width = 720)
        self.textbox.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.textbox.configure(state='disabled')

        
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.DisplayFrame, dynamic_resizing=False,
                                                        values= tableName, command=self.selectColumn)
        self.optionmenu_1.grid(row=1, column=1, padx=20, pady=(20, 10))
        pass
    
    def queryData(self, coluna: str):
        """Função que passa os atributos necessários para a query especifica, no caso, a coluna (recebida por parametro) e a tabela(passada como argumento na classe)

        Args:
            coluna (str): _description_
        """
        data = (self.tempDataSelect, coluna)
        output = matchAndRun('directQuery', data)
        self.textbox.configure(state='normal')
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", output)
        self.textbox.configure(state='disabled')
        pass

    def selectColumn(self, table: str):
        """Dada uma tabela, essa função itera através de todos os seus atributos gerando uma lista para o usuario selecionar o desejado

        Args:
            table (str): tabela a ser iterada
        """
        self.tempDataSelect = table
        columnName = matchAndRun('columnNames', table)
        columnName.insert(0, '*')
        self.optionmenu_2 = customtkinter.CTkOptionMenu(self.DisplayFrame, dynamic_resizing=False,
                                                        values= columnName, command = self.queryData)
        self.optionmenu_2.grid(row=2, column=1, padx=20, pady=(20, 10))
        pass


    def getEntryCentro(self):
        """Recebe as entradas dos inputs do GUI e repassa para o handler formular a consulta em SQL
        """
        nome = self.entryNome.get()
        cnpj = self.entryCnpj.get()
        caixa = self.entryCaixa.get()
        presidente = self.entryPresidente.get()
        local = self.entryLocal.get()
        data = (cnpj, caixa, nome, local, presidente)
        if matchAndRun('insertCentro', data) == -1:
            tkinter.messagebox.showinfo("ERRO", "Por favor, verificar a integridade das informações adicionadas")
        else:
            tkinter.messagebox.showinfo("Sucesso!", "Centro Inserido Com Sucesso")
        pass


    def cadCentro(self):
        """Cria o Display necessario para os inputs de informações relacionadas ao cadastro de centro e os vincula com a função disparada no botão
        """
        self.DisplayFrame.destroy()
        self.DisplayFrame = customtkinter.CTkFrame(self, width = 800, height = 1000)
        self.DisplayFrame.grid(row = 1, column = 1, sticky = 'nsew')

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
        """Recebe os inputs das entrys relacionadas ao cadastro da empresa
        """
        Nome = self.entryNome.get()
        Cnpj = self.entryCnpj.get()
        NumFunc = self.entryNumFunc.get()
        NumMax = self.entryNumFunc.get()
        data = (Nome, Cnpj, NumFunc, NumMax)
        if matchAndRun('insertEmp', data) == -1:
            tkinter.messagebox.showinfo("ERRO", "Por favor, verificar a integridade das informações adicionadas")
        else:
            tkinter.messagebox.showinfo("Sucesso!", "Empresa Parceira Inserida Com Sucesso!")
        pass


    def cadEmpresa(self):
        """Criação do display para coleta das entrys relacionadas ao cadastro de empresa
        """
        self.DisplayFrame.destroy()

        self.DisplayFrame = customtkinter.CTkFrame(self, width = 600, height = 720)
        self.DisplayFrame.grid(row = 1, column = 1, columnspan = 4, sticky = 'nsew')

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
        """Receber os inputs das entrys do Cadastro de funcionario e repassa-las como parametros para a geração de uma consulta SQL
        """
        nome = self.entryNome.get()
        CPF = self.entryCPF.get()
        Centro = self.entryCentro.get()
        data = [nome, CPF, Centro]
        if matchAndRun('insertFunc', data) == -1:
            tkinter.messagebox.showinfo("ERRO", "Por favor, verificar a integridade das informações adicionadas")
        else:
            tkinter.messagebox.showinfo("Sucesso!", "Funcionario Inserido Com Sucesso")
        return


    def insertFunc(self):   
        """Criação das entrys necessárias para a coleta de informações relacionadas a inserção de um funcionário
        """
        self.DisplayFrame.destroy()
        self.DisplayFrame = customtkinter.CTkFrame(self, width = 600, height = 720)
        self.DisplayFrame.grid(row = 1, column = 1, sticky = 'nsew')
        
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
        """Repassa pelo matchandrun a busca por 'consultas' onde será realizada as buscas explicitadas no arquivo consultas.sql
        """
        self.DisplayFrame.destroy()
        self.DisplayFrame = customtkinter.CTkFrame(self, width = 600, height = 720)
        self.DisplayFrame.grid(row = 1, column = 1, sticky = 'nsew')
        self.textbox = customtkinter.CTkTextbox(self.DisplayFrame, height=300, width = 720)
        self.textbox.grid(row=1, column=1, rowspan = 4, columnspan = 4,padx=(20, 20), pady=(20, 20), sticky="nsew")

        output = matchAndRun('consultas')
        self.textbox.configure(state='normal')
        self.textbox.delete("0.0", "end")
        unpackedString = '\n'.join(output)
        self.textbox.insert("0.0", unpackedString)
        self.textbox.configure(state='disabled')
        pass

    def getCommand(self):
        """Coleta do comando digitado em textbox pelo usuario e o repassa para a geração de uma consulta sql
        """
        inp = self.textbox1.get("1.0", "end-1c")
        output = matchAndRun('runSQL', inp)
        self.textbox.configure(state='normal')
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", output)
        self.textbox.configure(state='disabled')
        self.textbox1.delete("0.0", "end")
        pass



    def runSQL(self):
        """Criação do Display com entrys necessárias para a coleta da consulta SQL digitada pelo usuário
        """
        self.DisplayFrame.destroy()

        self.DisplayFrame = customtkinter.CTkFrame(self, width = 600, height = 720)
        self.DisplayFrame.grid(row = 1, column = 1, sticky = 'nsew')
        self.textbox = customtkinter.CTkTextbox(self.DisplayFrame, height=300, width = 720)
        self.textbox.grid(row=1, column=1, rowspan = 4, columnspan = 4,padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.textbox.configure(state='normal')
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Digite seu código em SQL abaixo\nObviamente esse tipo de opção não estaria disponível ao usuário por ser perigosa,\nmas é bom pra debugar e fazer teste :)")
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
