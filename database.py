import sqlalchemy as db
from sqlalchemy import inspect as Inspector
from sqlalchemy.engine import reflection

class DataBase:
    def __init__(self, name_database='pokemon'):
        self.name = name_database
        self.url = f"sqlite:///{name_database}.db"
        self.engine = db.create_engine(self.url)
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()
        self.inspector = reflection.Inspector.from_engine(self.engine)

    def create_table(self, name_table, **kwargs):
        if name_table not in self.inspector.get_table_names():
            columns = [db.Column(k, v, primary_key=True) if 'id_' in k else db.Column(k, v) for k, v in kwargs.items()]
            new_table = db.Table(name_table, self.metadata, *columns)
            self.metadata.create_all(self.engine)
            print(f"Table '{name_table}' created successfully.")
        else:
            print(f"Table '{name_table}' already exists.")

    def add_row(self, name_table, **kwargs):
        table = db.Table(name_table, self.metadata, autoload_with=self.engine)
        try:
            stmt = db.insert(table).values(**kwargs)
            self.connection.execute(stmt)
        except db.exc.IntegrityError as e:
            print(f"Row with id {kwargs.get('id_')} already exists. Skipping: {e}")
