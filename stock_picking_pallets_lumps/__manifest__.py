{
    'name': 'Stock Picking Add Pallets And Lumps',
    'summary': """Añade los campos numericos palets y bultos al albarán""",
    'version': '12.0.1.0.0',
    'description': """Añade los campos numericos palets y bultos al albarán""",
    'author': 'Dani Domínguez',
    'company': 'Xtendoo',
    'website': 'http://xtendoo.es',
    'category': 'stock Tools',
    'depends': [
        'base',
        'stock',
        ],
    'license': 'AGPL-3',
    'data': [
        'views/stock_picking_view.xml',

    ],
    'installable': True,
    'auto_install': True,
}
