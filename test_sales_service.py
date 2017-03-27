import json

import requests
from nose.tools import assert_equal

from sales_service import SECURE_STRING

_ip = "0.0.0.0:8080"


def test_request_response():
    # Send a request to the API server and store the response.
    s = requests.Session()

    data = {
        "sku": "test",
        "description": "just a test product"
    }

    # data = json.dumps(data)
    r = s.put('http://{0}/{1}/sku'.format(_ip, SECURE_STRING), data=json.dumps(data))

    # Confirm that the request-response cycle completed successfully.

    data = {
        'success': True,
        'error': "",
        'data': data
    }

    data = json.dumps(data)
    assert_equal((r.status_code, r.text), (200, data))

    data = {
        "sku": "test",
        "description": "just a test product"
    }

    r = s.put('http://{0}/{1}/sku'.format(_ip, SECURE_STRING), data=json.dumps(data))

    # Confirm that the request-response cycle completed successfully.

    data = {
        'success': False,
        'error': "Duplicate data",
        'data': data
    }

    data = json.dumps(data)
    assert_equal((r.status_code, r.text), (200, data))

    data = {
        'success': True,
        'error': "",
        'data': "test"
    }
    data = json.dumps(data)
    r = s.delete('http://{0}/{1}/sku/{2}'.format(_ip, SECURE_STRING, "test"))

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, data))

    data = {
        'success': False,
        'error': "Can not delete",
        'data': "test"
    }
    data = json.dumps(data)
    r = s.delete('http://{0}/{1}/sku/{2}'.format(_ip, SECURE_STRING, "test"))

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, data))

    data = {
        'success': False,
        'error': "Can not delete",
        'data': "test1"
    }
    data = json.dumps(data)
    r = s.delete('http://{0}/{1}/sku/{2}'.format(_ip, SECURE_STRING, "test1"))

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, data))

    data = {
        "first_name": "test",
        "last_name": "test"
    }

    r = s.put('http://{0}/{1}/customer'.format(_ip, SECURE_STRING), data=json.dumps(data))

    data = {
        'success': True,
        'error': "",
        'data': data,
        'id': 1
    }
    data = json.dumps(data)
    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, data))

    r = s.delete('http://{0}/{1}/customer/{2}'.format(_ip, SECURE_STRING, '1'))

    # Confirm that the request-response cycle completed successfully.
    data = {
        'success': True,
        'error': "",
        'data': "1"
    }

    assert_equal((r.status_code, r.text), (200, json.dumps(data)))

    r = s.get('http://{0}/{1}/cart'.format(_ip, SECURE_STRING))

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, u'{}'))

    data = {
        "customer_id": 1,
        "sku": "test"
    }

    r = s.put('http://{0}/{1}/cart'.format(_ip, SECURE_STRING), data=json.dumps(data))

    data = {
        'success': False,
        'error': "Can not find customer with this id",
        'data': data
    }

    data = json.dumps(data)

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, data))

    r = s.get('http://{0}/{1}/cart'.format(_ip, SECURE_STRING))

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, u'{}'))

    data = {
        "first_name": "test",
        "last_name": "test"
    }

    r = s.put('http://{0}/{1}/customer'.format(_ip, SECURE_STRING), data=json.dumps(data))

    data = {
        'success': True,
        'error': "",
        'data': data,
        'id': 1
    }
    data = json.dumps(data)
    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, data))

    data = {
        "customer_id": 1,
        "sku": "test"
    }

    r = s.put('http://{0}/{1}/cart'.format(_ip, SECURE_STRING), data=json.dumps(data))

    data = {
        'success': False,
        'error': "Can not find product with this id",
        'data': data
    }

    data = json.dumps(data)

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, data))

    r = s.get('http://{0}/{1}/cart'.format(_ip, SECURE_STRING))

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, u'{}'))

    data = {
        "sku": "test",
        "description": "just a test product"
    }

    # data = json.dumps(data)
    r = s.put('http://{0}/{1}/sku'.format(_ip, SECURE_STRING), data=json.dumps(data))

    # Confirm that the request-response cycle completed successfully.

    data = {
        'success': True,
        'error': "",
        'data': data
    }

    data = json.dumps(data)
    assert_equal((r.status_code, r.text), (200, data))

    data = {
        "customer_id": 1,
        "sku": "test"
    }

    r = s.put('http://{0}/{1}/cart'.format(_ip, SECURE_STRING), data=json.dumps(data))

    data = {
        'success': True,
        'error': "",
        'data': data
    }

    data = json.dumps(data)

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, data))

    r = s.get('http://{0}/{1}/cart'.format(_ip, SECURE_STRING))

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, u'{"1": ["test"]}'))

    data = {
        "sku": "test2",
        "description": "just a test product"
    }

    # data = json.dumps(data)
    r = s.put('http://{0}/{1}/sku'.format(_ip, SECURE_STRING), data=json.dumps(data))

    # Confirm that the request-response cycle completed successfully.

    data = {
        'success': True,
        'error': "",
        'data': data
    }

    data = json.dumps(data)
    assert_equal((r.status_code, r.text), (200, data))

    data = {
        "customer_id": 1,
        "sku": "test2"
    }

    r = s.put('http://{0}/{1}/cart'.format(_ip, SECURE_STRING), data=json.dumps(data))

    data = {
        'success': True,
        'error': "",
        'data': data
    }

    data = json.dumps(data)

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, data))

    r = s.get('http://{0}/{1}/cart'.format(_ip, SECURE_STRING))

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, u'{"1": ["test", "test2"]}'))

    data = {
        "customer_id": 1,
        "sku": "test"
    }

    r = s.put('http://{0}/{1}/cart'.format(_ip, SECURE_STRING), data=json.dumps(data))

    data = {
        'success': False,
        'error': "This item already in the cart",
        'data': data
    }

    data = json.dumps(data)

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, data))

    data = {
        'success': False,
        'error': "Can not delete",
        'data': "test"
    }
    data = json.dumps(data)
    r = s.delete('http://{0}/{1}/sku/{2}'.format(_ip, SECURE_STRING, "test"))

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, data))

    r = s.delete('http://{0}/{1}/cart/{2}/{3}'.format(_ip, SECURE_STRING, 1, 'test'))

    data = {
        'success': True,
        'error': "",
        'data': ('1', 'test')
    }

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, json.dumps(data)))

    r = s.delete('http://{0}/{1}/cart/{2}/{3}'.format(_ip, SECURE_STRING, 1, 'test2'))

    data = {
        'success': True,
        'error': "",
        'data': ('1', 'test2')
    }

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, json.dumps(data)))

    data = {
        'success': True,
        'error': "",
        'data': "test2"
    }
    data = json.dumps(data)
    r = s.delete('http://{0}/{1}/sku/{2}'.format(_ip, SECURE_STRING, "test2"))

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, data))

    r = s.delete('http://{0}/{1}/cart/{2}/{3}'.format(_ip, SECURE_STRING, 1, 'test'))

    data = {
        'success': False,
        'error': "Can not delete",
        'data': ('1', 'test')
    }

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, json.dumps(data)))

    data = {
        'success': True,
        'error': "",
        'data': "test"
    }
    data = json.dumps(data)
    r = s.delete('http://{0}/{1}/sku/{2}'.format(_ip, SECURE_STRING, "test"))

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, data))

    r = s.delete('http://{0}/{1}/customer/{2}'.format(_ip, SECURE_STRING, '1'))

    # Confirm that the request-response cycle completed successfully.
    data = {
        'success': True,
        'error': "",
        'data': "1"
    }

    assert_equal((r.status_code, r.text), (200, json.dumps(data)))

    # ==================================================
    # Deleting a customer while products in the cart
    # ==================================================

    r = s.get('http://{0}/{1}/cart'.format(_ip, SECURE_STRING))

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, u'{}'))

    data = {
        "customer_id": 1,
        "sku": "test"
    }

    r = s.put('http://{0}/{1}/cart'.format(_ip, SECURE_STRING), data=json.dumps(data))

    data = {
        'success': False,
        'error': "Can not find customer with this id",
        'data': data
    }

    data = json.dumps(data)

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, data))

    r = s.get('http://{0}/{1}/cart'.format(_ip, SECURE_STRING))

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, u'{}'))

    data = {
        "first_name": "test",
        "last_name": "test"
    }

    r = s.put('http://{0}/{1}/customer'.format(_ip, SECURE_STRING), data=json.dumps(data))

    data = {
        'success': True,
        'error': "",
        'data': data,
        'id': 1
    }
    data = json.dumps(data)
    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, data))

    data = {
        "customer_id": 1,
        "sku": "test"
    }

    r = s.put('http://{0}/{1}/cart'.format(_ip, SECURE_STRING), data=json.dumps(data))

    data = {
        'success': False,
        'error': "Can not find product with this id",
        'data': data
    }

    data = json.dumps(data)

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, data))

    r = s.get('http://{0}/{1}/cart'.format(_ip, SECURE_STRING))

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, u'{}'))

    data = {
        "sku": "test",
        "description": "just a test product"
    }

    # data = json.dumps(data)
    r = s.put('http://{0}/{1}/sku'.format(_ip, SECURE_STRING), data=json.dumps(data))

    # Confirm that the request-response cycle completed successfully.

    data = {
        'success': True,
        'error': "",
        'data': data
    }

    data = json.dumps(data)
    assert_equal((r.status_code, r.text), (200, data))

    data = {
        "customer_id": 1,
        "sku": "test"
    }

    r = s.put('http://{0}/{1}/cart'.format(_ip, SECURE_STRING), data=json.dumps(data))

    data = {
        'success': True,
        'error': "",
        'data': data
    }

    data = json.dumps(data)

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, data))

    r = s.get('http://{0}/{1}/cart'.format(_ip, SECURE_STRING))

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, u'{"1": ["test"]}'))

    data = {
        "sku": "test2",
        "description": "just a test product"
    }

    # data = json.dumps(data)
    r = s.put('http://{0}/{1}/sku'.format(_ip, SECURE_STRING), data=json.dumps(data))

    # Confirm that the request-response cycle completed successfully.

    data = {
        'success': True,
        'error': "",
        'data': data
    }

    data = json.dumps(data)
    assert_equal((r.status_code, r.text), (200, data))

    data = {
        "customer_id": 1,
        "sku": "test2"
    }

    r = s.put('http://{0}/{1}/cart'.format(_ip, SECURE_STRING), data=json.dumps(data))

    data = {
        'success': True,
        'error': "",
        'data': data
    }

    data = json.dumps(data)

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, data))

    r = s.get('http://{0}/{1}/cart'.format(_ip, SECURE_STRING))

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, u'{"1": ["test", "test2"]}'))

    data = {
        "customer_id": 1,
        "sku": "test"
    }

    r = s.put('http://{0}/{1}/cart'.format(_ip, SECURE_STRING), data=json.dumps(data))

    data = {
        'success': False,
        'error': "This item already in the cart",
        'data': data
    }

    data = json.dumps(data)

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, data))

    r = s.delete('http://{0}/{1}/customer/{2}'.format(_ip, SECURE_STRING, '1'))

    # Confirm that the request-response cycle completed successfully.
    data = {
        'success': True,
        'error': "",
        'data': "1"
    }

    assert_equal((r.status_code, r.text), (200, json.dumps(data)))

    r = s.get('http://{0}/{1}/cart'.format(_ip, SECURE_STRING))

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, u'{}'))

    data = {
        'success': True,
        'error': "",
        'data': "test"
    }
    data = json.dumps(data)
    r = s.delete('http://{0}/{1}/sku/{2}'.format(_ip, SECURE_STRING, "test"))

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, data))

    data = {
        'success': True,
        'error': "",
        'data': "test2"
    }
    data = json.dumps(data)
    r = s.delete('http://{0}/{1}/sku/{2}'.format(_ip, SECURE_STRING, "test2"))

    # Confirm that the request-response cycle completed successfully.
    assert_equal((r.status_code, r.text), (200, data))


if __name__ == "__main__":
    test_request_response()
