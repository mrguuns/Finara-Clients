import flet as ft
import os

# ATUALIZAR ROTA
_callback_rotas = None
def registrar_rota(callback):
    global _callback_rotas
    _callback_rotas = callback
def atualizar_rota(rota):
    global _callback_rotas
    if _callback_rotas:
        _callback_rotas(rota)

# ATIVAR OVERLAY
_callback_overlay = None
def registrar_callback_overlay(func):
    global _callback_overlay
    _callback_overlay = func
def ativar_overlay(valor):
    if _callback_overlay:
        _callback_overlay(valor)

# FECHAR MENU OVERLAY
_callback_button = None
def registrar_menu_overlay(callback):
    global _callback_button
    _callback_button = callback
def fechar_menu_animacao():
    global _callback_button
    if _callback_button:
        _callback_button()

_callback_pagina_clientes = None
def registrar_pagina_clientes(callback):
    global _callback_pagina_clientes
    _callback_pagina_clientes = callback
def abrir_pagina_clientes():
    if _callback_pagina_clientes:
        _callback_pagina_clientes()

