{
    'name': 'Zoopet Sale Order Tags',
    'summary': """Añade etiqueta de ventas en la vista de pedidos""",
    'version': '12.0.1.0.0',
    'description': """Añade etiqueta de ventas en la vista de pedidos""",
    'author': 'Dani Domínguez',
    'company': 'Xtendoo',
    'website': 'http://xtendoo.es',
    'category': 'Sale Tools',
    'depends': [
        'crm',
        'sale',
        'sale_order_tag',
        ],
    'license': 'AGPL-3',
    'data': [
        'views/sale_oder_view.xml',

    ],
    'installable': True,
    'auto_install': True,
}
