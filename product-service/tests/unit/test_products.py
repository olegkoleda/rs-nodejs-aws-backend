import json
import pytest
from product_service.lambda_func.products import handler as products_handler
from product_service.lambda_func.mock_data import products

def test_products():
    event = {}
    context = {}
    response = products_handler(event, context)
    
    assert response['statusCode'] == 200
    assert response['headers']['Content-Type'] == 'application/json'
    assert response['headers']['Access-Control-Allow-Origin'] == '*'
    assert response['headers']['Access-Control-Allow-Methods'] == 'GET'
    
    body = json.loads(response['body'])
    assert isinstance(body, list)
    assert len(body) == len(products)
    assert body == products
