# -*- coding: utf-8 -*-



{
    "name": "Global discount readonly",
    "summary": """Convierte en readonly y oculta el campo global discount en ventas, facturas y contactos""",
    "version": "13.0.1.0.2",
    "description": """Convierte en readonly y oculta el campo global discount en ventas, facturas y contactos""",
    "author": "DDL-Xtendoo",
    "company": "Xtendoo",
    "website": "https://xtendoo.es/",
    "category": "Extra Tools",
    "depends": [
        "base_global_discount",
        "sale_global_discount",
        "account_global_discount",
    ],
    "license": "AGPL-3",
    "data": [
        "views/sale_order_view.xml",
        "views/account_move_view.xml",
        "views/res_partner_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
