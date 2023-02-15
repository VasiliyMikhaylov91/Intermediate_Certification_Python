from GUI import initial_window, main_window


def start_program():
    iw = initial_window()
    iw.window()
    if iw.path != '':
        mw = main_window(iw)
        mw.window()
