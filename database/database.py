import sqlite3
import os

db_path = os.path.abspath("database/contatos.db")

def conexao():
    print("Banco usado:", db_path)
    return sqlite3.connect(db_path)
def criar_tabelas():
    try:
        with conexao() as con:
            cur = con.cursor()
            #TABELA DE CLIENTES
            cur.execute("""    
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    telefone TEXT,
                    endereco TEXT,
                    email TEXT,
                    plano_atual TEXT,
                    status TEXT,
                    categoria TEXT,
                    data_prospeccao TEXT,
                    data_qualificacao TEXT,
                    data_conversao TEXT,
                    idade TEXT,
                    observacao TEXT    
                )
            """)

            cur.execute("""    
                CREATE TABLE IF NOT EXISTS leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    telefone TEXT,
                    endereco TEXT,
                    email TEXT,
                    status TEXT,
                    categoria TEXT,
                    data_prospeccao TEXT,
                    data_qualificacao TEXT,
                    idade TEXT,
                    observacao TEXT
                )
            """)
            cur.execute("""    
                CREATE TABLE IF NOT EXISTS prospeccao (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    telefone TEXT,
                    endereco TEXT,
                    email TEXT,
                    status TEXT,
                    categoria TEXT,
                    data_prospeccao TEXT,
                    idade TEXT,
                    observacao TEXT      
                )
            """)
            return (True, "Tabelas criadas com sucesso.")
    except sqlite3.IntegrityError as e:
        return (False, f"Erro de integridade: {str(e)}")
    except sqlite3.OperationalError as e:
        return (False, f"Erro operacional: {str(e)}")
    except Exception as e:
        return (False, f"Erro inesperado: {str(e)}")
#================================= CLIENTES =======================================#

def inserir_cliente(data: dict):
    print("Database...")
    """
    Insere um cliente na tabela 'clientes' usando dict.
    Retorna (True, id) se OK, ou (False, mensagem) se erro.
    """
    #                                         EXEMPLO DAS COLOUNAS
    colunas = [
        "nome",
        "telefone",
        "endereco",
        "email",
        "plano_atual",
        "status",
        "categoria",
        "data_prospeccao",
        "data_qualificacao",
        "data_conversao",
        "idade",
        "observacao"
    ]
    #                                             REGRA DE OBRIGATORIOS
    obrigatorios = ["nome", "telefone"]
    for campo in obrigatorios:
        if campo not in data or not str(data[campo]).strip():
            return (False, f"O campo '{campo}' é obrigatório.")
    #                                            NORMALIZACAO DOS DADOS E FILTRAGEM
    dado = {}
    for campo in colunas:
        valor = data.get(campo, "")

        if isinstance(valor, str):
            valor = valor.strip()

        if campo == "telefone":
            valor = "".join(filter(str.isdigit, valor))  # mantém só números
            if len(valor) > 2:
                valor = valor[:2] + " " + valor[2:]  # adiciona espaço após os dois primeiros dígitos

        if campo in ["data_prospeccao", "data_qualificacao", "data_conversao"]:
            if valor:
                valor = valor.replace("/", "-")

        dado[campo] = valor
    if not dado:
        return (False, "Nenhum campo válido para inserir.")
    print("Campos obrigatórios verificados:", obrigatorios)
    
    #                                          MONTAGEM DA INJECAO SQL COM VALIDACAO

    campos_sql = ", ".join(dado.keys())
    placeholders = ", ".join(["?"] * len(dado))
    valores = list(dado.values())

    sql = f"INSERT INTO clientes ({campos_sql}) VALUES ({placeholders})"
    print("Dict final para insert:", dado)
    print("SQL a executar:", campos_sql)
    #                                          EXECUCAO SQL
    try: 
        with conexao() as con:
            cur = con.cursor()
            cur.execute(sql, valores)
            return (True, cur.lastrowid)

    except sqlite3.IntegrityError as e:
        return (False, f"Erro de integridade: {str(e)}")
    except sqlite3.OperationalError as e:
        return (False, f"Erro operacional: {str(e)}")
    except Exception as e:
        return (False, f"Erro inesperado: {str(e)}")

def remover_cliente(id: int):
    try: 
        with conexao() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM clientes WHERE id = ?", (id,))
            return (True, cur.lastrowid)

    except sqlite3.IntegrityError as e:
        return (False, f"Erro de integridade: {str(e)}")
    except sqlite3.OperationalError as e:
        return (False, f"Erro operacional: {str(e)}")
    except Exception as e:
        return (False, f"Erro inesperado: {str(e)}")

def listar_todos_clientes():
    with conexao() as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM clientes")
        result = cur.fetchall()
    return result

def limpar_tabela(nome_tabela: str):
    """
    Limpa todos os dados da tabela e reseta o AUTOINCREMENT.
    """
    try:
        with conexao() as con:
            cur = con.cursor()
            # Deleta todos os registros
            cur.execute(f"DELETE FROM {nome_tabela}")
            # Reseta o AUTOINCREMENT
            cur.execute(f"DELETE FROM sqlite_sequence WHERE name='{nome_tabela}'")

        print(f"Tabela '{nome_tabela}' limpa e AUTOINCREMENT resetado com sucesso.")
        return True
    except sqlite3.OperationalError as e:
        print(f"Erro operacional: {e}")
        return False
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return False

def atualizar_cliente(id: int, dados: dict):
    colunas = [
        "nome",
        "telefone",
        "endereco",
        "email",
        "plano_atual",
        "status",
        "categoria",
        "data_prospeccao",
        "data_qualificacao",
        "data_conversao",
        "idade",
        "observacao"
    ]

    # Campos obrigatórios
    obrigatorios = ["nome", "telefone"]
    for campo in obrigatorios:
        if campo not in dados or not str(dados[campo]).strip():
            return (False, f"O campo '{campo}' é obrigatório.")

    # Normalização e filtragem
    dado = {}
    for campo in colunas:
        valor = dados.get(campo, "")
        if isinstance(valor, str):
            valor = valor.strip()

        if campo == "telefone":
            valor = "".join(filter(str.isdigit, valor))  # mantém só números
            if len(valor) > 2:
                valor = valor[:2] + " " + valor[2:]  # adiciona espaço após os dois primeiros dígitos

        if campo in ["data_prospeccao", "data_qualificacao", "data_conversao"]:
            if valor:
                valor = valor.replace("/", "-")

        if valor != "":
            dado[campo] = valor  # só adiciona campos com valor

    if not dado:
        return (False, "Nenhum campo válido para atualizar.")

    # Montagem do SQL UPDATE
    set_sql = ", ".join([f"{chave} = ?" for chave in dado.keys()])
    valores = list(dado.values())
    valores.append(id)  # para o WHERE

    sql = f"UPDATE clientes SET {set_sql} WHERE id = ?"

    # Execução SQL
    try:
        with conexao() as con:
            cur = con.cursor()
            cur.execute(sql, valores)
            if cur.rowcount == 0:
                return (False, "Nenhum cliente encontrado com esse ID.")
            return (True, "Cliente atualizado com sucesso.")

    except sqlite3.IntegrityError as e:
        return (False, f"Erro de integridade: {str(e)}")
    except sqlite3.OperationalError as e:
        return (False, f"Erro operacional: {str(e)}")
    except Exception as e:
        return (False, f"Erro inesperado: {str(e)}")

def listar_ids():
    try:
        with conexao() as con:
            cur = con.cursor()
            cur.execute("SELECT id FROM clientes")
            ids = [row[0] for row in cur.fetchall()]
            return ids
    except sqlite3.OperationalError as e:
        print(f"Erro operacional: {e}")
        return False
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return False 

def resetar_autoincrement():
    try: 
        with conexao() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM sqlite_sequence WHERE name = 'clientes'")
            con.commit()
            return (True, cur.lastrowid)

    except sqlite3.IntegrityError as e:
        return (False, f"Erro de integridade: {str(e)}")
    except sqlite3.OperationalError as e:
        return (False, f"Erro operacional: {str(e)}")
    except Exception as e:
        return (False, f"Erro inesperado: {str(e)}")

def buscar_cliente_por_id(id_cliente: int):
    try:
        with conexao() as con:
            cur = con.cursor()
            cur.execute("SELECT id, nome, telefone, endereco, email, plano_atual, status, categoria, data_prospeccao, data_qualificacao, data_conversao, idade, observacao FROM clientes WHERE id = ?", (id_cliente,))
            resultado = cur.fetchone()

            # Se não existir
            # if not resultado:
            #     return None

            # Retorna como dict
            return {
                "id": resultado[0],
                "nome": resultado[1],
                "telefone": resultado[2],
                "endereco": resultado[3],
                "email": resultado[4],
                "plano_atual": resultado[5],
                "status": resultado[6],
                "categoria": resultado[7],
                "data_prospeccao": resultado[8],
                "data_qualificacao": resultado[9],
                "data_conversao": resultado[10],
                "idade": resultado[11],
                "observacao": resultado[12]
            }

    except Exception as e:
        print("Erro:", e)
        return None