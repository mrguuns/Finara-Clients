import flet as ft

def PaginaInicial(page: ft.Page):
    page.title = "Finara Clients"


    banner_topo = ft.Container(
        bgcolor="#141414",
        width=300,
        height=100,
        alignment=ft.alignment.center,
        # border=ft.border.all(color="red"),
        border_radius=ft.border_radius.only(bottom_left=25,bottom_right=25),
        border=ft.border.Border(
            bottom=ft.BorderSide(1, color="#18d1ff")
        ),
        # shadow=ft.BoxShadow(blur_radius=3, color="#18d1ff"),
        content=ft.Stack(
            controls=[
                ft.Column(
                    controls=[
                        ft.Row(controls=[ft.Text("Finara", size=25,offset=ft.Offset(x=0, y=0.5))],alignment=ft.MainAxisAlignment.CENTER,),
                        ft.Row(controls=[ft.Text("Clients", size=15,offset=ft.Offset(x=0, y=0.5))],alignment=ft.MainAxisAlignment.CENTER),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=0,
                ),
            ],
        ),
    )
    banner = ft.Container(
        bgcolor="#131111",
        width=page.width*1,
        height=page.height*0.8,
        alignment=ft.alignment.center,
        margin=ft.margin.symmetric(horizontal=10),
        border_radius=16,
        border=ft.border.all(color="#18d1ff"),
        # shadow=ft.BoxShadow(blur_radius=3, color="#18d1ff")
    )
    layout = ft.Container(
        # border=ft.border.all(color="red"),
        expand=True,
        alignment=ft.alignment.center,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_right,
            end=ft.alignment.bottom_left,
            colors=["#0F0F0F","#181818"]
        ),
        content=ft.Stack(
            expand=True,
            controls=[
                ft.Column(
                    expand=True,
                    controls=[
                        ft.Container(
                            content=banner,
                            alignment=ft.alignment.center,
                            # border=ft.border.all(color="red"),
                            height=banner.height,
                            width=banner.width,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                banner_topo,
            ],
            alignment=ft.alignment.top_center,
        ),
    )
    

    return layout