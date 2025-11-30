import flet as ft
from datetime import date
from callbacks import ativar_overlay
from overlay_manager import *
from database_controller import DatabaseController
from app_state import AppState

class overlay_com_click:
    def __init__(self, page: ft.Page):
        self.page = page
    def aplicar_overlay(self, ativo):
        self.overlay_click = ft.GestureDetector(
            opacity=1,
            visible=True,
            on_tap=lambda e: AppState.overlay_manager.fechar_por_click(),
            expand=True,
            content=ft.Container(
                expand=True,
                bgcolor="#ff0000",
            ),
        )
        if ativo == True:
            self.overlay_click.visible = True
        
        return self.overlay_click