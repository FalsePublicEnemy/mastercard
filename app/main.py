import logging
from dataclasses import dataclass
from uuid import uuid4
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
database = dict()

logger = logging.getLogger(__name__)

# Create a validator and make a difference between
# request validator and db model
class AccountCreateValidator(BaseModel):
    name: str
    email: str
    balance: float
    active: bool = True
    description: Optional[str] = None

# Use dataclass for more handy usage of object
@dataclass
class Account:
    id: str
    name: str
    email: str
    balance: float
    active: bool
    description: Optional[str]

    def to_db(self) -> None:
        database[self.id] = {
            'name': self.name,
            'email': self.email,
            'balance': self.balance,
            'active': self.active,
            'description': self.description,
        }

    def delete_from_db(self) -> None:
        database.pop(self.id)

# Make this func sync because there is no async interaction in function
def create_account(account: Account) -> None:
    # We could make additional work here arount Account creation
    # f.e. wallet creation etc.
    account.to_db()

def get_account_by_id(account_id: str) -> Optional[Account]:
    if account_id not in database.keys():
        raise HTTPException(status_code=404, detail='Account is not found with this ID')

    account = database[account_id]
    return Account(
        id=account_id,
        name=account['name'],
        email=account['email'],
        balance=account['balance'],
        active=account['active'],
        description=account['description'],
    )

@app.get('/api/health')
async def healthcheck():
    if database.get('db_down'):
        # Don't show reason of server error to customer
        # Log into server logs instead
        # TODO: Add sentry logging
        logger.error('DB Down')
        raise HTTPException(status_code=500, detail='Service unavailable')
    return {'message': 'Server is running'}

# Make creation POST instead of PUT
# Also make route through /api, because we could have other services on this host, f.e. admin panel
@app.post('/api/accounts', status_code=201)
async def add_account(request: AccountCreateValidator):
    if request.email in [account['email'] for account in database.values()]:
        raise HTTPException(status_code=400, detail='Email is already exists')

    account = Account(
        # Make id autogenerated instead of set via request
        id=str(uuid4()),
        name=request.name,
        # Make email unique instead of record id
        email=request.email,
        balance=request.balance,
        active=request.active,
        description=request.description,
    )
    create_account(account)
    logger.info('Account created', extra=account.__dict__)
    return {'result': account.__dict__}


@app.get('/api/accounts')
async def get_accounts():
    return database


@app.get('/api/accounts/{account_id}')
async def get_account(account_id: str):
    account = get_account_by_id(account_id)
    return {'result': account.__dict__}


@app.delete('/api/accounts/{account_id}')
async def delete_account(account_id: str):
    # We are checking account existance by reusing same function as in getting account
    account = get_account_by_id(account_id)
    account.delete_from_db()
    logger.info('Account deleted', extra=account.__dict__)
    return {}
