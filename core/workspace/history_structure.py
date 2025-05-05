import datetime


class History:
    blocks: list = []
    time: datetime.datetime
    is_read_only: bool = False

    def __init__(self, title, blocks, time=None, is_read_only=False) -> None:
        super().__init__()
        if blocks is None:
            blocks = []
        if not time:
            time = datetime.datetime.now()
        self.title = title
        self.blocks = blocks
        self.time = time
        self.is_read_only = is_read_only

    def get_dict(self):
        return {
            'title': self.title,
            'blocks': self.blocks,
            'is_read_only': self.is_read_only,
            'time': self.time.timestamp()
        }

    def is_recently(self):
        last_5_minute = datetime.datetime.now() - datetime.timedelta(minutes=5)
        return self.time > last_5_minute

    @staticmethod
    def create_from_dict(dict_data):
        return History(
            title=dict_data.get('title'),
            blocks=dict_data.get('blocks', []),
            is_read_only=dict_data.get('is_read_only', False),
            time=datetime.datetime.fromtimestamp(dict_data.get('time'))
        )
