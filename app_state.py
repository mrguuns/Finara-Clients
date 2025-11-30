from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from overlay_manager import OverlayManager
    from components.navbar import NavBar
    
    from telas.overlays.navbar_button import NavBarButtons
    from telas.overlays.overlay_adicionar_clientes import overlay_adicionar_clientes
    from telas.overlays.overlay_avisos import Avisos
    from telas.clientes import ListaClientes
    from telas.overlays.overlay_editar import overlay_editar
    from telas.overlays.overlay_editar_cliente import OverlayEditarCliente

class AppState:
    overlay = None
    overlay_manager: Optional["OverlayManager"] = None
    navbar: Optional["NavBar"] = None
    navbar_buttons: Optional["NavBarButtons"] = None
    overlay_cliente: Optional["overlay_adicionar_clientes"] = None
    overlay_avisos: Optional["Avisos"] = None
    lista_clientes: Optional["ListaClientes"] = None
    overlay_editar: Optional["overlay_editar"] = None
    overlay_editar_cliente: Optional["OverlayEditarCliente"] = None