from sqlalchemy import create_engine
from settings import STRING_CONNECTION


class Database:
    def __init__(self) -> None:
        self.string_connection = STRING_CONNECTION

    def database_connection(self):
        # Creates database connection
        engine = create_engine(self.string_connection, pool_reset_on_return = None)
        return engine