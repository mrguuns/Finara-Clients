import flet as ft
import os
from telas.pagina_inicial import PaginaInicial
from telas.clientes import ListaClientes
from telas.overlays.overlay_adicionar_clientes import overlay_adicionar_clientes
from telas.overlays.overlay_com_click import overlay_com_click
from telas.overlays.navbar_button import NavBarButtons
from telas.overlays.overlay_avisos import Avisos
from telas.overlays.overlay_editar import overlay_editar
from telas.overlays.overlay_editar_cliente import OverlayEditarCliente

from database_controller import DatabaseController
from components.navbar import NavBar
from app_state import AppState
from overlay_manager import OverlayManager

from callbacks import atualizar_rota, registrar_callback_overlay


def main(page: ft.Page):
    AppState.page = page
    AppState.overlay_manager = OverlayManager(page)
    AppState.navbar = NavBar(page)
    AppState.navbar_buttons = NavBarButtons(page)
    AppState.overlay_cliente = overlay_adicionar_clientes(page)
    AppState.overlay_avisos = Avisos(page)
    AppState.lista_clientes = ListaClientes(page)
    AppState.overlay_editar = overlay_editar(page)
    AppState.overlay_editar_cliente = OverlayEditarCliente(page, None)
    navbar = AppState.navbar.build()

    page.title = "Finara Clients"
    page.window.width=400
    page.window.max_width=392
    page.window.height=850
    page.window.max_height=850
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "none"
    page.window_soft_input_mode = "adjustNothing"
    import os


    overlay_click = overlay_com_click.aplicar_overlay(page, True)

    conteudo_container = ft.Container(
        opacity=1,
        expand=True,
        margin=0,
        padding=0,
        height=810,
        content=PaginaInicial(page),  # conteúdo inicial
        alignment=ft.alignment.center,
    )
    
    container_stack = ft.Stack(
        controls=[ 
            conteudo_container,
            overlay_click,  
            ft.Container(
                content=navbar,
                alignment=ft.alignment.center,
                height=90,
            ),
        ],
        alignment=ft.alignment.bottom_center,
        opacity=1,
    )
    
    page.add(container_stack)

    def mudar_rota(route):
        if page.route == "/":
            conteudo_container.content = PaginaInicial(page)
            atualizar_rota("/")

        elif page.route == "/clientes":
            conteudo_container.content = AppState.lista_clientes.layout()
            page.update()
            AppState.lista_clientes.on_segmented_change()
            atualizar_rota("/clientes")

        page.update()

    page.on_route_change = mudar_rota

    page.go("/")
    # AppState.overlay_manager.toggle_pagina_clientes_overlay() # Temporario
    # AppState.overlay_manager.toggle_pagina_editar_overlay()
    # dados_cliente = {
    # "id": 1,
    # "nome": "João da Silva",
    # "telefone": "(11) 99999-9999",
    # "endereco": "Rua Exemplo, 123 - Centro",
    # "email": "joao@example.com",
    # "plano_atual": "Plano Ouro",
    # "status": "Ativo",
    # "categoria": "Cliente",
    # "data_prospeccao": "2025-01-10",
    # "data_qualificacao": "2025-01-12",
    # "data_conversao": "2025-01-20",
    # "idade": 32,
    # "observacao": "Cliente retornou ligação e confirmou interesse."
    # }
    # AppState.overlay_manager.toggle_pagina_editar_cliente_overlay(dados_cliente)

if __name__ == "__main__":
    print("Aplicativo inicializado com sucesso.")
    ft.app(target=main)