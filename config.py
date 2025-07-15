import subprocess, os

from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from colors import colors


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/scripts/autostart.sh"])


mod = "mod4"
terminal = guess_terminal()

keys = [
    # Una lista de comandos disponibles que pueden ser asignados a teclas se encuentra en
    # https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Cambiar entre ventanas
    Key([mod], "left", lazy.layout.left(), desc="Mover el enfoque a la izquierda"),
    Key([mod], "right", lazy.layout.right(), desc="Mover el enfoque a la derecha"),
    Key([mod], "down", lazy.layout.down(), desc="Mover el enfoque hacia abajo"),
    Key([mod], "up", lazy.layout.up(), desc="Mover el enfoque hacia arriba"),
    Key(
        [mod],
        "space",
        lazy.layout.next(),
        desc="Mover el enfoque de la ventana al siguiente",
    ),
    # Mover ventanas entre columnas izquierda/derecha o mover hacia arriba/abajo en el stack actual.
    # Mover fuera de rango en el layout de Columnas creará una nueva columna.
    Key(
        [mod, "shift"],
        "left",
        lazy.layout.shuffle_left(),
        desc="Mover la ventana hacia la izquierda",
    ),
    Key(
        [mod, "shift"],
        "right",
        lazy.layout.shuffle_right(),
        desc="Mover la ventana hacia la derecha",
    ),
    Key(
        [mod, "shift"],
        "down",
        lazy.layout.shuffle_down(),
        desc="Mover la ventana hacia abajo",
    ),
    Key(
        [mod, "shift"],
        "up",
        lazy.layout.shuffle_up(),
        desc="Mover la ventana hacia arriba",
    ),
    # Agrandar ventanas. Si la ventana actual está en el borde de la pantalla y la dirección
    # va hacia el borde de la pantalla, la ventana se reducirá.
    Key(
        [mod, "control"],
        "left",
        lazy.layout.grow_left(),
        desc="Agrandar ventana hacia la izquierda",
    ),
    Key(
        [mod, "control"],
        "right",
        lazy.layout.grow_right(),
        desc="Agrandar ventana hacia la derecha",
    ),
    Key(
        [mod, "control"],
        "down",
        lazy.layout.grow_down(),
        desc="Agrandar ventana hacia abajo",
    ),
    Key(
        [mod, "control"],
        "up",
        lazy.layout.grow_up(),
        desc="Agrandar ventana hacia arriba",
    ),
    Key(
        [mod],
        "n",
        lazy.layout.normalize(),
        desc="Restablecer todos los tamaños de ventana",
    ),
    # Alternar entre lados divididos y no divididos del stack.
    # Dividido = todas las ventanas mostradas
    # No dividido = 1 ventana mostrada, como en el layout de Max, pero aún con
    # varios paneles en el stack.
    Key([mod], "q", lazy.spawn("kitty"), desc="Abre el terminal"),
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Alternar entre lados divididos y no divididos del stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Lanzar terminal"),
    # Alternar entre diferentes layouts como se define a continuación
    Key([mod], "Tab", lazy.next_layout(), desc="Alternar entre layouts"),
    Key([mod], "c", lazy.window.kill(), desc="Cerrar ventana enfocada"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Alternar fullscreen en la ventana enfocada",
    ),
    Key(
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Alternar flotante en la ventana enfocada",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Recargar la configuración"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Apagar Qtile"),
    # Comando para abrir rofi
    Key(
        [mod],
        "r",
        lazy.spawn("bash /home/arca/.config/rofi/launchers/type-6/launcher.sh"),
        desc="Ejecutar rofi",
    ),
    # Comando para abrir el powermenu
    # home/arca/.config/rofi/powermenu/type-6/powermenu.sh
    Key(
        [mod, "shift"],
        "q",
        lazy.spawn("bash /home/arca/.config/rofi/powermenu/type-6/powermenu.sh"),
        desc="Ejecutar powermenu",
    ),
    # Gestión de Volumen
    # Subir volumen
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("bash -c 'pamixer -i 10 --allow-boost; pamixer --set-limit 120'"),
    ),  # Ajusta si F12 no corresponde al keycode 123
    # Bajar volumen
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("bash -c 'pamixer -d 10 --allow-boost; pamixer --set-limit 120'"),
    ),
    # Mutear volumen
    Key([], "XF86AudioMute", lazy.spawn("pamixer --toggle-mute")),
    # Gestión de Brillo
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set 15%+")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 15%-")),
]

# Añadir bindings de teclas para cambiar VT en Wayland.
# No podemos verificar qtile.core.name en la configuración predeterminada ya que se carga antes de que Qtile se inicie
# Por lo tanto, retrasamos la verificación hasta que se ejecute el binding de teclas usando .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Cambiar a VT{vt}",
        )
    )


groups = [Group(i) for i in ["", "", "", "", "", "", "", "", ""]]
group_hotkeys = "123456789"
for g, k in zip(groups, group_hotkeys):
    keys.extend(
        [
            # mod + número de grupo = cambiar al grupo
            Key(
                [mod],
                k,
                lazy.group[g.name].toscreen(),
                desc=f"Cambiar al grupo {g.name}",
            ),
            # mod + shift + número de grupo = cambiar a & mover ventana enfocada al grupo
            Key(
                [mod, "shift"],
                k,
                lazy.window.togroup(g.name, switch_group=True),
                desc=f"Cambiar a & mover ventana enfocada al grupo {g.name}",
            ),
            # O, usa lo siguiente si prefieres no cambiar al grupo.
            # # mod + shift + número de grupo = mover ventana enfocada al grupo
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="mover ventana enfocada al grupo {}".format(i.name)),
        ]
    )

layout_theme = {
    "border_width": 3,
    "margin": 14,
    "border_focus": colors["Maroon"],
    "border_normal": colors["Mantle"],
}

layouts = [
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4, **layout_theme),
    # layout.Max(**layout_theme),
    # Intenta más layouts descomentando los siguientes layouts.
    # layout.Stack(num_stacks=2, **layout_theme),
    layout.Bsp(**layout_theme, fair=False),
    # layout.Matrix(**layout_theme),
    # layout.MonadTall(**layout_theme),
    # layout.MonadWide(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.Tile(**layout_theme),
    # layout.TreeTab(**layout_theme),
    # layout.VerticalTile(**layout_theme),
    # layout.Zoomy(**layout_theme),
    # layout.Spiral(**layout_theme),
]

widget_defaults = dict(
    font="MonaspaceNeon",
    fontsize=15,
    padding=10,
    foreground=colors["Base"],
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    active=colors["Maroon"],
                    # block_highlight_text_color= colors["Mauve"],
                    inactive=colors["Text"],
                    highlight_method="block",
                    # background="#eed49f",
                    this_current_screen_border=colors["Surface 2"],
                    this_screen_border=colors["Yellow"],
                    padding_x=10,
                    padding_y=6,
                    rounded=True,
                    background=colors["Crust"],
                    fontsize=19,
                ),
                widget.TextBox(
                    background=colors["Crust"],
                    text="",
                    padding=-1,
                    fontsize=27,
                    foreground=colors["Overlay 1"],
                ),
                widget.WindowName(
                    background=colors["Overlay 1"], foreground=colors["Crust"]
                ),
                widget.TextBox(
                    background=colors["Overlay 1"],
                    text="",
                    padding=-1,
                    fontsize=27,
                    foreground=colors["Green"],
                ),
                widget.Backlight(
                    backlight_name="amdgpu_bl1",
                    format="󰃠 {percent:2.0%}",
                    background=colors["Green"],
                ),
                widget.TextBox(
                    background=colors["Green"],
                    text="",
                    padding=-1,
                    fontsize=27,
                    foreground=colors["Mauve"],
                ),
                widget.Volume(background=colors["Mauve"], fmt=" {}"),
                widget.TextBox(
                    background=colors["Mauve"],
                    text="",
                    padding=-1,
                    fontsize=27,
                    foreground=colors["Lavender"],
                ),
                widget.Systray(
                    background=colors["Lavender"],
                ),
                widget.TextBox(
                    background=colors["Lavender"],
                    text="",
                    padding=-1,
                    fontsize=27,
                    foreground=colors["Pink"],
                ),
                widget.Clock(format="%d/%m/%Y %a %I:%M %p", background=colors["Pink"]),
                widget.TextBox(
                    background=colors["Pink"],
                    text="",
                    padding=-1,
                    fontsize=27,
                    foreground=colors["Peach"],
                ),
                widget.Battery(
                    format="{percent:2.0%} {char} ",
                    background=colors["Peach"],
                    charge_char="󰂆",
                    discharge_char="󰂁",
                    empty_char="󰁺",
                    full_char="󰂅 Full",
                    show_short_text=False,
                ),
                widget.TextBox(
                    background=colors["Peach"],
                    text="",
                    padding=-1,
                    fontsize=27,
                    foreground=colors["Red"],
                ),
                widget.TextBox(
                    background=colors["Red"],
                    text="⏻ ",
                    mouse_callbacks={
                        "Button1": lambda: qtile.cmd_spawn(
                            "/home/arca/.config/rofi/powermenu/type-6/powermenu.sh"
                        )
                    },
                ),
            ],
            34,
            background=colors["Mauve"],
            border_width=[0, 0, 4, 0],  # borde solo en la parte inferior
            border_color=["000000", "000000", colors["Yellow"], "000000"],
            # border_width=[2, 0, 2, 0],  # Dibujar bordes superior e inferior
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Bordes de color magenta
        ),
        # Puedes descomentar esta variable si ves que en X11 el redimensionamiento/movimiento de ventanas flotantes es lento
        # Por defecto manejamos estos eventos con retraso para mejorar el rendimiento, pero tu sistema podría seguir teniendo problemas
        # Esta variable está configurada en None (sin límite) por defecto, pero puedes configurarla a 60 para limitarlo a 60 eventos por segundo
        # x11_drag_polling_rate = 60,
    ),
]

# Arrastrar layouts flotantes.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # tipo: lista
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Usa la utilidad de `xprop` para ver el wm_class y el nombre de un cliente X.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # Entrada de contraseña de clave GPG
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# Si cosas como juegos de steam quieren minimizarse automáticamente cuando pierden
# enfoque, ¿debemos respetarlo o no?
auto_minimize = True

# Cuando uses el backend Wayland, esto se puede usar para configurar dispositivos de entrada.
wl_input_rules = None

# Tema de xcursor (cadena o None) y tamaño (entero) para el backend Wayland
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: ¡Vaya! Aquí estamos mintiendo. En realidad, nadie usa o le importa esta
# cadena, excepto los kits de distribución. Se va a cambiar en el futuro.
wmname = "LG3D"
