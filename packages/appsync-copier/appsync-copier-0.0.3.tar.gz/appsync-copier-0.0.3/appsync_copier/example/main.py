from ..utility import singular_to_plural
from .data import database, new_database


def run_mutation(model_name, params):

    print("hello", model_name)

    old_id = params.get('id')
    if 'new' in old_id:
        print('Something weird happened')
        exit()

    del params['id']
    created = {
        'id': f'new-{old_id}',
        **params
    }

    plurar = singular_to_plural(model_name)
    table = f"list{plurar}"

    if new_database.get(table) is None:
        new_database[table] = []

    new_database[table].append(created)
    return created


def run_query(query, modelName):
    plurar = singular_to_plural(modelName)
    return database[f'list{plurar}']


def run_filter_query(child, reference_parent, parent_id):
    plurar = singular_to_plural(child)
    lst = database[f'list{plurar}']
    result = []
    for item in lst:
        if item[reference_parent] == parent_id:
            result.append(item)
    return result


def get_by_id(model_name, id):
    plurar = singular_to_plural(model_name)
    lst = database[f'list{plurar}']
    for item in lst:
        if item['id'] == id:
            return item
