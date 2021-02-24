# -*- coding: utf-8 -*-

{
    "name": "document_format_Zoopet",
    "summary": """Formatos de documentos Zoopet""",
    "version": "12.0.1.0.0",
    "description": """Formatos de documentos Zoopet""",
    "author": "DDL",
    "company": "Xtendoo",
    "website": "http://www.xtendoo.com",
    "category": "Extra Tools",
    "depends": [
        "base",
        "account",
        "sale",
        "web",
        "stock",
        "product",
        "zoopet_sale_global_discount",
        "zoopet_administration",
        "stock_picking_and_sale_order_pallets_and_lumps",
        "pos_margin",
        "sale_margin",
        "product_brand",
        "stock_picking_report_valued",
    ],
    "license": "AGPL-3",
    "data": [
        # layout
        "views/layout/external_layout_clean.xml",
        # delivery
        "views/delivery/report_delivery_document_without_price.xml",
        "views/delivery/report_delivery_document_valued.xml",
        # sale_order
        "views/sale/report_saleorder_document.xml",
        "views/sale/sale_without_price.xml",
        # Purchase_order
        "views/purchase/report_purchaseorder_document.xml",
        # Invoice
        "views/invoice/report_invoice_document.xml",
        "views/invoice/report_invoice.xml",
        # Product Label
        "views/product_label/paper_format.xml",
        "views/product_label/label_template.xml",
        #Albarán en pedidos
        "views/sale_delivery/sale_delivery_without_price.xml",
        "views/sale_delivery/sale_delivery.xml",

        #Res_Partner
        "views/res_partner/res_partner_view.xml",


    ],
    "demo": [],
    "installable": True,
    "auto_install": False,
}
