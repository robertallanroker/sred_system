{
    "name" : "Product Image",
    "version" : "0.1",
    "author" : "Stefan Reisich, Rove.design GmbH",
    "website" : "http://www.rove.de/",
    "description": """
This Module overwrites openerp.web.list.Binary field to show the product image in the listview. A new column with product image is added.
    """,
    "depends" : [
                 "sale",
                 "sale_stock",
                 "stock"
    ],
    "data": [
        'views/product_view.xml',
        'views/sale_view.xml',
        'views/stock_view.xml'
    ],
    'installable': True,
    "active": False,
}
