import flet as ft
import asyncio
import time

from callbacks import fechar_menu_animacao, ativar_overlay
from telas.overlays.overlay_com_click import overlay_com_click
from telas.overlays.overlay_adicionar_clientes import overlay_adicionar_clientes
from app_state import AppState

class OverlayManager:
    def __init__(self, page):
        self.page = page
        self.overlay_atual = []
        self.overlay_clientes = None
        self.overlay_avisos = None
        self.overlay_editar = None
        self.overlay_editar_cliente = None

    async def toggle_menu_overlay(self):
        navbar = AppState.navbar_buttons          # classe que tem abrir_animacao()
        overlay = AppState.navbar_buttons.buttons_overlay

        # overlay ainda não está ativo → abrir
        if overlay not in self.page.overlay:
            print("abrrndo")
            AppState.navbar.xButton.rotate = 0.8
            self.page.overlay.append(overlay)
            self.page.update()

            # chama animação para abrir
            await navbar.abrir_animacao()

        # overlay já está ativo → fechar
        else:
            # animação reversa ANTES de remover
            print("fechando")
            AppState.navbar.xButton.rotate = 0
            await navbar.fechar_animacao()

            self.page.overlay.remove(overlay)
            self.page.update()

    def toggle_pagina_clientes_overlay(self):
        # cria uma vez só
        if self.overlay_clientes is None:
            self.overlay_clientes = overlay_adicionar_clientes(self.page)

            overlay = self.overlay_clientes

            if overlay not in self.overlay_atual:
                print("abrindo clientes")
                self.page.run_task(self.toggle_menu_overlay)
                self.overlay_atual.append(overlay)
                self.page.overlay.append(overlay)
                self.page.update()
        else:
            print("fechando clientes")
            self.overlay_atual.remove(self.overlay_clientes)
            self.page.overlay.remove(self.overlay_clientes)
            self.overlay_clientes = None
            self.page.update()

    def toggle_overlay_avisos(self, aviso, tipo: bool):
        # cria uma vez só

        self.overlay_avisos = AppState.overlay_avisos.create_overlay_avisos(aviso, tipo)

        overlay = self.overlay_avisos

        if overlay not in self.overlay_atual:
            self.overlay_atual.append(overlay)
            self.page.overlay.append(overlay)
            self.page.update()
            time.sleep(1)
            self.overlay_atual.remove(overlay)
            self.page.overlay.remove(overlay)
            self.page.update()

    def toggle_pagina_editar_overlay(self):
        # cria uma vez só
        if self.overlay_editar is None:
            self.overlay_editar = AppState.overlay_editar.editar_layout()

        overlay = self.overlay_editar

        if overlay not in self.overlay_atual:
            print("abrindo Editar")
            self.overlay_atual.append(overlay)
            self.page.overlay.append(overlay)
            overlay_com_click.aplicar_overlay(self.page,True)
            self.page.update()
        else:
            print("fechando Editar")
            self.overlay_atual.remove(overlay)
            self.page.overlay.remove(overlay)
            self.page.update()
        
    def toogle_popup_remover_por_id(self):
        overlay = AppState.overlay_editar.abrir_popup_remover_por_id(self.page)
        self.page.overlay.append(overlay)
        self.page.update()
        
    def toogle_popup_editar_por_id(self):
        overlay = AppState.overlay_editar.abrir_popup_editar_por_id(self.page)
        self.page.overlay.append(overlay)
        self.page.update()

    def toggle_pagina_editar_cliente_overlay(self, dados):
        if self.overlay_editar_cliente is None:
                # Atualiza os dados do model
                AppState.overlay_editar_cliente.carregar_dados(dados)

                # Constrói um novo overlay com os dados atualizados
                self.overlay_editar_cliente = AppState.overlay_editar_cliente.build()

                print("abrindo Editar")
                self.overlay_atual.append(self.overlay_editar_cliente)
                self.page.overlay.append(self.overlay_editar_cliente)
                self.page.update()
                return

            # Se já existe → fechar
        print("fechando Editar")
        if self.overlay_editar_cliente in self.page.overlay:
            self.page.overlay.remove(self.overlay_editar_cliente)

        if self.overlay_editar_cliente in self.overlay_atual:
            self.overlay_atual.remove(self.overlay_editar_cliente)

        # limpar ponteiro
        self.overlay_editar_cliente = None
        self.page.update()