class note:
    def __init__(self, id: int, time_change_stamp: int, time_change: str, title: str, text: str):
        self.id = id
        self.time_change_stamp = time_change_stamp
        self.time_change = time_change
        self.title = title
        self.text = text
        self.sort_type = 'id'

    def __str__(self):
        return f'{self.id}    {self.time_change}    {self.title}'

    def __gt__(self, other):
        match self.sort_type:
            case 'time_change':
                return self.time_change_stamp > other.time_change_stamp
            case 'title':
                return self.title > other.title
            case _:
                return self.id > other.id

    def __lt__(self, other):
        match self.sort_type:
            case 'time_change':
                return self.time_change_stamp < other.time_change_stamp
            case 'title':
                return self.title < other.title
            case _:
                return self.id < other.id

    def __ge__(self, other):
        match self.sort_type:
            case 'time_change':
                return self.time_change_stamp >= other.time_change_stamp
            case 'title':
                return self.title >= other.title
            case _:
                return self.id >= other.id

    def __le__(self, other):
        match self.sort_type:
            case 'time_change':
                return self.time_change_stamp <= other.time_change_stamp
            case 'title':
                return self.title <= other.title
            case _:
                return self.id <= other.id
