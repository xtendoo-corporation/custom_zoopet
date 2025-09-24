# -*- coding: utf-8 -*-



{
    "name": "Import internal transfers",
    "summary": """Import internal transfers""",
    "version": "15.0.2.2.0",
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
        "security/ir.model.access.csv",
        "wizard/internal_transfer_import_wizard.xml",
        #"views/stock_views.xml",
    ],

    "installable": True,
    "auto_install": False,
}
