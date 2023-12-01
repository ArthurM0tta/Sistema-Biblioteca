
import sqlite3
from datetime import datetime, timedelta
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
            consulta_obter_cadastro = "SELECT nome, nascimento, telefone, email, livro_alugado, data_aluguel, data_devolucao FROM cadastro WHERE cpf = ?"
            dados_para_consulta = (cpf_digitado,)
            self.cursor.execute(consulta_obter_cadastro, dados_para_consulta)
            resultado = self.cursor.fetchone()

            if resultado:
                nome, nascimento, telefone, email, livro_alugado, data_aluguel, data_devolucao = resultado

                # Formatar a data para exibição
                data_formatada = datetime.strptime(nascimento, '%Y-%m-%d').strftime('%d-%m-%Y')
                data_aluguel_formatada = datetime.strptime(data_aluguel, '%Y-%m-%d').strftime('%d-%m-%Y')
                data_devolucao_formatada = datetime.strptime(data_devolucao, '%Y-%m-%d').strftime('%d-%m-%Y')

                # Verificar se a entrega está atrasada
                hoje = datetime.now().date()
                data_devolucao = datetime.strptime(data_devolucao, '%Y-%m-%d').date()

                if hoje > data_devolucao:
                    status_entrega = "Entrega Atrasada"
                else:
                    status_entrega = "Dentro do Prazo"
                # Criar nova janela para exibir os dados
                dados_janela = tk.Toplevel()
                dados_janela.title("Dados do Cadastro")

                # Adicionar rótulos e campos para os dados
                tk.Label(dados_janela, text=f"Nome: {nome}").pack()
                tk.Label(dados_janela, text=f"Nascimento: {data_formatada}").pack()
                tk.Label(dados_janela, text=f"Telefone: {telefone}").pack()
                tk.Label(dados_janela, text=f"Email: {email}").pack()
                tk.Label(dados_janela, text=f"Livro alugado: {livro_alugado}").pack()
                tk.Label(dados_janela, text=f"Data do Aluguel: {data_aluguel_formatada}").pack()
                tk.Label(dados_janela, text=f"Data de Devolução: {data_devolucao_formatada}").pack()
                tk.Label(dados_janela, text=f"Status da Entrega: {status_entrega}").pack()

            else:
                messagebox.showinfo('Mensagem de Erro', 'CPF não encontrado. Por favor, insira um CPF existente.')

        # Botão para pesquisar e exibir os dados do cadastro associado ao CPF digitado
        self.pesquisar_cadastro_button = tk.Button(cadastro, text="Pesquisar Cadastro", command=realizar_pesquisa)
        self.pesquisar_cadastro_button.pack()

    def exibir_livros(self):
        messagebox.showinfo("Exibição de Livros", "Coloque a exibição de livros aqui.")
#---------------------------------------------------------------------------------------------------------------------------------------------
    
    def alugar_livro(self):
        aluguel_janela = tk.Toplevel(self.root)
        aluguel_janela.title("Aluguel de Livro")

        self.cpf_leitor_label = tk.Label(aluguel_janela, text="Insira o CPF (no formato xxx.xxx.xxx-xx)")
        self.cpf_leitor_entry = tk.Entry(aluguel_janela)
        self.cpf_leitor_label.pack()
        self.cpf_leitor_entry.pack()

        def verificar_cpf():
            cpf_digitado = self.cpf_leitor_entry.get()

            # Consultar o banco de dados para verificar se o CPF existe
            consulta_cpf = "SELECT * FROM cadastro WHERE cpf = ?"
            dados_para_consulta = (cpf_digitado,)
            self.cursor.execute(consulta_cpf, dados_para_consulta)
            leitor = self.cursor.fetchone()

            if leitor:
                # Se o CPF existir, abrir outra janela para inserir o ID do livro
                self.abrir_janela_inserir_livro(leitor)
                aluguel_janela.destroy()
            else:
                messagebox.showinfo("Aviso", "CPF não encontrado. Insira um CPF válido.")

        # Botão para verificar o CPF
        self.verificar_cpf_button = tk.Button(aluguel_janela, text="Verificar CPF", command=verificar_cpf)
        self.verificar_cpf_button.pack()

    def abrir_janela_inserir_livro(self, leitor):
        # Verificar se o leitor já possui um livro alugado
        if leitor[6]:  # A coluna correspondente ao livro alugado (índice 6) não é None
            # Mostrar uma mensagem indicando que o leitor já possui um livro alugado
            messagebox.showinfo("Aviso", f"Aluguel Indisponível: \nEste cadastro já possui o livro '{leitor[6]}' alugado.")
        else:
            # Continuar com a lógica atual para inserir o ID do livro
            janela_livro = tk.Toplevel(self.root)
            janela_livro.title("Inserir ID do Livro")

            self.id_livro_label = tk.Label(janela_livro, text='''Insira o ID do Livro que deseja alugar: 
            (Consulte o ID na página inicial no botão de Exibir Livros)''')
            self.id_livro_entry = tk.Entry(janela_livro)
            self.id_livro_label.pack()
            self.id_livro_entry.pack()

            def exibir_detalhes_livro():
                idLivro = self.id_livro_entry.get()

                # Consultar o banco de dados para obter os detalhes do livro
                consulta_livro = "SELECT * FROM livros WHERE idLivro = ?"
                dados_para_consulta = (idLivro,)
                self.cursor.execute(consulta_livro, dados_para_consulta)
                livro = self.cursor.fetchone()
        
                if livro:
                    # Se o livro existir, abrir uma janela para mostrar os detalhes
                    self.mostrar_detalhes_livro(janela_livro, livro, leitor)
                else:
                    messagebox.showinfo("Aviso", "ID do livro não encontrado. Insira um ID válido.")

        # Botão para exibir detalhes do livro
        tk.Button(janela_livro, text="Exibir Detalhes", command=exibir_detalhes_livro).pack()


    def mostrar_detalhes_livro(self, janela_livro, livro, leitor):
        # Esta função abre uma janela para mostrar os detalhes do livro e confirmar o aluguel
        janela_detalhes = tk.Toplevel(self.root)
        janela_detalhes.title("Detalhes do Livro")

        # Mostrar os detalhes do livro
        detalhes_label = tk.Label(janela_detalhes, text=f"Detalhes do Livro:\n\nID: {livro[0]}\nGênero: {livro[1]}\nTítulo: {livro[2]}\nAutor: {livro[3]}\nAno de Publicação: {livro[4]}\nDescrição: {livro[5]}")
        detalhes_label.pack()
        
        # Frame para conter os botões
        frame_botoes = tk.Frame(janela_detalhes)
        frame_botoes.pack(side=tk.BOTTOM, padx=5)

        # Botão para alugar o livro
        alugar_button = tk.Button(frame_botoes, text="Alugar", command=lambda: self.alugar_confirmado(janela_detalhes, livro, leitor))
        alugar_button.pack(side=tk.LEFT, padx=5)

        # Botão para cancelar
        cancelar_button = tk.Button(frame_botoes, text="Cancelar", command=lambda: self.cancelar_aluguel(janela_detalhes))
        cancelar_button.pack(side=tk.LEFT, padx=5)


    def alugar_confirmado(self, janela_detalhes, livro, leitor):
        # Implemente a lógica para concluir o aluguel aqui

        # Obtém o ID do leitor
        id_leitor = leitor[0]

        # Obtém as informações do livro
        livro = livro[0]
        nome_livro = livro[2]

        # Data atual
        data_aluguel = datetime.now().strftime('%Y-%m-%d')

        # Data de devolução (5 dias a partir da data de aluguel)
        data_devolucao = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')

        # Atualiza a tabela de cadastro
        consulta_atualizacao = "UPDATE cadastro SET livro_alugado=?, data_aluguel=?, data_devolucao=? WHERE id=?"
        dados_para_atualizacao = (nome_livro, data_aluguel, data_devolucao, id_leitor)
        self.cursor.execute(consulta_atualizacao, dados_para_atualizacao)
        self.conn.commit()

        # Fechar as janelas após concluir o aluguel
        janela_detalhes.destroy()
        # Se desejar, você pode chamar outra função ou procedimento para finalizar o aluguel

    def cancelar_aluguel(self, janela_detalhes):
        # Esta função é chamada quando o usuário decide cancelar o aluguel
        # Fechar a janela de detalhes
        janela_detalhes.destroy()

    def devolver_livro(self): 

       def abrir_janela_devolver_livro(self, leitor):
    # Verificar se o leitor possui um livro alugado
        if leitor[6]:  # A coluna correspondente ao livro alugado (índice 6) não é None
        # Continuar com a lógica para devolução do livro
         janela_devolucao = tk.Toplevel(self.root)
         janela_devolucao.title("Devolver Livro")

        # Mostrar os detalhes do livro alugado
        detalhes_label = tk.Label(janela_devolucao, text=f"Detalhes do Livro Alugado:\n\nID: {leitor[6]}")  # 6 é o índice da coluna do livro alugado
        detalhes_label.pack()

        # Frame para conter os botões
        frame_botoes = tk.Frame(janela_devolucao)
        frame_botoes.pack(side=tk.BOTTOM, padx=5)

        # Botão para devolver o livro
        devolver_button = tk.Button(frame_botoes, text="Devolver", command=lambda: self.devolver_confirmado(janela_devolucao, leitor))
        devolver_button.pack(side=tk.LEFT, padx=5)

        # Botão para cancelar
        cancelar_button = tk.Button(frame_botoes, text="Cancelar", command=lambda: self.cancelar_devolucao(janela_devolucao))
        cancelar_button.pack(side=tk.LEFT, padx=5)
        
     

def devolver_confirmado(self, janela_devolucao, leitor):
    # Lógica para devolução do livro
    livro_devolvido = leitor[6]  # Obtém o ID do livro alugado
    # Atualizar o banco de dados para indicar que o livro foi devolvido (definir a coluna correspondente ao livro alugado como None)
    update_query = "UPDATE cadastro SET livro_alugado = NULL WHERE cpf = ?"
    dados_para_atualizacao = (leitor[0],)  # Assumindo que leitor[0] contém o CPF
    self.cursor.execute(update_query, dados_para_atualizacao)
    self.conexao.commit()

    # Mostrar mensagem de sucesso
    messagebox.showinfo("Sucesso", f"Livro '{livro_devolvido}' devolvido com sucesso.")

    # Fechar a janela de devolução
    janela_devolucao.destroy()

def cancelar_devolucao(self, janela_devolucao):
    # Lógica para cancelar a devolução (se necessário)
    # Pode não ser necessário fazer nada aqui, dependendo da lógica do seu programa
    janela_devolucao.destroy()


    def remover_cadastro(self):
        messagebox.showinfo("Remoção de Cadastro", "Coloque a remoção de cadastro aqui.")




# Crie a instância da interface gráfica
root = tk.Tk()
app = BibliotecaGUI(root)

# Execute o loop principal da interface gráfica

root.mainloop()

root.mainloop()