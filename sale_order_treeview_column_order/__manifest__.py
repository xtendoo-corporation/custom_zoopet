# -*- coding: utf-8 -*-



{
    "name": "sale_order_treeview_column_order",
    "summary": """Orden de las columnas de sale pedidos y presupuestos de ventas""",
    "version": "13.0.1.0.2",
    "description": """Orden de las columnas de sale pedidos y presupuestos de ventas""",
    "author": "DDL-Xtendoo",
    "company": "Xtendoo",
    "website": "https://xtendoo.es/",
    "category": "Extra Tools",
    "depends": [
        "base",
        "sale",
        "zoopet_sale_order_tags",
        "sale_order_weight",
        "sale_order_tag",
        "sale_picking_state",
    ],
    "license": "AGPL-3",
    "data": [
        "views/sale_order_views.xml",
    ],
    "qweb": [
    ],
    "installable": True,
    "auto_install": False,
}
