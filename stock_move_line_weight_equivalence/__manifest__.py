{
    'name': 'Stock move line weight equivalence',
    'summary': """Añade un campo calculado en stock_move_line, con la equivalencia del campo qty_done en kg""",
    'version': '13.0.1.0.0',
    'description': """Añade un campo calculado en stock_move_line, con la equivalencia del campo qty_done en kg""",
    'author': 'Dani Domínguez',
    'company': 'Xtendoo',
    'website': 'http://xtendoo.es',
    'category': 'stock Tools',
    'depends': [
        'base',
        'stock'
        ],
    'license': 'AGPL-3',
    'data': [
        'views/stock_move_line_views.xml',

    ],
    'installable': True,
    'auto_install': True,
}
