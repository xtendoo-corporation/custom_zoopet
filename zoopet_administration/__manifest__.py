{
    'name': 'Zoopet Administration',
    'summary': """Administration settings for Zoopet""",
    'version': '12.0.1.0.0',
    'description': """Administration settings for Zoopet""",
    'author': 'Dani Domínguez',
    'company': 'Xtendoo',
    'website': 'http://xtendoo.es',
    'category': 'Admin Tools',
    'depends': [
        'base',
        'sale',
        'product',
        'sale_order_picking_all_done',
        'res_partner_hide_internal_notes',
        'crm',
        'stock',
        'delivery',
        'mrp',
        'account',
    ],
    'license': 'AGPL-3',
    'data': [
        'views/sale_order_views.xml',
        'views/account_invoice_view.xml',
        'views/mrp_bom_view.xml',
        'views/permission_to_archive_view.xml',
        'views/sale_order_type_views.xml',
        'security/security_group.xml',

    ],
    'installable': True,
    'auto_install': True,
}
