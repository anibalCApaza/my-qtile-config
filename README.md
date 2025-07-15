# Configuración de Qtile

![WhatsApp Image 2025-06-19 at 8 28 38 AM](https://github.com/user-attachments/assets/c68b2991-0c65-45cb-867c-07372b4cabdd)

Este repositorio contiene **mi configuración personalizada del gestor de ventanas Qtile**.
Qtile es un tiling window manager (TWM) dinámico, potente y completamente configurable en Python puro.

## 🧠 ¿Por qué Qtile?

Elegí Qtile porque:

- Está completamente escrito y configurado en **Python**, lo cual me da control total en la personalización visual y de atajos de teclado.
- Es **ligero**, ideal para equipos modestos o personas que buscan eficiencia y un twm que no consuma muchos recursos.
- Tiene un sistema de **layouts dinámicos** que se adaptan muy bien a mi flujo de trabajo.
- Es **extensible**, puedo agregar funciones o widgets fácilmente sin depender de scripts externos.

## 🧩 Qué contiene este repo

- `config.py`: archivo principal de configuración, donde se definen las teclas, grupos, layouts, widgets y más.
- `scripts/`: utilidades extra como cambiar de wallpaper, manejar audio, etc.
- `autostart.sh`: script que se ejecuta al iniciar Qtile (para lanzar Picom, configurar teclado, etc.).

## 🎮 Atajos de teclado destacados

Algunos de los atajos clave que uso:

| Tecla                            | Acción                               |
| -------------------------------- | ------------------------------------ |
| `mod + Enter`                    | Abrir terminal                       |
| `mod + c`                        | Cerrar ventana                       |
| `mod + [1-9]`                    | Cambiar de workspace                 |
| `mod + Shift + q`                | Abrir el menú de apagado del sistema |
| `mod + r`                        | Llamar al lanzador de aplicaciones   |
| `mod + up o down o left o right` | Navegar entre ventandas              |

## 🧩 Programas y herramientas adicionales

Esta configuración de Qtile hace uso de algunos programas o herramientas externas para mejorar la experiencia de uso:

| Herramienta       | Propósito                   | Cómo se usa                                           |
| ----------------- | --------------------------- | ----------------------------------------------------- |
| **bash**          | Shell para ejecutar scripts | Para ejecutar scripts como Rofi y el autostart.       |
| **pamixer**       | Control del volumen         | Para subir, bajar o mutear el audio.                  |
| **brightnessctl** | Control del brillo          | Para subir o bajar el brillo en laptops.              |
| **kitty**         | Terminal                    | Terminal invocada con los atajos de teclado de qtile. |
| **rofi**          | Launcher y menú de apagado  | Lanzador de aplicaciones.                             |
