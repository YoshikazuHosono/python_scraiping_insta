
import json
FETCH_COUNT = 20

GET_FORROWER_URL_TEMPLATE = '{"id":"1632264012","include_reel":true,"fetch_mutual":true,"first":20}'

def createGetFollowerUrl(id,isAfter,endCursor):
    param = {
        "id" : id
        ,"include_reel" : False
        ,"fetch_mutual" : True
        ,"first" : FETCH_COUNT
    }

    if isAfter:
        param["after"] = endCursor

    return json.dumps(param)

print(createGetFollowerUrl("1632264012",True,"aaaaaaaaaaaa"))
