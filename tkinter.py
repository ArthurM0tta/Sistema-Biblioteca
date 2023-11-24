import sqlite3
from datetime import datetime, timedelta
from prettytable import PrettyTable
import tkinter as tk
from tkinter import messagebox


# Funções

def obter_texto():
    texto_inserido = entry.get()
    print("Texto inserido:", texto_inserido)

# Função para calcular a diferença de dias entre duas datas
def calcular_atraso(fecha_actual, fecha_limite):
    fecha_limite = datetime.strptime(fecha_limite, '%Y-%m-%d').date()
    return (fecha_actual - fecha_limite).days if fecha_actual > fecha_limite else 0

# Função para verificar se está dentro do prazo ou em atraso
def verificar_atraso(atraso):
    if atraso <= 0:
        return "Estás dentro do prazo. Pode entregar o produto sem problemas."
    else:
        return "Está fora do prazo. Deve entregar produtos em 5 dias."






#-------------------------------------------------------------------------------------------------------

class BibliotecaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Biblioteca")

        # Conectar ao banco de dados (se não existir, será criado)
        self.conn = sqlite3.connect('Biblioteca.db')
        self.cursor = self.conn.cursor()

        self.menu_label = tk.Label(root, text="Escolha uma opção:")
        self.menu_label.pack()

        self.criar_button = tk.Button(root, text="Criar Cadastro", command=self.criar_cadastro)
        self.criar_button.pack()

        self.alterar_button = tk.Button(root, text="Alterar Cadastro", command=self.alterar_cadastro)
        self.alterar_button.pack()

        self.pesquisar_button = tk.Button(root, text="Pesquisar Cadastro", command=self.pesquisar_cadastro)
        self.pesquisar_button.pack()

        self.exibir_button = tk.Button(root, text="Exibir Livros", command=self.exibir_livros)
        self.exibir_button.pack()

        self.alugar_button = tk.Button(root, text="Alugar Livro", command=self.alugar_livro)
        self.alugar_button.pack()

        self.devolver_button = tk.Button(root, text="Devolver Livro", command=self.devolver_livro)
        self.devolver_button.pack()

        self.remover_button = tk.Button(root, text="Remover Cadastro", command=self.remover_cadastro)
        self.remover_button.pack()

        self.sair_button = tk.Button(root, text="Sair", command=root.destroy)
        self.sair_button.pack()

    def fechar_conexao(self):
        # Fechar a conexão com o banco de dados
        self.conn.close()
        self.root.destroy()

    # Adicione as demais funções de acordo com suas necessidades

    def criar_cadastro(self):
        cadastro = tk.Tk()
        self.cadastro = cadastro
        self.cadastro.title("Criação de cadastro")

        self.cpf_label = tk.Label(cadastro, text="Insira o CPF (no formato xxx.xxx.xxx-xx)")
        self.cpf_label.pack()

        self.cpf_var = tk.StringVar()
        cpf_entry = self.cpf_entry = tk.Entry(cadastro, textvariable=self.cpf_var)
        self.cpf_entry.pack()

        self.nome_label = tk.Label(cadastro, text="Nome:")
        self.nome_label.pack()

        self.nome_var = tk.StringVar()
        nome_entry = self.nome_entry = tk.Entry(cadastro, textvariable=self.nome_var)
        self.nome_entry.pack()

        self.nascimento_label = tk.Label(cadastro, text="Data de Nascimento (DD-MM-YYYY):")
        self.nascimento_label.pack()

        self.nascimento_var = tk.StringVar()
        nascimento_entry = self.nascimento_entry = tk.Entry(cadastro, textvariable=self.nascimento_var)
        self.nascimento_entry.pack()

        self.telefone_label = tk.Label(cadastro, text="Telefone (XX)XXXXX-XXXX:")
        self.telefone_label.pack()

        self.telefone_var = tk.StringVar()
        telefone_entry = self.telefone_entry = tk.Entry(cadastro, textvariable=self.telefone_var)
        self.telefone_entry.pack()

        self.email_label = tk.Label(cadastro, text="Email:")
        self.email_label.pack()

        self.email_var = tk.StringVar()
        email_entry = self.email_entry = tk.Entry(cadastro, textvariable=self.email_var)
        self.email_entry.pack()

        def validar_cpf(cpf):
            return len(cpf) == 14 and cpf[3] == '.' and cpf[7] == '.' and cpf[11] == '-'

        def validar_data(nascimento):
            try:
                datetime.strptime(nascimento, '%d-%m-%Y')
                return True
            except ValueError:
                return False

        def validar_telefone(telefone):
            return len(telefone) == 14 and telefone[0] == '(' and telefone[3] == ')' and telefone[9] == '-'


        def confirmar_envio():
            cpf = self.cpf_var.get()
            nome = self.nome_var.get()
            nascimento = self.nascimento_var.get()
            telefone = self.telefone_var.get()
            email = self.email_var.get()
            try:
                if validar_cpf(cpf) and validar_data(nascimento) and validar_telefone(telefone):
                    messagebox.showinfo('Cadastro criado!')
                    # Converter a data para o formato 'yyyy-mm-dd' para o SQLite
                    data_formatada = datetime.strptime(nascimento, '%d-%m-%Y').strftime('%Y-%m-%d')
                    # Executar uma consulta SQL para inserir uma variável no banco de dados
                    consulta_insercao = "INSERT INTO cadastro (cpf, nome, nascimento, telefone, email) VALUES (?, ?, ?, ?, ?)"
                    dados_para_inserir = (cpf, nome, data_formatada, telefone, email)
                    # Executar a consulta
                    self.cursor.execute(consulta_insercao, dados_para_inserir)
                    # Confirmar a transação
                    self.conn.commit()   
                    # Fechar a conexão após a inserção
                    self.fechar_conexao()        
                else:
                    messagebox.showinfo('Mensagem de Erro', 'Dados inválidos. Por favor, insira o CPF no formato xxx.xxx.xxx-xx, a data no formato correto (Dia-Mês-Ano) e o telefone no formato (xx) xxxxx-xxxx.')
            except ValueError as e:
                messagebox.showerror('Erro', str(e))


        # Botão de confirmação
        self.confirmar_button = tk.Button(cadastro, text="Confirmar", command=confirmar_envio)
        self.confirmar_button.pack()

    def alterar_cadastro(self):
        messagebox.showinfo("Alteração", "Coloque a alteração de cadastro aqui.")

    def pesquisar_cadastro(self):
        messagebox.showinfo("Pesquisa", "Coloque a pesquisa de cadastro aqui.")

    def exibir_livros(self):
        messagebox.showinfo("Exibição de Livros", "Coloque a exibição de livros aqui.")

    def alugar_livro(self):
        messagebox.showinfo("Aluguel de Livro", "Coloque a funcionalidade de aluguel de livro aqui.")

    def devolver_livro(self):
        messagebox.showinfo("Devolução de Livro", "Coloque a funcionalidade de devolução de livro aqui.")

    def remover_cadastro(self):
        messagebox.showinfo("Remoção de Cadastro", "Coloque a remoção de cadastro aqui.")




# Crie a instância da interface gráfica
root = tk.Tk()
app = BibliotecaGUI(root)

# Execute o loop principal da interface gráfica
root.mainloop()
