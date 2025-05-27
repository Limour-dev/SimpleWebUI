from SimpleWebUI import ui

with ui.column():
    ui.label('Hello, world!')
    with ui.row():
        ui.button('Click me!').classes('bs-1')

ui.run()
