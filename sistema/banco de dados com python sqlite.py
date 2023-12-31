import sqlite3
from datetime import datetime, timedelta
from prettytable import PrettyTable
import tkinter as tk
desejo = 0

# Conectar ao banco de dados (se não existir, será criado)
conn = sqlite3.connect('Biblioteca.db')

# Criar um cursor para interagir com o banco de dados
cursor = conn.cursor()

#Todas as funções-----------------------------------------------------------------------------------

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


# Função para validar o formato da data
def validar_data(nascimento):
    try:
        datetime.strptime(nascimento, '%d-%m-%Y')
        return True
    except ValueError:
        return False

# Função para validar o formato do cpf
def validar_cpf(cpf):
    return len(cpf) == 14 and cpf[3] == '.' and cpf[7] == '.' and cpf[11] == '-'

# Função para validar o formato do telefone
def validar_telefone(telefone):
    return len(telefone) == 14 and telefone[0] == '(' and telefone[3] == ')' and telefone[9] == '-'
#-------------------------------------------------------------------------------------------------------

print('\nBem-vindo ao programa de gestão de biblioteca!')

while True:

    # perguntar o que deseja fazer como parametro para o if
    desejo = input('''\nEscolha uma das opções abaixo:

Digite C para criar um cadastro
M para mudar um cadastro
P para pesquisar um cadastro
E para exibir a tabela de livros disponíveis
A para alugar um livro
D para devolver um livro
R para remover um cadastro
S para sair



O que você deseja fazer: ''')

#------------------------------------------------------------------------------------------------------
    # if para criação de cadastro
    if desejo.upper() == 'C':
        while True:

            print('\nVocê escolheu a criação de cadastro, Insira os dados solicitados abaixo')
            cpf = input('\nInsira o CPF (no formato xxx.xxx.xxx-xx): ')
            nome = input('\nInsira o nome: ')
            nascimento = input('\nInsira a data de nascimento (separada pelo sinal "-" Ex: Dia-Mes-Ano): ')
            telefone = input('\nInsira o telefone (no formato (xx)xxxxx-xxxx): ')
            email = input('\nInsira o email: ')

            if validar_cpf(cpf) and validar_data(nascimento) and validar_telefone(telefone):
                print('\nCadastro criado!')
                # Converter a data para o formato 'yyyy-mm-dd' para o SQLite
                data_formatada = datetime.strptime(nascimento, '%d-%m-%Y').strftime('%Y-%m-%d')
                # Executar uma consulta SQL para inserir uma variável no banco de dados
                consulta_insercao = "INSERT INTO cadastro (cpf, nome, nascimento, telefone, email) VALUES (?, ?, ?, ?, ?)"
                dados_para_inserir = (cpf, nome, data_formatada, telefone, email)
                # Executar a consulta
                cursor.execute(consulta_insercao, dados_para_inserir)
                # Confirmar a transação
                conn.commit()
                break
            else:
                print('Dados inválidos. Por favor, insira o CPF no formato xxx.xxx.xxx-xx, a data no formato correto (Dia-Mês-Ano) e o telefone no formato (xx) xxxxx-xxxx.')

#------------------------------------------------------------------------------------------------------
    # if para alteração de cadastro
    elif desejo.upper() == 'M':
        cpf_alterar = input('Você escolheu a alteração de cadastro, insira o CPF a ser alterado(no formato xxx.xxx.xxx-xx): ')
        consulta_verificacao = "SELECT * FROM cadastro WHERE cpf = ?"
        cursor.execute(consulta_verificacao, (cpf_alterar,))
        dado_do_banco = cursor.fetchone()
        if dado_do_banco:
            print(dado_do_banco)
            cpf, nome, nascimento, telefone, email, data, livro_alugado = dado_do_banco
            print("\nDados encontrados:")
            print("CPF:", cpf)
            print("Nome:", nome)
            print("Data de nascimento:", nascimento)
            print("Telefone:", telefone)
            print("Email:", email)
            confirma_alteracao = input('Deseja realmente alterar este cadastro? (S para Sim e N para Não): ')
            if confirma_alteracao.upper() == 'S':
                # Receber os novos dados
                novo_nome = input('Novo nome: ')
                novo_nascimento = input('Nova data de nascimento (separada pelo sinal "-" Ex: Dia-Mes-Ano): ')
                novo_telefone = input('Novo telefone (no formato (xx)xxxxx-xxxx): ')
                novo_email = input('Novo email: ')
                # Validar os novos dados
                if validar_data(novo_nascimento) and validar_telefone(novo_telefone):
                    
                    
                    # Executar uma consulta SQL para alterar os dados do cadastro
                    consulta_alteracao = "UPDATE cadastro SET nome=?, nascimento=?, telefone=?, email=? WHERE cpf=?"
                    novos_dados = (novo_nome, novo_nascimento, novo_telefone, novo_email, cpf_alterar)
                    cursor.execute(consulta_alteracao, novos_dados)
                    conn.commit()

                    print(f"\nCadastro com CPF {cpf_alterar} alterado com sucesso.")
                else:
                    print('\nNovos dados inválidos. Por favor, insira a nova data no formato correto (Dia-Mês-Ano) e o novo telefone no formato (xx) xxxxx-xxxx.')
            else:
                print('\nAlteração cancelada.')
        else:
            print(f"\nCPF {cpf_alterar} não encontrado no banco de dados.")
#------------------------------------------------------------------------------------------------------
    # if para pesquisar um cadastro
    elif desejo.upper() == 'P':
        # receber o cpf
        cpf = input('\nVocê escolheu pesquisar um cadastro, Insira o CPF cadastrado (no formato xxx.xxx.xxx-xx): ')

        # Executar uma consulta SQL para obter um dado do banco de dados
        consulta_sql = "SELECT * FROM cadastro WHERE cpf = ?"
        cursor.execute(consulta_sql, (cpf,))

        dado_do_banco = cursor.fetchone()

        # Usar o dado do banco de dados em uma instrução if
        if dado_do_banco:
            # Faça algo se o dado existir no banco de dados
            cpf, nome, nascimento, telefone, email, data, livro, data_aluguel, data_devolucao = dado_do_banco

            # Formatar a data de nascimento
            data_formatada = datetime.strptime(nascimento, "%Y-%m-%d").strftime("%d/%m/%Y")

            # Faça algo se o dado existir no banco de dados
            print("\nDados encontrados:")
            print("CPF:", cpf)
            print("Nome:", nome)
            print("Data de nascimento:", data_formatada)
            print("telefone:", telefone)
            print("email:", email)

            if livro is not None:  # Verificar se o livro alugado não é None
                print("Livro Alugado:", livro)
                print("Data do aluguel:", data_aluguel)
                print("Data de devolução:", data_devolucao)

            else:
                print("Livro Alugado: Nenhum livro cadastrado")
                print("Data do aluguel: Nenhum livro cadastrado")
                print("Data de devolução: Nenhum livro cadastrado")

        else:
            # Faça algo se o dado não existir no banco de dados
            print("\ncpf não encontrado")
            

        # Fechar a conexão
        

#------------------------------------------------------------------------------------------------------
# if para exibir a tabela de livros
    elif desejo.upper() == 'E':

            print('\nLIVROS DISPONÍVEIS ABAIXO:\n')
            # Selecionar todos os registros da tabela "livros"
            cursor.execute('SELECT * FROM livros')

            # Obter todos os registros
            livros = cursor.fetchall()

            # Criar uma tabela bonita
            tabela = PrettyTable()
            tabela.field_names = ["ID", "Título", "Autor", "Data de Publicação", "Descrição"]

            # Preencher a tabela com os dados
            for livro in livros:
                # Verificar se há dados suficientes na tupla
                if len(livro) >= 5:
                    try:
                        data_formatada = datetime.strptime(livro[4], '%Y-%m-%d').strftime('%d/%m/%Y')
                    except ValueError:
                        data_formatada = 'Data Desconhecida'
                tabela.add_row([livro[0], livro[2], livro[3], data_formatada, livro[5]])

            # Exibir a tabela formatada
            print(tabela)
            # Fechar a conexão

#------------------------------------------------------------------------------------------------------

    # if para Remover um cadastro
    elif desejo.upper() == 'R':
        cpf_remover = input('Você escolheu a remoção de cadastro, insira o CPF a ser removido(no formato xxx.xxx.xxx-xx): ')

    # Executar uma consulta SQL para verificar se o CPF existe no banco de dados
        consulta_verificacao = "SELECT * FROM cadastro WHERE cpf = ?"
        cursor.execute(consulta_verificacao, (cpf_remover,))
        dado_do_banco = cursor.fetchone()

        if dado_do_banco:
            cpf, nome, nascimento, telefone, email, _, _ = dado_do_banco
            print("Dados encontrados:")
            print("CPF:", cpf)
            print("Nome:", nome)
            print("Data de nascimento:", nascimento)
            print("Telefone:", telefone)
            print("Email:", email)

            confirma_remocao = input('Deseja realmente remover este cadastro? (S para Sim e N para Não): ')
            if confirma_remocao.upper() == 'S':
                # Executar uma consulta SQL para remover o cadastro
                consulta_remocao = "DELETE FROM cadastro WHERE cpf = ?"
                cursor.execute(consulta_remocao, (cpf_remover,))
                conn.commit()
                print(f"\nCadastro com CPF {cpf_remover} removido com sucesso.")
            else:
                print('\nRemoção cancelada.')
        else:
            print(f"\nCPF {cpf_remover} não encontrado no banco de dados.")
#------------------------------------------------------------------------------------------------------
    # if para alugar um livro
    elif desejo.upper() == 'A':
        # Solicitar o CPF do usuário
        cpf = input('Insira o CPF (no formato xxx.xxx.xxx-xx) para alugar o livro: ')

        # Executar uma consulta SQL para verificar se o CPF existe na tabela de cadastro
        consulta_cpf = "SELECT * FROM cadastro WHERE cpf = ?"
        cursor.execute(consulta_cpf, (cpf,))
        dados_cadastro = cursor.fetchone()

        if dados_cadastro:
            # Verificar se o usuário já possui um livro alugado
            if dados_cadastro[6] is not None:  # A sexta coluna (índice 5) é a coluna livro_alugado
                print(f'\nVocê já possui o livro "{dados_cadastro[6]}" alugado.')
                print(f'Devolva o livro atual antes de alugar um novo.')
            else:
                # Solicitar o ID do livro que a pessoa deseja alugar
                idLivro = input('Insira o ID do livro que deseja alugar: ')

                # Executar uma consulta SQL para obter informações sobre o livro
                consulta_livro = "SELECT * FROM livros WHERE idLivro = ?"
                cursor.execute(consulta_livro, (idLivro,))

                livro_selecionado = cursor.fetchone()

                if livro_selecionado:
                    # Mostrar informações do livro selecionado
                    print("\nInformações do livro selecionado:")
                    print("ID:", livro_selecionado[0])
                    print("Gênero:", livro_selecionado[1])
                    print("Título:", livro_selecionado[2])
                    print("Autor:", livro_selecionado[3])
                    print("Data de Publicação:", livro_selecionado[4])
                    print("Descrição:", livro_selecionado[5])

                    # Confirmar se a pessoa deseja alugar o livro
                    confirmacao_aluguel = input('Deseja alugar este livro? (S para Sim e N para Não): ')

                    if confirmacao_aluguel.upper() == 'S':
                        # Atualizar a tabela de cadastro com o livro alugado, data_aluguel e data_devolucao
                        data_aluguel = datetime.now().date()
                        data_devolucao = data_aluguel + timedelta(days=5)

                        update_cadastro_query = "UPDATE cadastro SET livro_alugado = ?, data_aluguel = ?, data_devolucao = ? WHERE cpf = ?"
                        cursor.execute(update_cadastro_query, (livro_selecionado[2], data_aluguel, data_devolucao, cpf))
            
                        print(f'\nLivro alugado com sucesso! Devolução até {data_devolucao.strftime("%d/%m/%Y")}.')
                    else:
                        print('Aluguel cancelado.')
                else:
                    print('\nLivro não encontrado.')
        else:
            print('\nCPF não encontrado.')
        # Commit as alterações no banco de dados
        conn.commit()
#------------------------------------------------------------------------------------------------------------
    # Devolver Livro:
    elif desejo.upper() == 'D':
        # Solicitar o CPF do usuário
        cpf = input('Insira o CPF (no formato xxx.xxx.xxx-xx) para devolver o livro: ')

        # Executar uma consulta SQL para verificar se o CPF existe na tabela de cadastro
        consulta_cpf = "SELECT * FROM cadastro WHERE cpf = ?"
        cursor.execute(consulta_cpf, (cpf,))
        dados_cadastro = cursor.fetchone()

        if dados_cadastro:
            # Verificar se o usuário possui um livro alugado
            if dados_cadastro[6] is not None:  # A sexta coluna (índice 5) é a coluna livro_alugado
                # Mostrar informações do livro alugado
                print('\nVocê tem o livro "{}" alugado.'.format(dados_cadastro[6]))
                confirmacao_devolucao = input('Deseja devolver este livro? (S para Sim e N para Não): ')

                if confirmacao_devolucao.upper() == 'S':
                    # Calcular atraso e mensagem
                    atraso = calcular_atraso(datetime.now().date(), dados_cadastro[8])  # Oitava coluna (índice 7) é a coluna data_devolucao
                    mensaje = verificar_atraso(atraso)

                    # Atualizar a tabela de cadastro para indicar que o livro foi devolvido
                    update_cadastro_query = "UPDATE cadastro SET livro_alugado = NULL, data_aluguel = NULL, data_devolucao = NULL WHERE cpf = ?"
                    cursor.execute(update_cadastro_query, (cpf,))
                    print(f'Livro devolvido com sucesso! {mensaje}')
                    # Commit as alterações no banco de dados
                    conn.commit()
                else:
                    print('Devolução cancelada.')
            else:
                print('Você não possui nenhum livro alugado no momento.')
        else:
            print('CPF não encontrado.')



#------------------------------------------------------------------------------------------------------
    #if para Encerrar programa
    elif desejo.upper() == 'S':
        print('\nVolte sempre!\n')
        break

#------------------------------------------------------------------------------------------------------

    else:
        print('\nComando não encontrado...\n')
        print('Digite um comando valido!')

# Fechar a conexão fora do bloco elif
conn.close()
