import requests
import json
import datetime
import secrets
import models
from models import Price, Historical
from sqlalchemy.orm import sessionmaker
import psycopg2


print('Layer 1s are coins like BTC or LTC while Tokens are on L2s like ERC20s/ERC721s')
choice = str(input('choose which one to look up: coin or token? '))
# raise Error if not coin or token
choice2 = str(input('Latest price or historical?: '))
# raise Error here if not right




if choice.lower() == 'token':
    if choice2.lower() == 'latest':

        tokenAddress = str(input('input hash of token do you want to look up? '))

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
    if choice2.lower() == 'historical':
        # https://docs.amberdata.io/reference#get-historical-token-price for questions on querystring
        tokenAddress2 = str(input('input hash of token you want to look up? '))
        url = "https://web3api.io/api/v2/market/tokens/prices/"+tokenAddress2+"/historical"

        querystring = {"timeInterval": "d", "timeFormat": "ms"}

        headers = {"x-api-key": secrets.api_key}

        response = requests.get(url, headers=headers, params=querystring)
        query2 = json.loads(response.content)
        # historical data api doesn't give a name in the output field
        payload2 = query2["payload"]["data"]
        db_string2 = 'postgresql://postgres:' + secrets.password + '@localhost/Historical0x'
        db2 = models.create_engine(db_string2, echo=False)
        base = models.declarative_base()
        base.metadata.create_all(db2)
        db_Session2 = sessionmaker(db2)
        db_session2 = db_Session2()
        for p in payload2:
            s = p[0] / 1000.0
            print(s, p[1])
            result2 = Historical(
                Day=datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f'),
                Price=p[1]
            )
            db_session2.add(result2)
        db_session2.commit()
        print('Entries Added')
        db_session2.close()
        # print(json.dumps(payload2, indent=4, sort_keys=True))

        #print(response.text)



# ask Brian about api cost
elif choice.lower() == 'coin':
    coinName = str(input('What coin do you want to look up? '))
    url2 = "https://web3api.io/api/v2/market/spot/prices/assets/" + coinName + "/latest/"

    headers2 = {"x-api-key": secrets.api_key}

    querystring2 = {"format": "csv"}

    responses = requests.request("GET", url2, headers=headers2, params=querystring2)

    print(responses.text)
