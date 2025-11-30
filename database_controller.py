import sqlite3
from database.database import *
import time

class DatabaseController:
    def __init__(self):
        pass

    def inserir_dados_clientes(self, dados):
        try:
            debug = inserir_cliente(dados)
            return debug
        except Exception as e:
            return e
        
    def remover_dados_por_id(self, id: int):
        lista_ids = listar_ids()
        try:
            if id in lista_ids:
                resultado_remocao = remover_cliente(id)
                return True, resultado_remocao

            if id not in lista_ids:
                print(f"lista de ids: {lista_ids}")
                return False, "ID não encontrado"

        except Exception as e:
            return False, str(e)

    def atualizar_cliente(self, id: int, dados: dict):
        try:
            debug = atualizar_cliente(id, dados)
            return debug
        except Exception as e:
            return e

    def buscar_cliente_por_id(self, id: int):
        try:
            resultado = buscar_cliente_por_id(id)
            return True, resultado
        except Exception as e:
            return False, str(e)
    
    def listar_ids(self):       
        try:
            resultado = listar_ids()
            return resultado
        except Exception as e:
            return False, str(e)
        