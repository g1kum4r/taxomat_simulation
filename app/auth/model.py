class UserModel:
    id: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    is_authenticated = True

    def __init__(self, ob: dict):
        self.id = ob.get('_id').__str__()
        self.email = ob.get('email')
        self.first_name = ob.get('first_name')
        self.last_name = ob.get('last_name')
        self.is_active = ob.get('is_active', True)

    def get_id(self):
        return self.id

    def get_username(self):
        if self.first_name is not None or self.last_name is not None:
            return f'{self.first_name} {self.last_name}'.strip()
        else:
            return self.email
