"""
This web service serves as a basic store with 'customer', 'product' and 'cart' tables
It supports following API calls:

PUT /{secure_string}/sku -                                  adds product to the service
DELETE /{secure_string}/sku/{product_sku} -                 removes product from the service by product_sku

PUT /{secure_string}/customer -                             adds product to the service
DELETE /{secure_string}/customer/{customer_id} -            removes customer from the service by customer_id

GET /{secure_string}/cart -                                 returns all customer's carts
PUT /{secure_string}/cart -                                 adds a product to the customer's cart
DELETE /{secure_string}/cart/{customer_id}/{product_sku} -  removes a product from the customer's cart
                                                            by customer_id and product_sku
"""
import json

import cherrypy
from sqlalchemy import create_engine

SECURE_STRING = "fm7m67u44p"
DB_STRING = "sale.db"
_engine = create_engine('sqlite:///sale.db', echo=True)


@cherrypy.expose
class Customer(object):
    """
    This class handles interaction with the Customer object in the database
    Methods:
        PUT - inserts a new customer into the table
        DELETE - removes a customer from the table
    """

    @cherrypy.tools.accept(media='text/plain')
    @cherrypy.tools.json_out()
    def PUT(self):
        """
        This method adds a new customer into the customer table
        :input:
        data = {
            'fist_name': 'customer_fist_name',
            'last_name': 'customer_last_name'
        }
        :return:
         res = {
            'success': False, - was the insertion successful or not
            'error': "", - error message
            'data': data, - original input data
            'id': None - id of the inserted row
        }
        """
        cl = cherrypy.request.headers['Content-Length']
        raw_body = cherrypy.request.body.read(int(cl))
        res = {
            'success': False,
            'error': "",
            'data': None,
            'id': None
        }

        try:
            data = json.loads(raw_body)
            res['data'] = data
        except:
            res['error'] = "Cannot parse json"
            return res

        conn = _engine.connect()
        insert = conn.execute(
            "INSERT INTO customer VALUES ('{0}', '{1}')".format(data['first_name'], data['last_name']))
        insert_id = insert.lastrowid
        if insert_id:
            res['success'] = True
            res['id'] = insert_id
        else:
            res['error'] = "Cannot insert data"
        conn.close()

        return res

    @cherrypy.tools.accept(media='text/plain')
    @cherrypy.tools.json_out()
    def DELETE(self, customer_id):
        """
        This method removes a customer for the table by the customer's id along with all products in his cart
        and all products added to the cart of this customer
        :param customer_id: customer's id
        :return:
        res = {
            'success': False, - was deletion successful or not
            'error': "", - error message
            'data': customer_id - customer's id
        }
        """
        res = {
            'success': False,
            'error': "",
            'data': customer_id
        }
        if customer_id:
            conn = _engine.connect()
            conn.execute("DELETE FROM cart WHERE customer_id='{0}'".format(customer_id))
            n = conn.execute("DELETE FROM customer WHERE rowid='{0}'".format(customer_id)).rowcount
            if n:
                res['success'] = True
            else:
                res['error'] = "Can not delete"
            conn.close()
        else:
            res['error'] = "No customer_id were passed"

        return res


@cherrypy.expose
class SKU(object):
    """
    This class handles interactions with the product table
    Methods:
        PUT: add a product to the table
        DELETE: removes a product from the table
    """

    @cherrypy.tools.accept(media='text/plain')
    @cherrypy.tools.json_out()
    def PUT(self):
        """
        This method adds a product to the table if it's sku is not present in the table
        :input:
        data = {
            'sku': '192837412', - product's sku number
            'description: 'a test product' - product's description
        }
        :return:
        res = {
            'success': False, - was the insertion successful or not
            'error': "", - error message
            'data': data, - original input data
        }
        """
        cl = cherrypy.request.headers['Content-Length']
        raw_body = cherrypy.request.body.read(int(cl))
        res = {
            'success': False,
            'error': "",
            'data': None
        }
        try:
            data = json.loads(raw_body)
            res['data'] = data
        except:
            res['error'] = "Can not parse json"
            return res

        conn = _engine.connect()
        sku = conn.execute("SELECT rowid FROM product WHERE sku='{0}'".format(data['sku'])).fetchone()
        if not sku:
            conn.execute("INSERT INTO product VALUES ('{0}', '{1}')".format(data['sku'], data['description']))
            res['success'] = True
        else:
            res['error'] = "Duplicate data"
        conn.close()

        return res

    @cherrypy.tools.accept(media='text/plain')
    @cherrypy.tools.json_out()
    def DELETE(self, product_id):
        """
        This method removes a product from the table if it's id is not present in carstomer's cart
        :param product_id: product's sku number
        :return:
        res = {
            'success': False, - was deletion successful or not
            'error': "", - error message
            'data': product_id - product's sku number
        }
        """
        res = {
            'success': False,
            'error': "",
            'data': product_id
        }
        if product_id:
            conn = _engine.connect()
            n = conn.execute("SELECT rowid FROM cart WHERE product_id='{0}'".format(product_id)).fetchone()
            if not n:
                n = conn.execute("DELETE FROM product WHERE sku='{0}'".format(product_id)).rowcount
                if n:
                    res['success'] = True
                else:
                    res['error'] = "Can not delete"
                conn.close()
            else:
                res['error'] = "Can not delete"
        else:
            res['error'] = "No product_id were passed"

        return res


@cherrypy.expose
class Cart(object):
    """
    This class handles interactions with 'cart' table
    Methods:
        GET - returns all customer's carts
        PUT - adds a product to the customer's cart
        DELETE - removes a product from the customer's cart
    """

    @cherrypy.tools.accept(media='text/plain')
    @cherrypy.tools.json_out()
    def GET(self):
        """
        This method return a JSON object of all customer's carts
        :return:
        '{"1": ["test", "test2"]}'

        where:
            "1" - customer's id
            ["test", "test2"] - list of product's skus added to the customer's cart
        """
        conn = _engine.connect()
        res = conn.execute("SELECT * FROM cart").fetchall()
        carts = {}
        for item in res:
            if item[0] in carts.keys():
                carts[item[0]].append(item[1])
            else:
                carts[item[0]] = [item[1]]
        return carts

    @cherrypy.tools.accept(media='text/plain')
    @cherrypy.tools.json_out()
    def PUT(self):
        """
        This method inserts a product to the customer's cart if
        customer's id and product's sku is present in the database
        :input:
        data = {
            'customer_id': '1', - customer's id
            'sku': 'test' - product's sku
        }
        :return:
        res = {
            'success': False, - was insertion successful
            'error': "", - error message
            'data': data - original data
        }
        """
        cl = cherrypy.request.headers['Content-Length']
        raw_body = cherrypy.request.body.read(int(cl))
        res = {
            'success': False,
            'error': "",
            'data': None
        }
        try:
            data = json.loads(raw_body)
            res['data'] = data
        except:
            res['error'] = "Can not parse json"
            return res

        conn = _engine.connect()
        customer_id = conn.execute("SELECT rowid FROM customer WHERE rowid={0}".format(data['customer_id'])).fetchone()
        if not customer_id:
            res['error'] = "Can not find customer with this id"
            conn.close()
            return res
        product_id = conn.execute("SELECT rowid FROM product WHERE sku='{0}'".format(data['sku'])).fetchone()
        if not product_id:
            res['error'] = "Can not find product with this id"
            conn.close()
            return res
        item_id = conn.execute("SELECT rowid FROM cart WHERE customer_id='{0}' and product_id='{1}'"
                               .format(data['customer_id'], data['sku'])).fetchone()
        if item_id:
            res['error'] = "This item already in the cart"
            conn.close()
            return res
        conn.execute("INSERT INTO cart VALUES ('{0}', '{1}')".format(data['customer_id'], data['sku']))
        res['success'] = True
        conn.close()

        return res

    @cherrypy.tools.accept(media='text/plain')
    @cherrypy.tools.json_out()
    def DELETE(self, customer_id, product_id):
        """
        This method removes a product from the customer's cart
        :param customer_id: customer's id
        :param product_id: product's sku
        :return:
         res = {
            'success': False, - was deletion successful or not
            'error': "", - error message
            'data': (customer_id, product_id) - customer's and product's ids
        }
        """
        res = {
            'success': False,
            'error': "",
            'data': (customer_id, product_id)
        }
        if customer_id and product_id:
            conn = _engine.connect()
            n = conn.execute("DELETE FROM cart WHERE customer_id='{0}' AND product_id='{1}'"
                             .format(customer_id, product_id)).rowcount
            if n:
                res['success'] = True
            else:
                res['error'] = "Can not delete"
            conn.close()
        else:
            res['error'] = "Either customer_id or product_id or both weren't passed"

        return res


def setup_database():
    """
    Create the `product`, 'customer' and 'cart' tables in the database
    on server startup
    """

    conn = _engine.connect()
    conn.execute("CREATE TABLE product (sku, description)")
    conn.execute("CREATE TABLE customer (first_name, last_name)")
    conn.execute("CREATE TABLE cart (customer_id, product_id)")
    conn.close()


def cleanup_database():
    """
    Destroy the `product`, 'customer' and 'cart' tables from the database
    on server shutdown.
    """

    conn = _engine.connect()
    conn.execute("DROP TABLE product")
    conn.execute("DROP TABLE customer")
    conn.execute("DROP TABLE cart")
    conn.close()


if __name__ == "__main__":
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.engine.subscribe('start', setup_database)
    cherrypy.engine.subscribe('stop', cleanup_database)

    cherrypy.tree.mount(SKU(), '/{0}/sku'.format(SECURE_STRING), conf)
    cherrypy.tree.mount(Customer(), '/{0}/customer'.format(SECURE_STRING), conf)
    cherrypy.tree.mount(Cart(), '/{0}/cart'.format(SECURE_STRING), conf)

    cherrypy.engine.start()
    cherrypy.engine.block()
