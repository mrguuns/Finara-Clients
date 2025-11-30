import flet as ft
from telas.overlays.overlay_adicionar_clientes import overlay_adicionar_clientes
from overlay_manager import *
import os
from app_state import AppState

from database.database import inserir_cliente, listar_todos_clientes , criar_tabelas, limpar_tabela

class ListaClientes:
    def __init__(self, page: ft.Page):
        self.page = page
        self.lista_view = ft.ListView(expand=True, spacing=5, padding=ft.padding.only(top=60, bottom=45))
        self.CATEGORIAS = ["todos", "cliente", "lead", "prospecção"]
    
    def resetar_tabela(self):
        limpar_tabela("clientes")
        time.sleep(0.5)
        self.on_segmented_change()

    def filtrar_por_categoria(self, categoria_selecionada):
        clientes = listar_todos_clientes()

        categoria_selecionada = categoria_selecionada.lower()
        if categoria_selecionada == "todos":
            return clientes

        return [
            c for c in clientes
            if c[7].lower() == categoria_selecionada
        ]    

    def atualizar_lista_por_categoria(self, cliente):
        self.lista_view.controls.clear()

        for id, nome, telefone, endereco, email, plano_atual, status, categoria, data_prospeccao, data_qualificacao, data_conversao, idade, observacao in cliente:
            cliente_card = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(spans=[
                            ft.TextSpan(text=f"Id:  "),
                            ft.TextSpan(text=f"{id}", style=ft.TextStyle(weight="bold")),
                        ]),
                        ft.Container(width=20),
                        ft.Text(spans=[
                            ft.TextSpan(text=f"Nome:  "),
                            ft.TextSpan(text=f"{nome}", style=ft.TextStyle(weight="bold", color="#5eff00")),
                        ]),
                        ft.Container(width=20),
                        ft.Text(spans=[
                            ft.TextSpan(text=f"Telefone:  "),
                            ft.TextSpan(text=f"{telefone}", style=ft.TextStyle(weight="bold")),
                        ]),
                        ft.Container(width=20),
                        ft.Text(spans=[
                            ft.TextSpan(text=f"Endereço:  "),
                            ft.TextSpan(text=f"{endereco}", style=ft.TextStyle(weight="bold")),
                        ]),
                        ft.Container(width=20),
                        ft.Text(spans=[
                            ft.TextSpan(text=f"Email:  "),
                            ft.TextSpan(text=f"{email}", style=ft.TextStyle(weight="bold")),
                        ]),
                        ft.Container(width=20),
                        ft.Text(spans=[
                            ft.TextSpan(text=f"Plano Atual:  "),
                            ft.TextSpan(text=f"{plano_atual}", style=ft.TextStyle(weight="bold")),
                        ]),
                        ft.Container(width=20),
                        ft.Text(spans=[
                            ft.TextSpan(text=f"Status:  "),
                            ft.TextSpan(text=f"{status}", style=ft.TextStyle(weight="bold")),
                        ]),
                        ft.Container(width=20),
                        ft.Text(spans=[
                            ft.TextSpan(text=f"Categoria:  "),
                            ft.TextSpan(text=f"{categoria}", style=ft.TextStyle(weight="bold")),
                        ]),
                        ft.Container(width=20),
                        ft.Text(spans=[
                            ft.TextSpan(text=f"Data de Prospecção:  "),
                            ft.TextSpan(text=f"{data_prospeccao}", style=ft.TextStyle(weight="bold")),
                        ]),
                        ft.Container(width=20),
                        ft.Text(spans=[
                            ft.TextSpan(text=f"Data de Qualificação:  "),
                            ft.TextSpan(text=f"{data_qualificacao}", style=ft.TextStyle(weight="bold")),
                        ]),
                        ft.Container(width=20),
                        ft.Text(spans=[
                            ft.TextSpan(text=f"Data de Conversão:  "),
                            ft.TextSpan(text=f"{data_conversao}", style=ft.TextStyle(weight="bold")),
                        ]),
                        ft.Container(width=20),
                        ft.Text(spans=[
                            ft.TextSpan(text=f"Idade:  "),
                            ft.TextSpan(text=f"{idade}", style=ft.TextStyle(weight="bold")),
                        ]),
                        ft.Container(width=20),
                        ft.Text(spans=[
                            ft.TextSpan(text=f"Observação:  "),
                            ft.TextSpan(text=f"{observacao}", style=ft.TextStyle(weight="bold")),
                        ]),
                    ],
                    spacing=3
                ),
                border=ft.border.all(width=1, color="#18d1ff"),
                padding=10,
                margin=ft.margin.only(bottom=10),
                bgcolor="#272727",
                border_radius=5,
                expand=True,
            )
            self.lista_view.controls.append(cliente_card)
        self.lista_view.update()
    
    def on_segmented_change(self, e=None):
        self.idx = self.seg_control.selected_index
        categoria = self.CATEGORIAS[self.idx].lower()
        print(categoria)
        clientes_filtrados = self.filtrar_por_categoria(categoria)

        print(f"Cliente filtrado: {clientes_filtrados}")
        self.atualizar_lista_por_categoria(clientes_filtrados)
        self.page.update()
    
    # --- Parte superior da lista (botões) ---
    def header_botoes(self):
        header_botoes = ft.Row(
            controls=[
                ft.IconButton(icon=ft.Icons.EDIT),
                ft.IconButton(icon=ft.Icons.ADD),
                ft.IconButton(icon=ft.Icons.LIST, on_click=lambda e: self.on_segmented_change(e)),
                ft.IconButton(icon=ft.Icons.REMOVE, on_click=lambda e: self.resetar_tabela()), 
            ],
            alignment="center",
        )
        return header_botoes

    def barra_botoes(self):
        barra_botoes = ft.Container(
            content=self.header_botoes(),
            top=10,
        )
        return barra_botoes
    
    def lista_com_scroll(self):
        lista_com_scroll = ft.Container(
            width=425,
            height=800,
            bgcolor="#0E0E0E",
            # border=ft.border.all(width=1, color="#18d1ff"),
            padding=10,
            border_radius=10,
            content=ft.Column(
                controls=[
                    self.lista_view,
                ]
            )
        )
        return lista_com_scroll

    def segmented(self):
    # --- Categorias fixas ---
        segmented = ft.CupertinoSlidingSegmentedButton(
            selected_index=0,
            on_change=self.on_segmented_change,
            thumb_color=ft.Colors.with_opacity(opacity=0.6,color="#00eeff"),
            controls=[
                ft.Text("Todos"),
                ft.Text("Clientes"),
                ft.Text("Leads"),
                ft.Text("Prospecção"),
            ],
        )
        self.seg_control = segmented
        return segmented

    def barra_categorias(self):
        barra_categorias = ft.Container(
            top=25,
            left=25,
            height=50,
            width=325,
            content=self.segmented()
        )
        return barra_categorias
    
    def layout(self):
    # --- Layout final ---
        layout = ft.Stack(
            controls=[
                self.lista_com_scroll(),
                self.barra_categorias(),
            ],
            expand=True,
        )
        return layout
    
