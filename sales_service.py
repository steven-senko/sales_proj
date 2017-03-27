import json

import cherrypy
from sqlalchemy import create_engine

SECURE_STRING = "fm7m67u44p"
DB_STRING = "sale.db"
_engine = create_engine('sqlite:///sale.db', echo=True)


@cherrypy.expose
class Customer(object):
    @cherrypy.tools.accept(media='text/plain')
    @cherrypy.tools.json_out()
    def PUT(self):
        cl = cherrypy.request.headers['Content-Length']
        raw_body = cherrypy.request.body.read(int(cl))
        data = json.loads(raw_body)
        res = {
            'success': False,
            'error': "",
            'data': data,
            'id': None
        }
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
        res = {
            'success': False,
            'error': "",
            'data': customer_id
        }

        conn = _engine.connect()
        conn.execute("DELETE FROM cart WHERE customer_id='{0}'".format(customer_id))
        n = conn.execute("DELETE FROM customer WHERE rowid='{0}'".format(customer_id)).rowcount
        if n:
            res['success'] = True
        else:
            res['error'] = "Can not delete"
        conn.close()

        return res


@cherrypy.expose
class SKU(object):
    @cherrypy.tools.accept(media='text/plain')
    @cherrypy.tools.json_out()
    def PUT(self):
        cl = cherrypy.request.headers['Content-Length']
        raw_body = cherrypy.request.body.read(int(cl))
        data = json.loads(raw_body)
        res = {
            'success': False,
            'error': "",
            'data': data
        }

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
        res = {
            'success': False,
            'error': "",
            'data': product_id
        }

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

        return res


@cherrypy.expose
class Cart(object):
    @cherrypy.tools.accept(media='text/plain')
    @cherrypy.tools.json_out()
    def GET(self):
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
        cl = cherrypy.request.headers['Content-Length']
        raw_body = cherrypy.request.body.read(int(cl))
        data = json.loads(raw_body)
        res = {
            'success': False,
            'error': "",
            'data': data
        }

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
        res = {
            'success': False,
            'error': "",
            'data': (customer_id, product_id)
        }

        conn = _engine.connect()
        n = conn.execute("DELETE FROM cart WHERE customer_id='{0}' AND product_id='{1}'"
                         .format(customer_id, product_id)).rowcount
        if n:
            res['success'] = True
        else:
            res['error'] = "Can not delete"
        conn.close()

        return res


def setup_database():
    """
    Create the `user_string` table in the database
    on server startup
    """

    conn = _engine.connect()
    conn.execute("CREATE TABLE product (sku, description)")
    conn.execute("CREATE TABLE customer (first_name, last_name)")
    conn.execute("CREATE TABLE cart (customer_id, product_id)")
    conn.close()


def cleanup_database():
    """
    Destroy the `user_string` table from the database
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
