import flet as ft

class Avisos:
    def __init__(self, page: ft.Page):
        self.page = page

    def create_overlay_avisos(self, aviso, tipo):
        if tipo == True:
            overlay_avisos = ft.SnackBar(
                ft.Text(f"{aviso}",size=20, color="BLACK"),
                open=True,
                bgcolor="green",
                duration=800,
            )
            return overlay_avisos
        if tipo == False:
            overlay_avisos = ft.SnackBar(
                ft.Text(f"{aviso}",size=20, color="BLACK"),
                open=True,
                bgcolor="red",
                duration=800,
            )
            return overlay_avisos
            
