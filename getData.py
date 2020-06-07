import requests
#get predictions
def getdata(startDate,endDate,provider,predictionObject):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://graphql.anilkuscu.io',
        "authorization": <Your authorization header>,
    }
    data = <Your graphql quary with start-end date>
    response = requests.post('https://graphql.anilkuscu.io/graphql', headers=headers, data=data)
    return response.text
#Get realized production data
def getproductiondata(startDate,endDate,predictionObject):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Connection': 'keep-alive',
        'Origin': 'https://graphql.anilkuscu.io',
        "authorization": <Your authorization header>,
    }

    data=data = <Your graphql quary with start-end date>
    response = requests.post('https://graphql.anilkuscu.io/graphql', headers=headers, data=data)
    return response.text
