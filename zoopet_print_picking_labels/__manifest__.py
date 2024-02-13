# -*- coding: utf-8 -*-
{
    "name": "Zoopet print picking labels",
    "summary": """Imprimir etiquetas en el icking""",
    "version": "13.0.1.0.2",
    "description": """FImprimir etiquetas en el icking""",
    "author": "DDL-Xtendoo",
    "company": "Xtendoo",
    "website": "https://xtendoo.es/",
    "category": "Extra Tools",
    "depends": [
        "document_format_zoopet",
        "product"
    ],
    "license": "AGPL-3",
    "data": [
        "views/stock_move_line_views.xml",
        "views/product_template_views.xml",
        "views/print_product_labels_2_5_x_3_8.xml",
        "views/print_product_labels_5_x_10.xml",
        "views/labels/label_template_2_5_x_3_8.xml",
        "views/labels/label_template_5_x_10.xml"
    ],
    "installable": True,
    "auto_install": False,
}
