from sqlalchemy.event import listen, remove
from sqlalchemy.orm import Session


class SQLAlchemyQueryCounter:
    """
    Check SQLAlchemy query count.
    Usage:
        with SQLAlchemyQueryCounter(session, expected_query_count=2):
            conn.execute("SELECT 1")
            conn.execute("SELECT 1")
    """

    def __init__(self, session: Session, expected_query_count: int):
        self.session = session.get_bind()
        self._query_count = expected_query_count
        self.count = 0
        self.executed_queries = ""

    def __enter__(self):
        listen(self.session, "before_cursor_execute", self._callback)
        return self

    def __exit__(self, *_):
        remove(self.session, "before_cursor_execute", self._callback)
        assert self.count == self._query_count, (
            "Executed: "
            + str(self.count)
            + " != Required: "
            + str(self._query_count)
            + f"{self.executed_queries}"
        )

    def _callback(self, conn, cursor, statement, parameters, *_):
        self.count += 1
        if parameters and isinstance(parameters, tuple):
            parameters = parameters[0]

            for param, value in parameters.items():
                statement = statement.replace("%(" + param + ")s", str(value))

        self.executed_queries += f"\n\nQuery {self.count}: \n{str(statement)}"
