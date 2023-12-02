

import sqlite3
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox


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

#--------------------------------------------------------------------------------------------------------

    def criar_cadastro(self):
        cadastro = tk.Tk()
        self.cadastro = cadastro
        self.cadastro.title("Criação de cadastro")

        self.cpf_label = tk.Label(cadastro, text="Insira o CPF (no formato xxx.xxx.xxx-xx)")
        self.cpf_label.pack()

        self.cpf_var = tk.StringVar()
        self.cpf_entry = tk.Entry(cadastro, textvariable=self.cpf_var)
        self.cpf_entry.pack()

        self.nome_label = tk.Label(cadastro, text="Nome:")
        self.nome_label.pack()

        self.nome_var = tk.StringVar()
        self.nome_entry = tk.Entry(cadastro, textvariable=self.nome_var)
        self.nome_entry.pack()

        self.nascimento_label = tk.Label(cadastro, text="Data de Nascimento (DD-MM-YYYY):")
        self.nascimento_label.pack()

        self.nascimento_var = tk.StringVar()
        self.nascimento_entry = tk.Entry(cadastro, textvariable=self.nascimento_var)
        self.nascimento_entry.pack()

        self.telefone_label = tk.Label(cadastro, text="Telefone (XX)XXXXX-XXXX:")
        self.telefone_label.pack()

        self.telefone_var = tk.StringVar()
        self.telefone_entry = tk.Entry(cadastro, textvariable=self.telefone_var)
        self.telefone_entry.pack()

        self.email_label = tk.Label(cadastro, text="Email:")
        self.email_label.pack()

        self.email_var = tk.StringVar()
        self.email_entry = tk.Entry(cadastro, textvariable=self.email_var)
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
            cpf = self.cpf_entry.get()
            nome = self.nome_entry.get()
            nascimento = self.nascimento_entry.get()
            telefone = self.telefone_entry.get()
            email = self.email_entry.get()

            try:
                if validar_cpf(cpf) and validar_data(nascimento) and validar_telefone(telefone):

                    # Verificar se o CPF já está cadastrado
                    consulta_verificacao = "SELECT * FROM cadastro WHERE cpf = ?"
                    self.cursor.execute(consulta_verificacao, (cpf,))
                    resultado = self.cursor.fetchone()

                    if resultado:
                        messagebox.showinfo('Mensagem de Aviso', 'CPF já cadastrado. Por favor, insira um CPF diferente.')
                    else:
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

                        # Fechar a janela de criação após a inserção
                        self.cadastro.destroy()
                        messagebox.showinfo('Cadastro finalizado', 'Cadastro criado com sucesso!')      
                else:
                        messagebox.showinfo('Mensagem de Erro', 'Dados inválidos. Por favor, insira o CPF no formato xxx.xxx.xxx-xx, a data no formato correto (Dia-Mês-Ano) e o telefone no formato (xx) xxxxx-xxxx.')
            except ValueError as e:
                messagebox.showerror('Erro', str(e))
            except Exception as ex:
                messagebox.showerror('Erro', f'Erro inesperado: {str(ex)}')


        # Botão de confirmação
        self.confirmar_button = tk.Button(cadastro, text="Confirmar", command=confirmar_envio)
        self.confirmar_button.pack()

#--------------------------------------------------------------------------------------------------------

    def alterar_cadastro(self):
        cadastro = tk.Tk()
        self.cadastro = cadastro
        self.cadastro.title("Alteração de cadastro")

        self.nome_var = tk.StringVar()
        self.nascimento_var = tk.StringVar()
        self.telefone_var = tk.StringVar()
        self.email_var = tk.StringVar()

        self.nome_entry = tk.Entry(self.cadastro, textvariable=self.nome_var, state=tk.DISABLED)
        self.nascimento_entry = tk.Entry(self.cadastro, textvariable=self.nascimento_var, state=tk.DISABLED)
        self.telefone_entry = tk.Entry(self.cadastro, textvariable=self.telefone_var, state=tk.DISABLED)
        self.email_entry = tk.Entry(self.cadastro, textvariable=self.email_var, state=tk.DISABLED)

        self.cpf_label = tk.Label(cadastro, text="Insira o CPF (no formato xxx.xxx.xxx-xx)")
        self.cpf_label.pack()

        self.cpf_var = tk.StringVar()
        self.cpf_entry = tk.Entry(cadastro, textvariable=self.cpf_var)
        self.cpf_entry.pack()

        def realizar_pesquisa():
            cpf_digitado = self.cpf_entry.get()

            # Consulta para obter informações do cadastro associadas ao CPF
            consulta_obter_cadastro = "SELECT nome, nascimento, telefone, email FROM cadastro WHERE cpf = ?"
            dados_para_consulta = (cpf_digitado,)
            self.cursor.execute(consulta_obter_cadastro, dados_para_consulta)
            resultado = self.cursor.fetchone()

            if resultado:
                # Preencher automaticamente os campos com os dados existentes
                nome, nascimento, telefone, email = resultado

                # Abrir uma nova janela para edição
                self.abrir_janela_edicao(nome, nascimento, telefone, email)
            else:
                messagebox.showinfo('Mensagem de Aviso', 'CPF não cadastrado. Insira um CPF válido.')

        # Botão de pesquisa
        self.pesquisar_button = tk.Button(cadastro, text="Pesquisar", command=realizar_pesquisa)
        self.pesquisar_button.pack()

    def abrir_janela_edicao(self, nome, nascimento, telefone, email):
        cpf_digitado = self.cpf_entry.get()
        janela_edicao = tk.Toplevel(self.cadastro)
        janela_edicao.title("Edição de cadastro")
        
        # Consulta para obter informações do cadastro associadas ao CPF
        consulta_obter_cadastro = "SELECT nome, nascimento, telefone, email FROM cadastro WHERE cpf = ?"
        dados_para_consulta = (cpf_digitado,)
        self.cursor.execute(consulta_obter_cadastro, dados_para_consulta)
        resultado = self.cursor.fetchone()

        if resultado:
            # Desempacotar os dados obtidos
            nome_atual, nascimento_atual, telefone_atual, email_atual = resultado

            
            # Atribuir os valores diretamente às variáveis de instância
            self.nome_var.set(nome_atual)
            # Formatar a data antes de inseri-la nos campos de entrada
            data_formatada = datetime.strptime(nascimento_atual, '%Y-%m-%d').strftime('%d-%m-%Y')
            self.nascimento_var.set(data_formatada)
            self.telefone_var.set(telefone_atual)
            self.email_var.set(email_atual)

            # Entry para nome
            tk.Label(janela_edicao, text="Nome:").pack()
            self.nome_entry = tk.Entry(janela_edicao)
            self.nome_entry.insert(0, nome_atual)  # Preencher com o valor atual
            self.nome_entry.pack()

            # Entry para nascimento
            tk.Label(janela_edicao, text="Nascimento (DD-MM-YYYY):").pack()
            self.nascimento_entry = tk.Entry(janela_edicao)
            self.nascimento_entry.insert(0, data_formatada)  # Preencher com o valor atual
            self.nascimento_entry.pack()

            # Entry para telefone
            tk.Label(janela_edicao, text="Telefone (XX)XXXXX-XXXX:").pack()
            self.telefone_entry = tk.Entry(janela_edicao)
            self.telefone_entry.insert(0, telefone_atual)  # Preencher com o valor atual
            self.telefone_entry.pack()

            # Entry para email
            tk.Label(janela_edicao, text="Email:").pack()
            self.email_entry = tk.Entry(janela_edicao)
            self.email_entry.insert(0, email_atual)  # Preencher com o valor atual
            self.email_entry.pack()


        # Botão de confirmação
        self.confirmar_button = tk.Button(janela_edicao, text="Confirmar", command=self.confirmar_edicao)
        self.confirmar_button.pack()

    def confirmar_edicao(self):
        # Obter os dados editados
        nome = self.nome_entry.get()
        nascimento = self.nascimento_entry.get()
        telefone = self.telefone_entry.get()
        email = self.email_entry.get()


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


        try:
            cpf = self.cpf_entry.get()
            if validar_cpf(cpf) and validar_data(nascimento) and validar_telefone(telefone):
                # Converter a data para o formato 'yyyy-mm-dd' para o SQLite
                data_formatada = datetime.strptime(nascimento, '%d-%m-%Y').strftime('%Y-%m-%d')
                # Executar uma consulta SQL para atualizar os dados no banco de dados
                consulta_atualizacao = "UPDATE cadastro SET nome=?, nascimento=?, telefone=?, email=? WHERE cpf=?"
                dados_para_atualizacao = (nome, data_formatada, telefone, email, cpf)
                # Executar a consulta
                self.cursor.execute(consulta_atualizacao, dados_para_atualizacao)
                # Confirmar a transação
                self.conn.commit()   
                # Fechar a conexão após a atualização
                self.fechar_conexao()
                messagebox.showinfo('Cadastro atualizado','Cadastro atualizado com sucesso!')
                # Fechar a janela de alteração após a atualização
                self.cadastro.destroy()
            else:
                messagebox.showinfo('Mensagem de Erro', 'Dados inválidos. Por favor, insira o CPF no formato xxx.xxx.xxx-xx, a data no formato correto (Dia-Mês-Ano) e o telefone no formato (xx) xxxxx-xxxx.')
        except ValueError as e:
            messagebox.showerror('Erro', str(e))
        except Exception as ex:
            messagebox.showerror('Erro', f'Erro inesperado: {str(ex)}')

#--------------------------------------------------------------------------------------------------------

    def pesquisar_cadastro(self):
        cadastro = tk.Tk()
        self.cadastro = cadastro
        self.cadastro.title("Pesquisa de cadastro")

        self.cpf_label = tk.Label(cadastro, text="Insira o CPF (no formato xxx.xxx.xxx-xx)")
        self.cpf_label.pack()

        self.cpf_var = tk.StringVar()
        self.cpf_entry = tk.Entry(cadastro, textvariable=self.cpf_var)
        self.cpf_entry.pack()

        def realizar_pesquisa():
            cpf_digitado = self.cpf_entry.get()

            # Consulta para obter informações do cadastro associadas ao CPF
            consulta_obter_cadastro = "SELECT nome, nascimento, telefone, email FROM cadastro WHERE cpf = ?"
            dados_para_consulta = (cpf_digitado,)
            self.cursor.execute(consulta_obter_cadastro, dados_para_consulta)
            resultado = self.cursor.fetchone()

            if resultado:
                nome, nascimento, telefone, email = resultado

                # Formatar a data para exibição
                data_formatada = datetime.strptime(nascimento, '%Y-%m-%d').strftime('%d-%m-%Y')

                # Criar nova janela para exibir os dados
                dados_janela = tk.Toplevel()
                dados_janela.title("Dados do Cadastro")

                # Adicionar rótulos e campos para os dados
                tk.Label(dados_janela, text=f"Nome: {nome}").pack()
                tk.Label(dados_janela, text=f"Nascimento: {data_formatada}").pack()
                tk.Label(dados_janela, text=f"Telefone: {telefone}").pack()
                tk.Label(dados_janela, text=f"Email: {email}").pack()
            else:
                messagebox.showinfo('Mensagem de Erro', 'CPF não encontrado. Por favor, insira um CPF existente.')

        # Botão para pesquisar e exibir os dados do cadastro associado ao CPF digitado
        self.pesquisar_cadastro_button = tk.Button(cadastro, text="Pesquisar Cadastro", command=realizar_pesquisa)
        self.pesquisar_cadastro_button.pack()

    def exibir_livros(self):
        janela_livros = tk.Toplevel(self.root)
        janela_livros.title("Lista de Livros")
        #janela_livros.geometry(padx=10, pady=10)
        
        # tk.Label(janela_livros, text='Livros|Autor|Data de Publicação|Descrição').pack(padx=10,pady=10)
        

        consulta_livros = "SELECT * FROM livros"
        self.cursor.execute(consulta_livros)
        livros = self.cursor.fetchall()
        # titulo = livros
        # Criar a Treeview
        tree = ttk.Treeview(janela_livros)
        # Definir os estilos para cabeçalhos em negrito
        estilo = ttk.Style()
        estilo.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Definir as colunas
        tree["columns"] = ("ID","Gênero","Título", "Autor", "Ano de Publicação", "Descrição")

        # Configurar as colunas
        tree.column("#0", width=0, stretch=tk.NO)  # Coluna invisível
        tree.column("ID", anchor=tk.W, width=200)
        tree.column("Gênero", anchor=tk.W, width=200)
        tree.column("Título", anchor=tk.W, width=200)
        tree.column("Autor", anchor=tk.W, width=200)
        tree.column("Ano de Publicação", anchor=tk.W, width=200)
        tree.column("Descrição", anchor=tk.W, width=500)
        

        # Configurar os cabeçalhos das colunas
        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("ID", text="ID", anchor=tk.W)
        tree.heading("Gênero", text="Gênero", anchor=tk.W)
        tree.heading("Título", text="Título", anchor=tk.W)
        tree.heading("Autor", text="Autor", anchor=tk.W)
        tree.heading("Ano de Publicação", text="Ano de Publicação", anchor=tk.W)
        tree.heading("Descrição", text="Descrição", anchor=tk.W)
        for livro in livros:
            # Verificar se a data é 'Varia' antes de tentar formatar
            data_publicacao = livro[4]
            if data_publicacao.lower() == 'varia':
                data_formatada = data_publicacao
            else:
                try:
                    data_formatada = datetime.strptime(data_publicacao, '%Y-%m-%d').strftime('%d-%m-%Y')
                except ValueError:
                    # Se a data não for válida, use o valor original
                    data_formatada = data_publicacao
            tree.insert("", tk.END, values=(livro[0], livro[1],livro[2], livro[3], data_formatada, livro[5]))

        # Adicionar a Treeview à janela
        tree.pack(padx=10, pady=10)
        





    def alugar_livro(self):
        aluguel_janela = tk.Toplevel(self.root)
        aluguel_janela.title("Aluguel de Livro")

        self.cpf_leitor_label = tk.Label(aluguel_janela, text="Incira o CPF")
        self.cpf_leitor_entry = tk.Entry(aluguel_janela)
        self.cpf_leitor_label.pack()
        self.cpf_leitor_entry.pack()

        self.id_livro_label = tk.Label(aluguel_janela, text="ID do Livro:")
        self.id_livro_entry = tk.Entry(aluguel_janela)
        self.id_livro_label.pack()
        self.id_livro_entry.pack()

    def devolver_livro(self): 

        messagebox.showinfo("Aluguel de Livro", "Coloque a funcionalidade de aluguel de livro aqui.")

    def devolver_livro(self):

        messagebox.showinfo("Devolução de Livro", "Coloque a funcionalidade de devolução de livro aqui.")

    def remover_cadastro(self):
        remover = tk.Tk()
        self.remover = remover
        self.remover.title("Remover Cadastro")
        

        self.cpf_label = tk.Label(self.remover, text="Insira o CPF a ser removido (no formato xxx.xxx.xxx-xx):")
        self.cpf_label.pack()

        self.cpf_var = tk.StringVar()
        self.cpf_entry = tk.Entry(self.remover, textvariable=self.cpf_var)
        self.cpf_entry.pack()
        
        def confirmar_remover_cadastro():
            cpf = self.cpf_entry.get()
                
            def validar_cpf(cpf):
                return len(cpf) == 14 and cpf[3] == '.' and cpf[7] == '.' and cpf[11] == '-'
            
            try:
            
                if validar_cpf(cpf):
                    # Verificar se o CPF existe no banco de dados
                    consulta_verificacao = "SELECT * FROM cadastro WHERE cpf = ?"
                    self.cursor.execute(consulta_verificacao, (cpf,))
                    resultado = self.cursor.fetchone()

                    if resultado:
                        # CPF encontrado, realizar a remoção
                        consulta_remocao = "DELETE FROM cadastro WHERE cpf = ?"
                        self.cursor.execute(consulta_remocao, (cpf,))
                        self.conn.commit()
                        messagebox.showinfo('Cadastro Removido', 'Cadastro removido com sucesso!')
                    else:
                        messagebox.showinfo('Mensagem de Aviso', 'CPF não encontrado. Insira um CPF válido.')
            except Exception as ex:
                messagebox.showerror('Erro', f'Erro inesperado: {str(ex)}')

            finally:
                # Fechar a conexão após a operação
                self.fechar_conexao()
            
            # Fechar a janela de remoção após a operação
            remover.destroy()

        self.confirmar_button = tk.Button(remover, text="Confirmar", command=confirmar_remover_cadastro)
        self.confirmar_button.pack()







# Crie a instância da interface gráfica
root = tk.Tk()
app = BibliotecaGUI(root)

# Execute o loop principal da interface gráfica

root.mainloop()

root.mainloop()
