from django.http import JsonResponse
import json

# respond with new item
def respondWithNewItem(statusCode, data, transformer):
    response = {}
    response['data'] = transformer.transform(data)
    
    response['notification'] = {}
    response['notification']['hint'] = "Response Sent"
    response['notification']['message'] = "Success"
    response['notification']['code'] = "200"
    response['notification']['type'] = "Success"
    
    return JsonResponse(response, content_type='application/json', status=statusCode)

# # respond with item
def respondWithItem(statusCode, data, transformer):
    response = {}
    response['data'] = transformer.transform(data)
    
    response['notification'] = {}
    response['notification']['hint'] = "Response Sent"
    response['notification']['message'] = "Success"
    response['notification']['code'] = "200"
    response['notification']['type'] = "Success"
    
    return JsonResponse(response, content_type='application/json', status=statusCode)

# respond with error
def respondWithError(statusCode, message):
    response = {}
    response['data'] = []
    
    response['notification'] = {}
    response['notification']['hint'] = "Error"
    response['notification']['message'] = message
    response['notification']['code'] = statusCode
    response['notification']['type'] = "Failed"
    
    return JsonResponse(response, content_type='application/json', status=statusCode)

# respond with success
def respondWithSuccess(statusCode, message):
    response = {}
    response['data'] = []
    
    response['notification'] = {}
    response['notification']['hint'] = "Success"
    response['notification']['message'] = message
    response['notification']['code'] = statusCode
    response['notification']['type'] = "Success"
    
    return JsonResponse(response, content_type='application/json', status=statusCode)

# respond with collection
def respondWithCollection(statusCode, data, transformer):
    response = {}
    response['data'] = fetchDataFromTransformer(transformer, data)
    
    response['notification'] = {}
    response['notification']['hint'] = "Response Sent"
    response['notification']['message'] = "Success"
    response['notification']['code'] = "200"
    response['notification']['type'] = "Success"
    
    return JsonResponse(response, content_type='application/json', status=statusCode)

# fetch data from respective transformer
def fetchDataFromTransformer(transformer, data):
    result = []
    for key, value in enumerate(data):
        result.append(transformer.transform(value))
    return result
        