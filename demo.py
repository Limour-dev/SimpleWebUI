from SimpleWebUI import ui
from SimpleWebUI.RunAfter import RunAfter
run = RunAfter()

with ui.column():
    ui.link("Limour's Blog", target='https://hexo.limour.top/')
    ui.label('Hello, world!')
    ui.pinput('test')
    with ui.row():
        ui.button('Click me!').classes('bs-1')

run(0, ui.run_app)
