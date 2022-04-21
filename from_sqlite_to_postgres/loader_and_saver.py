from dataclasses import astuple

from psycopg2.extras import execute_values


class SQLiteLoader:

    def __init__(self, sqlite_cursor):
        self.sqlite_cursor = sqlite_cursor

    def load_data(self, table, dataclass, row_amount):
        self.sqlite_cursor.execute(f"SELECT * FROM {table}")
        amount_of_fields = dataclass.amount_of_fields()
        while True:
            records = self.sqlite_cursor.fetchmany(row_amount)
            data = []
            if not records:
                break
            for row in records:
                field_values = [row[i] for i in range(amount_of_fields)]
                dataclass_obj = dataclass(*field_values)
                data.append(astuple(dataclass_obj))
            yield data


class PostgresSaver:
    def __init__(self, pg_cursor):
        self.pg_cursor = pg_cursor

    def save_data(self, data, table, dataclass):
        part_data = [part_data for part_data in data]
        for args in part_data:
            query = f"""
                INSERT INTO content.{table} ({dataclass.fields_names()})
                VALUES %s ON CONFLICT (id) DO NOTHING
                """
            execute_values(self.pg_cursor, query, args)
