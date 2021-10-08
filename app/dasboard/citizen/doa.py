from pymongo import ASCENDING
from pymongo.errors import BulkWriteError

from app import mongo


class CitizenModel:
    cnic: int
    ntn: int
    bank_accounts: []
    utilities:  []
    telecommunication:  []
    fuel_stations:  []

    def __init__(self, _dict: dict):
        self.cnic = _dict.get('cnic')
        self.ntn = _dict.get('ntn')
        self.bank_accounts = _dict.get('bank_accounts')
        self.utilities = _dict.get('utilities')
        self.telecommunication = _dict.get('telecommunication')
        self.fuel_stations = _dict.get('fuel_stations')


def get_bank_account(cnic, ntn):
    pass


def get_utility_account(cnic, ntn):
    pass


def get_telecommunication(cnic, ntn):
    pass


def get_fuel_stations(cnic, ntn):
    pass


def generate_list(limit=1, start_from_cnic=None):
    citizens = []
    citizen = None
    if start_from_cnic is None:
        try:
            citizen = mongo.db.citizens.find().sort('cnic', True).first()
        except AttributeError as e:
            print(f'AttributeError: {e}')
    else:
        try:
            citizen = mongo.db.citizens.find({'cnic': start_from_cnic}).first()
        except AttributeError as e:
            print(f'AttributeError: {e}')
            citizen = CitizenModel({'cnic': start_from_cnic, 'ntn': int(f'{start_from_cnic}'[:8])})

    if citizen is not None:

        if not isinstance(citizen, CitizenModel):
            citizen = CitizenModel(citizen)

        last_cnic = citizen.cnic
        last_ntn = citizen.ntn
    else:
        last_cnic = 2110141516123
        last_ntn = 41516123

    for i in range(limit):
        cnic = int(last_cnic) + i
        ntn = int(last_ntn) + i
        citizens.append({
            'cnic': cnic,
            'ntn': ntn,
            'bank_accounts':  get_bank_account(cnic, ntn),
            'utilities':  get_utility_account(cnic, ntn),
            'telecommunication':  get_telecommunication(cnic, ntn),
            'fuel_stations':  get_fuel_stations(cnic, ntn)
        })
    mongo.db.citizens.ensure_index([("cnic", ASCENDING), ("slug", ASCENDING)], unique=True, dropDups=True)
    mongo.db.citizens.ensure_index([("ntn", ASCENDING), ("slug", ASCENDING)], unique=True, dropDups=True)
    return mongo.db.citizens.insert_many(citizens)


def citizens_list(offset=0, limit=0):
    return {
        'count': mongo.db.citizens.count(),
        'list':  mongo.db.citizens.find().skip(offset).limit(limit)
    }
