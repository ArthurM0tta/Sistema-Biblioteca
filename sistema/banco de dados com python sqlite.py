import sqlite3
from datetime import datetime
from prettytable import PrettyTable
desejo = 0

# Conectar ao banco de dados (se não existir, será criado)
conn = sqlite3.connect('Biblioteca.db')

# Criar um cursor para interagir com o banco de dados
cursor = conn.cursor()




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
        while True:
            print('\nVocê escolheu Mudar/alterar um cadastro, Insira quais dados você deseja alterar')
            alter = input('''\nDigite N para alterar o nome
D para alterar a data de nascimento
L para alterar o livro alugado (apenas caso haja algum erro de seleção!) ''')
            # Converter a entrada para minúsculas
            alter = alter.upper()

            if len(alter) != 1 or alter not in ['N', 'D', 'S', 'L']:
                print('Comando não encontrado...')
            else:
                print('tudo certo')
                break

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
            print("Livro Alugado:", livro)
            print("Data do aluguel:", data_aluguel)
            print("Data de devolução:", data_devolucao)
        
        else:
            # Faça algo se o dado não existir no banco de dados
            print("\ncpf não encontrado")
            

        # Fechar a conexão
        conn.close()

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
            conn.close()


#------------------------------------------------------------------------------------------------------

    # if para Remover um cadastro
    elif desejo.upper() == 'R':
        conf = input('Você escolheu a remoção de cadastro, deseja prosseguir? (S para Sim e N para Não) ')
        if conf.upper() == 'S':
            print('OK! para prosseguir insira o cpf cadastrado a ser removido: ')
        else:
            print('\nOK! Retornando para o menu de escolha!')

#------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------
    # if para Encerrar programa
    elif desejo.upper() == 'S':
        print('\nVolte sempre!\n')
        break

#------------------------------------------------------------------------------------------------------

    else:
        print('\nComando não encontrado...\n')
        print('Digite um comando valido!')
