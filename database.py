import sqlite3
from typing import Union

from models import Stats, Url

class Database:
    def __init__(self, db: str):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.conn.execute("CREATE TABLE IF NOT EXISTS urls ("
                         "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                         "url TEXT NOT NULL,"
                         "short TEXT NOT NULL UNIQUE,"
                         "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                         "updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                         "clicks INTEGER DEFAULT 0)")
        self.conn.commit()

    def create_short_url(self, url: str, short: str) -> Url:
        try:
            self.cur.execute("INSERT INTO urls (url, short) VALUES (?, ?)", (url, short))
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Short code already exists")
        return self.__read_last_inserted()

    @staticmethod
    def __make_url(url: tuple) -> Url:
        return Url(id=url[0], url=url[1], shortCode=url[2], createdAt=url[3], updatedAt=url[4])

    def __read_last_inserted(self) -> Url:
        self.cur.execute("SELECT * FROM urls WHERE id = last_insert_rowid()")
        return self.__make_url(self.cur.fetchone())

    def get_short_url(self, short: str, raw: bool = False) -> Union[Url, tuple]:
        self.cur.execute("SELECT * FROM urls WHERE short = ?", (short,))
        if not (url := self.cur.fetchone()):
            raise ValueError("Short code not found")
        if raw:
            return url
        return self.__make_url(url)

    def update_short_url(self, short: str, url: str) -> Url:
        # check if the short code exists
        self.get_short_url(short)
        self.cur.execute("UPDATE urls SET url = ?, updated_at = CURRENT_TIMESTAMP WHERE short = ?", (url, short))
        self.conn.commit()
        return self.get_short_url(short)

    def delete_short_url(self, short: str):
        self.get_short_url(short)
        self.cur.execute("DELETE FROM urls WHERE short = ?", (short,))
        self.conn.commit()

    def get_stats(self, short: str) -> Stats:
        url = self.get_short_url(short, raw=True)
        return Stats(id=url[0], url=url[1], shortCode=url[2], createdAt=url[3], updatedAt=url[4], accessCount=url[5])

    def access_url(self, short: str) -> None:
        self.cur.execute("UPDATE urls SET clicks = clicks + 1 WHERE short = ?", (short,))
        self.conn.commit()

