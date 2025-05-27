from SimpleWebUI import ui
from SimpleWebUI.RunAfter import RunAfter
run = RunAfter()

with ui.column():
    ui.label('Hello, world!')
    with ui.row():
        ui.button('Click me!').classes('bs-1')

run(0, ui.run_app)
