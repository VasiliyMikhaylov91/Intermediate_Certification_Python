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
            self.path = fd.askopenfilename(filetypes=(("JSON files", "*.json"), ("CSV files", "*.csv")),
                                           defaultextension='.json')
            stf = db(self.path)
            self.data = stf.extract()
        else:
            self.path = fd.asksaveasfilename(filetypes=(("JSON files", "*.json"), ("CSV files", "*.csv")),
                                             defaultextension='.json')
            stf = db(self.path)
            stf.save(self.data)

    def __exit_program(self):
        self.root.destroy()


class main_window:
    def __init__(self, initial: initial_window):
        self.initial = initial

    # def __list_create(self):
    #     new_list = []
    #     for key in self.initial.data.keys():
    #         new_list.append(f'{key}  {self.initial.data[key]["time_change"]}  {self.initial.data[key]["title"]}')
    #     return Variable(value=new_list)

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
        self.button_frame = Frame(master=self.root, height=5, width=400)
        self.button_frame.pack(anchor='center', padx=5, pady=5)
        self.button_create_note = Button(master=self.button_frame, text='Создать заметку', command=self.__note)
        self.button_create_note.grid(row=0, column=0, padx=5, pady=5)
        self.button_edit_note = Button(master=self.button_frame, text='Открыть заметку')
        self.button_edit_note.grid(row=0, column=1, padx=5, pady=5)
        self.button_del_note = Button(master=self.button_frame, text='Удалить заметку')
        self.button_del_note.grid(row=0, column=2, padx=5, pady=5)
        self.button_save = Button(master=self.button_frame, text='Сохранить')
        self.button_save.grid(row=1, column=0, padx=5, pady=5)
        self.button_save_as = Button(master=self.button_frame, text='Сохранить как...')
        self.button_save_as.grid(row=1, column=1, padx=5, pady=5)
        self.button_ext = Button(master=self.button_frame, text='Выйти')
        self.button_ext.grid(row=1, column=2, padx=5, pady=5)
        self.root.mainloop()

    def __note(self):
        self.note_window = Tk()
        self.note_window.title('Заметка')
        self.note_window.geometry('500x500')
        self.note_window.resizable(False, False)
        self.note_window.attributes('-topmost', True)
        Label(master=self.note_window, text='Заголовок:').pack(anchor='nw', padx=5)
        self.note_title_entry = Entry(master=self.note_window, width=100)
        self.note_title_entry.pack(anchor='nw', padx=5)
        self.note_text_field = Text(master=self.note_window, width=100, height=25)
        Label(master=self.note_window, text='Текст заметки:').pack(anchor='nw', padx=5)
        self.note_text_field.pack(anchor='nw', padx=5)
        self.button_save_note = Button(master=self.note_window, text='Сохранить заметку', command=self.save_new_note)
        self.button_save_note.pack(anchor='center', pady=5)
        self.note_window.mainloop()

    def save_new_note(self):
        title = self.note_title_entry.get()
        if title:
            note_id = 1 if not len(self.initial.data) else max(self.initial.data).id + 1
            text = self.note_text_field.get(0.0, END)
            # self.initial.data[id] = {"time_change_stamp": time.time(),
            #                          "time_change": time.ctime(),
            #                          "title": title,
            #                          "text": text}
            self.initial.data.append(note(note_id, time.time(), time.ctime(), title, text))
            self.notes_list.config(listvariable=Variable(value=self.initial.data))
            self.note_window.destroy()
        else:
            messagebox.showerror('Ошибка', 'Введите заголовок заметки')
