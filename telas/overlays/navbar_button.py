import flet as ft
import asyncio
from app_state import AppState

class NavBarButtons:
    def __init__(self, page: ft.Page):

        self.page = page
        
        self.btn_fomulary = self.create_btn_formulary()
        
        self.btn_edit =  self.create_btn_edit()
        
        self.btn_create =  self.create_btn_create()

        self.buttons_overlay = self.create_bnt_overlay()

    def create_btn_formulary(self):
        return ft.Container(
            content=ft.IconButton(
                icon=ft.Icons.INSIGHTS,
                icon_color="white",
                icon_size=25,
            ),
            bottom=-100,
            right=180,
            animate_position=ft.Animation(duration=100, curve=ft.AnimationCurve.DECELERATE),
            width=60,
            height=60,
            bgcolor="#292828",
            border_radius=50,
        )
        
    def create_btn_edit(self):
        return ft.Container(
            content=ft.IconButton(
                icon=ft.Icons.EDIT_NOTE,
                icon_color="white",
                icon_size=25,
                on_click=lambda e: AppState.overlay_manager.toggle_pagina_editar_overlay()
            ),
            bottom=-100,
            left=180,
            animate_position=ft.Animation(duration=100, curve=ft.AnimationCurve.DECELERATE),
            width=60,
            height=60,
            bgcolor="#292828",
            border_radius=50,
        )

    def create_btn_create(self):
        return ft.Container(
            content=ft.IconButton(
                icon=ft.Icons.PERSON_ADD,
                icon_color="white",
                icon_size=25,
                on_click=lambda e: AppState.overlay_manager.toggle_pagina_clientes_overlay(),
            ),
            bottom=-100,
            animate_position=ft.Animation(duration=100, curve=ft.AnimationCurve.DECELERATE),
            width=60,
            height=60,
            bgcolor="#292828",
            border_radius=50,
        )

    async def abrir_animacao(self, e=None):

        self.btn_create.bottom = 125


        self.btn_edit.bottom = 100
        self.btn_edit.left = 80


        self.btn_fomulary.bottom = 100
        self.btn_fomulary.right = 80

        await asyncio.sleep(0.03)
        self.page.update()
    async def fechar_animacao(self, e=None):

        self.btn_edit.bottom = -100
        self.btn_edit.left = 180

        self.btn_fomulary.bottom = -100
        self.btn_fomulary.right = 180

        self.btn_create.bottom = -100


        self.page.update()
        await asyncio.sleep(0.03)

    def create_bnt_overlay(self):
        overlay = ft.Stack(
            controls=[
                self.btn_create,
                self.btn_edit,
                self.btn_fomulary,
            ],
            alignment=ft.alignment.bottom_center,
        )
        overlay._nome = "menu_overlay"
        return overlay
    

