{
    'name': 'Sale Order Add Pallets And Lumps',
    'summary': """Añade los campos numericos palets y bultos al pedido de venta""",
    'version': '12.0.1.0.0',
    'description': """Añade los campos numericos palets y bultos al pedido de venta""",
    'author': 'Dani Domínguez',
    'company': 'Xtendoo',
    'website': 'http://xtendoo.es',
    'category': 'Sale Tools',
    'depends': [
        'base',
        'sale',
        ],
    'license': 'AGPL-3',
    'data': [
        'views/sale_order_view.xml',

    ],
    'installable': True,
    'auto_install': True,
}
