import PySimpleGUI as sg

sg.theme('DarkBlue')

layout = [
    [sg.Checkbox('All checked',   enable_events=True, key='Check_All'),
     sg.Checkbox('All unchecked', enable_events=True, key='Uncheck_All')],
    [sg.HorizontalSeparator()]] + [
    [sg.Checkbox(f'check ({j}, {i})', enable_events=True, key=f'check{j}{i}')
        for i in range(5)] for j in range(4)
]

window = sg.Window ('Sample GUI', layout, finalize=True)

while True: # Event Loop
    event, values = window.read (timeout = 100)
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Check_All':
        for j in range(4):
            for i in range(5):
                window[f'check{j}{i}'].update(True)
        window['Uncheck_All'].update(False)
    elif event == 'Uncheck_All':
        for j in range(4):
            for i in range(5):
                window[f'check{j}{i}'].update(False)
        window['Check_All'].update(False)
    elif event.startswith('check'):
        if not values[event]:
            window['Check_All'].update(False)
        else:
            window['Uncheck_All'].update(False)

window.close ()