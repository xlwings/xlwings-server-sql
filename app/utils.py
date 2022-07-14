def process_cursor_result(result):
    """Turn SQLAlchemy's CursorResult into a list of tuples"""
    columns = tuple(result.keys())
    data = [row for row in result.fetchall()]
    table = [columns]
    table.extend(data)
    return table
