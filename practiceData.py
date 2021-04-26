import requests
import json

import secrets
import models
from models import Price
from sqlalchemy.orm import sessionmaker
import psycopg2


print('Layer 1s are coins like BTC or LTC while Tokens are on L2s like ERC20s/ERC721s')
choice = str(input('choose which one to look up: coin or token? '))




if choice.lower() == 'token':

    tokenAddress = str(input('What token do you want to look up? '))

    url = "https://web3api.io/api/v2/market/tokens/prices/" + tokenAddress + '/latest'

    headers = {"x-api-key": secrets.api_key}

    response = requests.get(url, headers=headers)
    query = json.loads(response.content)
    payload = query['payload']
    tkADD = payload[0]['address']
    tkNAME = payload[0]['name']
    tkSYMBOL = payload[0]['symbol']
    tkPRICE = payload[0]['priceUSD']
    print(tkADD, tkPRICE, tkNAME, tkSYMBOL)

    db_string = 'postgresql://postgres:'+secrets.password+'@localhost/practiceDataDB'
    db = models.create_engine(db_string, echo=False)
    base = models.declarative_base()
    base.metadata.create_all(db)
    db_Session = sessionmaker(db)
    db_session = db_Session()
    result = Price(
        address=tkADD,
        name=tkNAME,
        symbol=tkSYMBOL,
        price=tkPRICE
    )

    db_session.add(result)
    db_session.commit()
    print('entry added')
    db_session.close()

    #print(json.loads(response.content))


# ask Brian about api cost
elif choice.lower() == 'coin':
    coinName = str(input('What coin do you want to look up? '))
    url2 = "https://web3api.io/api/v2/market/spot/prices/assets/" + coinName + "/latest/"

    headers2 = {"x-api-key": secrets.api_key}

    querystring2 = {"format": "csv"}

    responses = requests.request("GET", url2, headers=headers2, params=querystring2)

    print(responses.text)
