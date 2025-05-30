from SimpleWebUI import ui
from SimpleWebUI.RunAfter import RunAfter
run = RunAfter()

with ui.column().classes('bs-4'):
    ui.link("Limour's Blog", target='https://hexo.limour.top/')
    ui.label('Hello, world!', id='itest')
    ui.pinput('test', id='iinput')
    with ui.row():
        ui.button('Click me!').classes('bs-6')

run(0, ui.run_app)
# ui.itest.v = 'limour'
# run(0, ui.commit)
# print(ui.iinput.v)
