from SimpleWebUI import ui
from SimpleWebUI.RunAfter import RunAfter
run = RunAfter()

with ui.column().classes('bs-4'):
    ui.link("Limour's Blog", target='https://hexo.limour.top/')
    ui.label('Hello, world!', id='itest')
    ui.pinput('test', id='iinput')
    with ui.row():
        ui.button('Click me!', id='btn').classes('bs-6')

async def click(_ui, el):
    _ui.iinput.v = 'hello ' + _ui.iinput.v
    _ui.itest.v = 'button clicked'
ui.btn.click = click

run(0, ui.run_app)
