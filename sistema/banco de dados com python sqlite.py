import sqlite3
from datetime import datetime
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
        cpf_alterar = input('Você escolheu a alteração de cadastro, insira o CPF a ser alterado: ')
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

                    print(f"Cadastro com CPF {cpf_alterar} alterado com sucesso.")
                else:
                    print('Novos dados inválidos. Por favor, insira a nova data no formato correto (Dia-Mês-Ano) e o novo telefone no formato (xx) xxxxx-xxxx.')
            else:
                print('Alteração cancelada.')
        else:
            print(f"CPF {cpf_alterar} não encontrado no banco de dados.")
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
            cpf, nome, nascimento, telefone, email, data, livro = dado_do_banco

            # Formatar a data de nascimento
            data_formatada = datetime.strptime(nascimento, "%Y-%m-%d").strftime("%d/%m/%Y")

            # Faça algo se o dado existir no banco de dados
            print("\nDados encontrados:")
            print("CPF:", cpf)
            print("Nome:", nome)
            print("Data de nascimento:", data_formatada)
            print("telefone:", telefone)
            print("email:", email)
            print("data do aluguel:", data)
            print("Livro Alugado:", livro)
        
        else:
            # Faça algo se o dado não existir no banco de dados
            print("\ncpf não encontrado")
            

        # Fechar a conexão
        conn.close()

#------------------------------------------------------------------------------------------------------
    # if para Remover um cadastro
    elif desejo.upper() == 'R':
      cpf_remover = input('Você escolheu a remoção de cadastro, insira o CPF a ser removido: ')

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
                print(f"Cadastro com CPF {cpf_remover} removido com sucesso.")
            else:
                print('Remoção cancelada.')
      else:
        print(f"CPF {cpf_remover} não encontrado no banco de dados.")
#------------------------------------------------------------------------------------------------------




#------------------------------------------------------------------------------------------------------
    #if para Encerrar programa
    elif desejo.upper() == 'S':
        print('\nVolte sempre!\n')
        break

#------------------------------------------------------------------------------------------------------

    else:
       print('\nComando não encontrado...\n')
       print('Digite um comando valido!')
