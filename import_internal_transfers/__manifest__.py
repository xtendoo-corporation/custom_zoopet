# -*- coding: utf-8 -*-



{
    "name": "Import internal transfers",
    "summary": """Import internal transfers""",
    "version": "13.0.1.0.2",
    "description": """Import internal transfers""",
    "author": "Dani Domínguez",
    "company": "Xtendoo",
    "website": "https://xtendoo.es/",
    "category": "Extra Tools",
    "depends": [
        "base",
        "stock",
    ],
    "license": "AGPL-3",
    "data": [
        "wizard/internal_transfer_import_wizard.xml",
        "views/stock_views.xml",
    ],

    "installable": True,
    "auto_install": False,
}
