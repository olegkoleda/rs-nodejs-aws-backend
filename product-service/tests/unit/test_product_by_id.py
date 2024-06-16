import json
import pytest
from product_service.lambda_func.product_by_id import handler as getproductbyid_handler

def test_getproductbyid_found():
    event = {
        'pathParameters': {
            'productId': '1'
        }
    }
    context = {}
    response = getproductbyid_handler(event, context)
    
    assert response['statusCode'] == 200
    assert response['headers']['Content-Type'] == 'application/json'
    assert response['headers']['Access-Control-Allow-Origin'] == '*'
    assert response['headers']['Access-Control-Allow-Methods'] == 'GET'
    
    body = json.loads(response['body'])
    assert isinstance(body, dict)
    assert body['id'] == 1
    assert body['title'] == 'Chun Mee'
    assert body['price'] == 24
    assert body['description'] == 'Good tea'

def test_getproductbyid_not_found():
    event = {
        'pathParameters': {
            'productId': '999'
        }
    }
    context = {}
    response = getproductbyid_handler(event, context)
    
    assert response['statusCode'] == 404
    assert response['headers']['Content-Type'] == 'application/json'
    assert response['headers']['Access-Control-Allow-Origin'] == '*'
    assert response['headers']['Access-Control-Allow-Methods'] == 'GET'
    
    body = json.loads(response['body'])
    assert isinstance(body, dict)
    assert body['message'] == 'Product not found'
