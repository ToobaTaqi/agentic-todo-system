def get_next_id(todos):
    if not todos:
        return 1
    return max(todo.id for todo in todos) + 1
