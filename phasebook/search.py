from flask import Blueprint, request

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200


def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """

    results = set()

    # Filter by id
    if 'id' in args:
        user = next((user for user in USERS if user['id'] == args['id']), None)
        if user:
            results.add(tuple(user.items()))

    # Filter by name
    if 'name' in args:
        name = args['name'].lower()
        for user in USERS:
            if name in user['name'].lower():
                results.add(tuple(user.items()))

    # Filter by age
    if 'age' in args:
        try:
            age = int(args['age'])
            for user in USERS:
                if age - 1 <= user['age'] <= age + 1:
                    results.add(tuple(user.items()))
        except ValueError:
            pass

    # Filter by occupation
    if 'occupation' in args:
        occupation = args['occupation'].lower()
        for user in USERS:
            if occupation in user['occupation'].lower():
                results.add(tuple(user.items()))

    # Convert set of tuples back to list of dictionaries with specified order
    result_list = [dict([
        ('id', dict(user)['id']),
        ('name', dict(user)['name']),
        ('age', dict(user)['age']),
        ('occupation', dict(user)['occupation'])
    ]) for user in results]

    # Sort the result list by id
    result_list.sort(key=lambda x: x['id'])

    return result_list
