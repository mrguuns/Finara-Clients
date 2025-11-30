import flet as ft
import asyncio
import time

from callbacks import registrar_rota, ativar_overlay, registrar_menu_overlay, abrir_pagina_clientes
from app_state import AppState


class NavBar:
    def __init__(self, page: ft.Page):
        self.page = page

        # elementos que serão criados no build()
        self.marcadorhome = None
        self.marcadorclientes = None

        self.btn_home = None
        self.btn_person = None
        self.xButton = None

        self.bottom_bar = None

        # registrar callbacks igual no seu código
        registrar_rota(self._atualizar_rota)

    def _atualizar_rota(self, rota):
        if rota == "/":
            self.marcadorhome.visible = True
            self.marcadorclientes.visible = False

        elif rota == "/clientes":
            self.marcadorclientes.visible = True
            self.marcadorhome.visible = False

        self.marcadorhome.update()
        self.marcadorclientes.update()


    def build(self):

        # marcadores
        self.marcadorhome = ft.Container(
            bgcolor="#18d1ff",
            width=70,
            height=2,
            visible=False,
            opacity=1,
            margin=ft.margin.only(left=16, bottom=10)
        )
        
        self.marcadorclientes = ft.Container(
            bgcolor="#18d1ff",
            width=70,
            height=2,
            visible=False,
            opacity=1,
            margin=ft.margin.only(left=16, bottom=10)
        )

        self.btn_home = ft.Column(
            controls=[
                ft.IconButton(icon=ft.Icons.HOME, icon_color="white", icon_size=30,
                              on_click=lambda e: self.page.go("/")),
                ft.Text("Principal", size=12),
            ],
            height=70,
            width=100,
            expand=True,
            spacing=-10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            opacity=1,
        )

        self.btn_person = ft.Column(
            controls=[
                ft.IconButton(icon=ft.Icons.PERSON, icon_color="white", icon_size=30,
                              on_click=lambda e: self.page.go("/clientes")),
                ft.Text("Clientes", size=12),
            ],
            expand=True,
            height=70,
            width=100,
            spacing=-10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            opacity=1,
        )

        self.xButton = ft.Container(
            content=ft.IconButton(
                icon=ft.Icons.ADD,
                icon_size=40,
                on_click=lambda e: AppState.overlay_manager.page.run_task(AppState.overlay_manager.toggle_menu_overlay),
                icon_color="white",
                rotate=0,
                animate_rotation=ft.Animation(duration=4000, curve=ft.AnimationCurve.DECELERATE),
            ),
            width=60,
            height=60,
            bgcolor="#18d1ff",
            border_radius=30,
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(blur_radius=10, color="black"),
            opacity=1,
        )

        self.bottom_bar = ft.Stack(
            alignment=ft.alignment.bottom_center,
            controls=[
                ft.Container(
                    height=70,
                    width=425,
                    bgcolor="#141414",
                    content=ft.Row(
                        controls=[
                            ft.Container(expand=1),
                            ft.Column([self.btn_home, self.marcadorhome]),
                            ft.Container(expand=1),
                            ft.Container(expand=1),
                            ft.Column([self.btn_person, self.marcadorclientes]),
                            ft.Container(expand=1),
                        ],
                    ),
                ),
                ft.Container(
                    content=self.xButton,
                    alignment=ft.alignment.bottom_center,
                    margin=ft.margin.only(bottom=30),
                    height=60,
                    width=60,
                )
            ]
        )

        return self.bottom_bar

