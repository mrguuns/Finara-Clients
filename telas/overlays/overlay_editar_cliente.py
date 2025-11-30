import flet as ft
import time
from app_state import AppState
from datetime import date
from database_controller import DatabaseController

class OverlayEditarCliente(ft.Container):
    def __init__(self, page, dados_cliente=None):
        super().__init__()
        self.page = page
        self.d = dados_cliente or {}

    def get(self, key):
        return "" if self.d is None else self.d.get(key, "")

    def abrir_dp(self, callback):
        self.page.open(
            ft.DatePicker(
                value=date.today(),
                on_change=callback
            )
        )

    def salvar_dp_prospeccao(self, e):
        self.data_prospeccao_input.value = e.control.value.strftime("%d/%m/%Y")
        self.data_prospeccao_input.update()

    def salvar_dp_qualificacao(self, e):
        self.data_qualificacao_input.value = e.control.value.strftime("%d/%m/%Y")
        self.data_qualificacao_input.update()

    def salvar_dp_conversao(self, e):
        self.data_conversao_input.value = e.control.value.strftime("%d/%m/%Y")
        self.data_conversao_input.update()

    def capturar_e_salvar(self, e):
        dados = {
            "nome": self.nome_input.value,
            "telefone": self.telefone_input.value,
            "endereco": self.endereco_input.value,
            "email": self.email_input.value,
            "plano_atual": self.dropdown_plano_atual.value,
            "status": self.dropdown_status.value,
            "categoria": self.dropdown_categoria.value,
            "data_prospeccao": self.data_prospeccao_input.value,
            "data_qualificacao": self.data_qualificacao_input.value,
            "data_conversao": self.data_conversao_input.value,
            "idade": self.idade_input.value,
            "observacao": self.observacao_input.value
        }

        from database.database import atualizar_cliente
        debug = atualizar_cliente(self.get("id"), dados)
        AppState.overlay_manager.toggle_overlay_avisos(debug, True)
        AppState.lista_clientes.on_segmented_change()
        self.page.update()

    def build(self):

        self.nome_input = ft.TextField(
            label="Nome completo:",
            border=ft.InputBorder.UNDERLINE,
            value=self.get("nome"),
        )

        self.telefone_input = ft.TextField(
            label="Telefone:",
            border=ft.InputBorder.UNDERLINE,
            value=self.get("telefone"),
        )

        self.endereco_input = ft.TextField(
            label="Endereço:",
            border=ft.InputBorder.UNDERLINE,
            value=self.get("endereco"),
        )

        self.email_input = ft.TextField(
            label="Email:",
            border=ft.InputBorder.UNDERLINE,
            value=self.get("email"),
        )

        self.idade_input = ft.TextField(
            label="Idade:",
            border=ft.InputBorder.UNDERLINE,
            value=str(self.get("idade")),
        )

        self.observacao_input = ft.TextField(
            label="Observação:",
            border=ft.InputBorder.UNDERLINE,
            value=self.get("observacao"),
        )
        
        self.dropdown_status = ft.Dropdown(
            expand=True,
            label="Status",
            width=170,
            options=[ft.dropdown.Option(x) for x in [
                "Ativo", "Inativo", "VIP", "Bloqueado", "Novo", "Contatado",
                "Qualificado", "Não Qualificado", "Em andamento",
                "Concluído", "Perdido"
            ]],
            value=self.get("status")
        )

        self.dropdown_categoria = ft.Dropdown(
            expand=True,
            label="Categoria",
            width=180,
            options=[
                ft.dropdown.Option("Cliente"),
                ft.dropdown.Option("Lead"),
                ft.dropdown.Option("Prospecção"),
            ],
            value=self.get("categoria")
        )

        self.dropdown_plano_atual = ft.Dropdown(
            expand=1,
            label="Plano Atual",
            width=180,
            options=[ft.dropdown.Option("NULL")],
            value=self.get("plano_atual")
        )

        self.data_prospeccao_input = ft.TextField(
            label="Data de prospecção",
            expand=1,
            value=self.get("data_prospeccao"),
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: self.abrir_dp(self.salvar_dp_prospeccao)
        )

        self.data_qualificacao_input = ft.TextField(
            expand=1,
            label="Data de qualificação",
            value=self.get("data_qualificacao"),
            on_click=lambda e: self.abrir_dp(self.salvar_dp_qualificacao)
        )

        self.data_conversao_input = ft.TextField(
            expand=1,
            label="Data de conversão",
            value=self.get("data_conversao"),
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: self.abrir_dp(self.salvar_dp_conversao)
        )

        botao_cancelar = ft.Button(
            text="Voltar",
            bgcolor="#202020",
            icon_color="#ff0000",
            scale=1.2,
            icon=ft.Icons.ARROW_BACK,
            on_click=lambda e: AppState.overlay_manager.toggle_pagina_editar_cliente_overlay(dados=None)
        )

        botao_salvar = ft.Button(
            text="Salvar",
            bgcolor="#202020",
            icon_color="green",
            scale=1.2,
            icon=ft.Icons.SAVE,
            on_click=self.capturar_e_salvar
        )

        titulo = (
            f"Editar Cliente | ID: {self.get('id')}"
            if self.get("id") else
            "Editar Cliente"
        )

        return ft.Stack(
            controls=[
                ft.Container(
                    expand=True,
                    width=375,
                    bgcolor="#141414",
                    padding=10,
                    border=ft.border.all(width=1, color="#18d1ff"),
                    border_radius=30,
                    content=ft.Stack(
                        controls=[
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(titulo, size=18, offset=ft.Offset(x=0.53, y=0.0),),
                                        self.nome_input,
                                        self.telefone_input,
                                        self.endereco_input,
                                        self.email_input,
                                        self.idade_input,
                                        self.observacao_input,
                                        ft.Row([self.dropdown_status, self.dropdown_categoria]),
                                        ft.Row([self.data_prospeccao_input, self.data_qualificacao_input]),
                                        ft.Row([self.data_conversao_input, self.dropdown_plano_atual]),
                                        ft.Row([botao_cancelar, botao_salvar], alignment="center",spacing=30,),
                                    ],
                                    scroll=ft.ScrollMode.AUTO,
                                ),
                            ),
                        ],
                    ),
                    # top=30
                    margin=ft.margin.only(top=30,),
                ),
            ],
        )
    
    def carregar_dados(self, dados):
        self.d = dados

        # Recria o layout com valores novos
        novo_conteudo = self.build()
        self.controls = novo_conteudo.controls
        self.page.update()