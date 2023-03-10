import time
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox
from db import db
from functions import note


class initial_window:
    def __init__(self):
        self.path = None
        self.data = list()

    def window(self):
        self.root = Tk()
        self.root.title("Выбор файла данных")
        self.root.geometry("300x140")
        self.root.resizable(False, False)
        btn_create_new = Button(self.root, text="Новые заметки", command=lambda: self.get_path(False))
        btn_create_new.pack(anchor='center', pady=10)
        btn_open = Button(self.root, text="Выбрать существующие заметки", command=lambda: self.get_path(True))
        btn_open.pack(anchor='center', pady=10)
        btn_exit = Button(self.root, text='Выход', command=self.__exit_program)
        btn_exit.pack(anchor='center', pady=10)
        self.root.mainloop()

    def get_path(self, is_open: bool):
        self.__exit_program()
        if is_open:
            self.path = fd.askopenfilename(filetypes=(("JSON files", "*.json"), ("All files", "*.*")),
                                           defaultextension='.json')
            stf = db(self.path)
            self.data = stf.extract()
        else:
            self.path = ''

    def __exit_program(self):
        self.root.destroy()


class main_window:
    def __init__(self, initial: initial_window):
        self.initial = initial

    def window(self):
        self.root = Tk()
        self.root.title('Заметки')
        self.root.geometry('500x500')
        self.root.resizable(False, False)
        self.notes_frame = Frame(master=self.root, height=25, width=400)
        self.notes_frame.pack(anchor='center', padx=5, pady=5)
        self.notes_list = Listbox(master=self.notes_frame, height=25, width=400,
                                  listvariable=Variable(value=self.initial.data))
        self.notes_list.pack()
        self.button_frame_notes = Frame(master=self.root, height=3, width=400)
        self.button_frame_notes.pack(anchor='center', padx=5, pady=3)
        self.button_create_note = Button(master=self.button_frame_notes, text='Создать заметку',
                                         command=lambda: self.__change_note(True))
        self.button_create_note.grid(row=0, column=0, padx=5, pady=5)
        self.button_edit_note = Button(master=self.button_frame_notes, text='Открыть заметку',
                                       command=self.__select_note)
        self.button_edit_note.grid(row=0, column=1, padx=5, pady=5)
        self.button_del_note = Button(master=self.button_frame_notes, text='Удалить заметку',
                                      command=lambda: self.__select_note(False))
        self.button_del_note.grid(row=0, column=2, padx=5, pady=5)
        self.button_sort = Button(master=self.button_frame_notes, text='Сортировать заметки', command=self.__sort_notes)
        self.button_sort.grid(row=0, column=3, padx=5, pady=5)
        self.button_frame_global = Frame(master=self.root, height=3, width=400)
        self.button_frame_global.pack(anchor='center', padx=5, pady=3)
        self.button_save = Button(master=self.button_frame_global, text='Сохранить', command=self.__save)
        self.button_save.grid(row=1, column=0, padx=5, pady=5)
        self.button_save_as = Button(master=self.button_frame_global, text='Сохранить как...', command=self.__save_as)
        self.button_save_as.grid(row=1, column=1, padx=5, pady=5)
        self.button_ext = Button(master=self.button_frame_global, text='Выйти', command=self.__close)
        self.button_ext.grid(row=1, column=2, padx=5, pady=5)
        self.root.mainloop()

    def __close(self):
        if messagebox.askyesno('Выход из программы',
                               'Все не сохраненные данные будут потеряны.\nУверены, что хотите выйти?'):
            self.root.destroy()

    def __save_as(self):
        path = fd.asksaveasfilename(filetypes=(("JSON files", "*.json"), ("All files", "*.*")),
                                    defaultextension='.json')
        self.initial.path = path if path else self.initial.path
        if self.initial.path:
            self.__save()

    def __save(self):
        if self.initial.path:
            saver = db(self.initial.path)
            saver.save(self.initial.data)
        else:
            self.__save_as()

    def __sort_notes(self):
        self.sort_window = Tk()
        self.sort_window.title('Поле сортировки')
        self.sort_window.geometry('250x200')
        self.sort_window.resizable(False, False)
        self.sort_window.attributes('-topmost', True)
        position = {'anchor': 'center', 'padx': 5, 'pady': 5}
        var_sort = StringVar(value='id')
        var_sort.set('id')
        Label(master=self.sort_window, text='Нажмите на способ сортировки').pack(**position)
        self.sort_id_button = Button(master=self.sort_window, text='По номеру', command=lambda: self.__sort_start('id'))
        self.sort_id_button.pack(**position)
        self.sort_time_button = Button(master=self.sort_window, text='По времени создания/изменения',
                                       command=lambda: self.__sort_start('time_change'))
        self.sort_time_button.pack(**position)
        self.sort_title_button = Button(master=self.sort_window, text='По заголовку',
                                        command=lambda: self.__sort_start('title'))
        self.sort_title_button.pack(**position)
        self.sort_window.mainloop()

    def __sort_start(self, sort_mode: str):
        for item in self.initial.data:
            item.sort_type = sort_mode
        self.initial.data.sort()
        self.__update()
        self.sort_window.destroy()

    def __select_note(self, is_edit: bool = True):
        list_selection = self.notes_list.curselection()
        if len(list_selection):
            if is_edit:
                self.__change_note(False, self.initial.data[list_selection[0]])
            else:
                self.__delete_note(list_selection[0])

    def __delete_note(self, number: int):
        if messagebox.askyesno('Удаление заметки',
                               f'Вы уверены, что хотите удалить заметку "{self.initial.data[number].title}"?'):
            self.initial.data.pop(number)
            self.__update()

    def __change_note(self, is_new: bool, editable_note: note = None):
        self.note_window = Tk()
        self.note_window.title('Заметка')
        self.note_window.geometry('500x500')
        self.note_window.resizable(False, False)
        self.note_window.attributes('-topmost', True)
        Label(master=self.note_window, text='Заголовок:').pack(anchor='nw', padx=5)
        if is_new:
            self.note_title_entry = Entry(master=self.note_window, width=100)
            self.note_title_entry.pack(anchor='nw', padx=5)
        else:
            Label(master=self.note_window, text=editable_note.title).pack(anchor='nw', padx=5)
        Label(master=self.note_window, text='Текст заметки:').pack(anchor='nw', padx=5)
        self.note_text_field = Text(master=self.note_window, width=100, height=25)
        if not is_new:
            self.note_text_field.insert(0.0, editable_note.text)
        self.note_text_field.pack(anchor='nw', padx=5)
        self.button_save_note = Button(master=self.note_window, text='Сохранить заметку',
                                       command=self.__save_new_note if is_new else lambda: self.__edit_note(
                                           editable_note))
        self.button_save_note.pack(anchor='center', pady=5)
        self.note_window.mainloop()

    def __save_new_note(self):
        title = self.note_title_entry.get()
        if title:
            for item in self.initial.data:
                item.sort_type = 'id'
            note_id = 1 if not len(self.initial.data) else max(self.initial.data).id + 1
            text = self.note_text_field.get(0.0, END)
            self.initial.data.append(note(note_id, time.time(), time.ctime(), title, text))
            self.__update()
            self.note_window.destroy()
        else:
            messagebox.showerror('Ошибка', 'Введите заголовок заметки')

    def __edit_note(self, ed_note: note):
        ed_note.time_change_stamp = time.time()
        ed_note.time_change = time.ctime()
        ed_note.text = self.note_text_field.get(0.0, END)
        self.__update()
        self.note_window.destroy()

    def __update(self):
        self.notes_list.config(listvariable=Variable(value=self.initial.data))
