def user_serializer(user) -> dict:
    return {
        'id': str(user['_id']),
        'email': user['email'],
        'hashed_password': user['hashed_password']
    }