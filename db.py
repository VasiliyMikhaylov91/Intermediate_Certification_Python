import json
from functions import note


class db:
    def __init__(self, path):
        self.path = path

    def save(self, data: list):
        if self.path.endswith('.json'):
            rec_dict = dict()
            if len(data):
                for item in data:
                    rec_dict[item.id] = {'time_change_stamp': item.time_change_stamp,
                                         'time_change': item.time_change,
                                         'title': item.title,
                                         'text': item.text}
            with open(self.path, 'w', encoding='utf-8') as file:
                json.dump(rec_dict, file)

    def extract(self):
        if self.path.endswith('.json'):
            with open(self.path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                res = list()
                for key in data.keys():
                    res.append(note(int(key),
                                    int(data[key]['time_change_stamp']),
                                    data[key]['time_change'],
                                    data[key]['title'],
                                    data[key]['text']))
            return res
