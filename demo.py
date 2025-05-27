from SimpleWebUI import ui

with ui.column().classes('bs-12'):
    ui.label('纵向1')
    with ui.row():
        ui.label('横向1.1').classes('bs-1')
        ui.label('横向1.2').classes('bs-2')
        with ui.column().classes('bs-4'):
            ui.label('纵向1.2.1')
            ui.label('纵向1.2.2')
        ui.label('横向1.3').classes('bs-3')
    ui.label('纵向2')
    with ui.row():
        ui.label('横向2.1')
        ui.label('横向2.2')
    ui.label('纵向3')

ui.run()
