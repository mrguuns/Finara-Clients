import flet as ft
from database_controller import DatabaseController
from app_state import AppState


class overlay_editar:
    def __init__(self, page:ft.Page):
        self.db = DatabaseController()
        self.page = page
        self.input_field = ft.TextField(label="Digite o ID...")
    
    def fechar_popup_remover_por_id(self, dialog):
        dialog.open = False
        self.page.update()

    def enviar_popup_remover_por_id(self, dialog):
        try:
            valor = int(self.input_field.value)
            print("Valor digitado:", valor)  # aqui você trata o dado
        
            try:
                debug, resultado = self.db.remover_dados_por_id(valor)
                if debug is True:
                    aviso = f"Removido do banco de dados com sucesso: {resultado}"
                    AppState.overlay_manager.toggle_overlay_avisos(aviso, True)
                    AppState.lista_clientes.on_segmented_change()
                if debug is False:
                    aviso = f"{resultado}"
                    AppState.overlay_manager.toggle_overlay_avisos(aviso, False)
                    AppState.lista_clientes.on_segmented_change()
            except Exception as e:
                aviso = f"Ocorreu um erro inesperado: {e}"
                AppState.overlay_manager.toggle_overlay_avisos(aviso, False)
                AppState.lista_clientes.on_segmented_change()
        
            dialog.open = False
            self.page.update()
        except Exception as e:
            aviso = f"Digite um valor correto: {e}"
            AppState.overlay_manager.toggle_overlay_avisos(aviso, False)
            self.page.update()
    
    def abrir_popup_remover_por_id(self, e):
        dialog = ft.AlertDialog(
            title=ft.Text("Remover por ID"),
            content=self.input_field,
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.fechar_popup_remover_por_id(dialog)),
                ft.TextButton("Enviar", on_click=lambda e: self.enviar_popup_remover_por_id(dialog)),
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        return dialog

    def editar_layout(self):
        btn_remover_por_id = ft.Button(
            icon=ft.Icons.REMOVE,
            width=150,
            text="Remover",
            on_click=lambda e: AppState.overlay_manager.toogle_popup_remover_por_id()
        )      
        btn_editar_por_id = ft.Button(
            icon=ft.Icons.EDIT_DOCUMENT,
            width=150,
            text="Editar",
            on_click=lambda e: AppState.overlay_manager.toogle_popup_editar_por_id()
        )
        btn_fechar_editar = ft.Button(
            icon=ft.Icons.ARROW_BACK,
            width=150,
            text="Voltar",
            on_click=lambda e: AppState.overlay_manager.toggle_pagina_editar_overlay()
        )
        layout = ft.Container(
            width=200,
            height=300,
            top=220,
            left=90,
            alignment=ft.alignment.center,
            bgcolor="#141414",
            border=ft.border.all(width=1,color="#18d1ff"),
            expand=True,
            border_radius=17,
            content=ft.Stack(
                controls=[
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                btn_editar_por_id,
                                btn_remover_por_id,
                                btn_fechar_editar,
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ),
                ],
            ),
        )

        return layout
    
    def fechar_popup_editar_por_id(self, dialog):
        dialog.open = False
        self.page.update()

    def abrir_popup_editar_por_id(self,e):
        dialog = ft.AlertDialog(
            title=ft.Text("Editar por ID"),
            content=self.input_field,
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.fechar_popup_editar_por_id(dialog)),
                ft.TextButton("Enviar", on_click=lambda e: self.enviar_popup_editar_por_id(dialog)),
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        return dialog

    def enviar_popup_editar_por_id(self, dialog):
        try:
            valor = int(self.input_field.value)
            print(valor)
            lista_ids = DatabaseController.listar_ids(self.page)
            print(lista_ids)
            if valor in lista_ids:
                debug, resultado = self.db.buscar_cliente_por_id(valor)
                self.fechar_popup_editar_por_id(dialog)
                AppState.overlay_manager.toggle_pagina_editar_cliente_overlay(resultado)
            else:
                aviso = "ID não encontrado"         
                AppState.overlay_manager.toggle_overlay_avisos(aviso, False)

        except Exception as e:
            aviso = (f"Algo deu errado. {e}")
            AppState.overlay_manager.toggle_overlay_avisos(aviso, False)

  