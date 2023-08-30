# sqlalchemy-counter
A simple tool for counting queries and debugging with sqlalchemy sessions.

## Motivation
ORMs are powerful tools but it's easy to end up with overly-complicated queries that hurt performance. SQLAlchemyQueryCounter can help debug these issues by printing all executed queries in a statement when the query count is not what was expected.

Example usage:

````
    with SQLAlchemyQueryCounter(session, expected_query_count=2):
        conn.execute("SELECT 1")
        conn.execute("SELECT 1")
````
