import flet as ft
from datetime import date
from callbacks import ativar_overlay

from database_controller import DatabaseController
from app_state import AppState

def overlay_adicionar_clientes(page: ft.Page):
    db = DatabaseController()

    def salvar_dp_prospeccao(e):
        valor_formatado = e.control.value.strftime("%d/%m/%Y")

        data_prospeccao_input.value = valor_formatado
        data_prospeccao_input.update()  # chama update sem argumentos
        
        print("Data selecionada:", valor_formatado)
    def salvar_dp_qualificacao(e):
        valor_formatado = e.control.value.strftime("%d/%m/%Y")

        data_qualificacao_input.value = valor_formatado
        data_qualificacao_input.update()  # chama update sem argumentos
        
        print("Data selecionada:", valor_formatado)
    def salvar_dp_conversao(e):
        valor_formatado = e.control.value.strftime("%d/%m/%Y")

        data_conversao_input.value = valor_formatado
        data_conversao_input.update()  # chama update sem argumentos
        
        print("Data selecionada:", valor_formatado)
    def capturar_e_enviar_dados(e):
        dados = {
            "nome": nome_input.value.strip(),
            "telefone": telefone_input.value.strip(),
            "endereco": endereco_input.value.strip(),
            "email": email_input.value.strip(),
            "plano_atual": dropdown_plano_atual.value.strip(),
            "status": dropdown_status.value,
            "categoria": dropdown_categoria.value.strip(),
            "data_prospeccao": data_prospeccao_input.value.strip(),
            "data_qualificacao": data_qualificacao_input.value.strip(),
            "data_conversao": data_conversao_input.value.strip(),
            "idade": idade_input.value.strip(),
            "observacao": observacao_input.value.strip()
        }
        if not dados["nome"] or not dados["telefone"]:
            aviso = "Nome e telefone são necessarios."
            AppState.overlay_manager.toggle_overlay_avisos(aviso, False)
            return
        try:
            resultado = db.inserir_dados_clientes(dados)
            aviso = f"Inserido no Banco de Dados com Sucesso: {resultado}"
            AppState.overlay_manager.toggle_overlay_avisos(aviso, True)
            AppState.lista_clientes.on_segmented_change()
        except Exception as e:
            aviso = f"Ocorreu um erro ao inserir no banco de dados: {e}"
            AppState.overlay_manager.toggle_overlay_avisos(aviso, False)
            return
        nome_input.value = ""
        telefone_input.value = ""
        endereco_input.value = ""
        email_input.value = ""
        dropdown_plano_atual.value = ""
        dropdown_status.value = ""
        dropdown_categoria.value = ""
        data_prospeccao_input.value = ""
        data_qualificacao_input.value = ""
        data_conversao_input.value = ""
        idade_input.value = ""
        observacao_input.value = ""
        page.update()

    titulo_painel = ft.Row(
        controls=[
            ft.Text("Adicionar Cliente", size=18, text_align="center"),
        ],
        offset=ft.Offset(x=0.3, y=0.0),
    )

    nome_input = ft.TextField(
        label="Nome completo:",
        border=ft.InputBorder.UNDERLINE,
        hint_text="--->",
    )
    telefone_input = ft.TextField(
        label="Telefone:",
        border=ft.InputBorder.UNDERLINE,
        hint_text="--->",
    )
    endereco_input = ft.TextField(
        label="Endereço:",
        border=ft.InputBorder.UNDERLINE,
        hint_text="--->",
    )   
    email_input = ft.TextField(
        label="Email:",
        border=ft.InputBorder.UNDERLINE,
        hint_text="--->",
    )
    idade_input = ft.TextField(
        label="Idade:",
        border=ft.InputBorder.UNDERLINE,
        hint_text="--->",
    )
    observacao_input = ft.TextField(
        label="Observação:",
        border=ft.InputBorder.UNDERLINE,
        hint_text="--->",
    )
    dropdown_status = ft.Dropdown(
        label="Status",
        width=170,
        options=[
        ft.dropdown.Option("Ativo"),
        ft.dropdown.Option("Inativo"),
        ft.dropdown.Option("VIP"),
        ft.dropdown.Option("Bloqueado"),
        ft.dropdown.Option("Novo"),
        ft.dropdown.Option("Contatado"),
        ft.dropdown.Option("Qualificado"),
        ft.dropdown.Option("Não Qualificado"),
        ft.dropdown.Option("Em andamento"),
        ft.dropdown.Option("Concluído"),
        ft.dropdown.Option("Perdido"),
        ],
        value="Novo",  # valor padrão
        on_change=lambda e: print("Selecionado:", e.control.value)
    )
    dropdown_categoria = ft.Dropdown(
        label="Categoria",
        width=170   ,
        options=[
            ft.dropdown.Option("Cliente"),
            ft.dropdown.Option("Lead"),
            ft.dropdown.Option("Prospecção"),
        ],
        value="Prospecção",  # valor padrão
        on_change=lambda e: print("Selecionado:", e.control.value)
    )
    dropdown_plano_atual = ft.Dropdown(
        label="plano_atual",
        expand=1,
        width=180,
        options=[
            ft.dropdown.Option("Nenhum"),
        ],
        value="Nenhum",  # valor padrão
        on_change=lambda e: print("Selecionado:", e.control.value)
    )
    data_prospeccao_input = ft.TextField(
        label="Data de prospecção",
        expand=1,
        value=None,
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda e: page.open(
                ft.DatePicker(
                    value=date.today(),
                    on_change=salvar_dp_prospeccao,
                ),
            ),
    )
    data_qualificacao_input = ft.TextField(
        label="Data de qualificação",
        expand=1,
        value=None,
        on_click=lambda e: page.open(
                ft.DatePicker(
                    value=date.today(),
                    on_change=salvar_dp_qualificacao,
                ),
            ),
    )
    data_conversao_input = ft.TextField(
        label="Data de conversão",
        expand=1,
        value=None,
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda e: page.open(
                ft.DatePicker(
                    value=date.today(),
                    on_change=salvar_dp_conversao,
                ),
            ),
    )
    
    botao_cancelar = ft.Button(
        text="Voltar",
        bgcolor="#202020",
        icon_color="#ff0000",
        scale=1.2,
        icon=ft.Icons.ARROW_BACK,
        on_click=lambda e: AppState.overlay_manager.toggle_pagina_clientes_overlay()
    )
    botao_Salvar = ft.Button(
        text="Salvar",
        bgcolor="#202020",
        icon_color="green",
        scale=1.2,
        icon=ft.Icons.SAVE,
        on_click=lambda e: capturar_e_enviar_dados(e),
    )
    overlay_container = ft.Stack(
        controls=[
            ft.Container(
                expand=True,
                bgcolor="#141414",
                width=375,
                padding=10,
                border=ft.border.all(width=1, color="#18d1ff"),
                border_radius=30,
                content=ft.Stack(
                    controls=[
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    titulo_painel,
                                    nome_input,
                                    telefone_input,
                                    endereco_input,
                                    email_input,
                                    idade_input,
                                    observacao_input,
                                    ft.Row(
                                        controls=[dropdown_status, dropdown_categoria],
                                    ),

                                    ft.Row(
                                        controls=[data_prospeccao_input, data_qualificacao_input],
                                    ),

                                    ft.Row(
                                        controls=[data_conversao_input, dropdown_plano_atual],
                                    ),

                                    ft.Row([botao_cancelar,botao_Salvar], alignment="center", spacing=30,),
                                ],
                                scroll=ft.ScrollMode.AUTO,
                            ),
                        ),
                    ],
                ),
                margin=ft.margin.only(top=30,),
            ),
        ],
    )

    overlay_container._nome = "pagina_adicionar_clientes"
    return overlay_container