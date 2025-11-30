import sqlite3



def conectar():
    """Cria e retorna a conexao com o banco de dados se não existirem..."""
    return sqlite3.connect(DB_NAME, timeout=5)
def criar_tabelas():
    try:
        with conectar() as con:
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


# def teste():
#     import sqlite3

#     con = sqlite3.connect(DB_NAME, timeout=5)
#     cur = con.cursor()

#     cur.execute("INSERT INTO clientes (nome, telefone, endereco) VALUES (?, ?, ?)",
#                 ["Teste Lock", "123456789", ''])
#     con.commit()  # aqui trava se banco bloqueado

#     con.close()

# teste()