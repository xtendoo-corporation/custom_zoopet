# -*- coding: utf-8 -*-



{
    "name": "document_format_Zoopet",
    "summary": """Formatos de documentos Zoopet""",
    "version": "12.0.1.0.0",
    "description": """Formatos de documentos Zoopet""",
    "author": "DDL-Xtendoo",
    "company": "Xtendoo",
    "website": "https://xtendoo.es/",
    "category": "Extra Tools",
    "depends": [
        "base",
        "account",
        "sale",
        "web",
        "stock",
        "product",
        "sale_global_discount",
        "account_global_discount",
        "zoopet_administration",
        "stock_picking_and_sale_order_pallets_and_lumps",
        "pos_margin",
        "sale_margin",
        "product_brand",
        "stock_picking_report_valued",
        "point_of_sale",
        "account_invoice_report_grouped_by_picking",
        "zoopet_administration",
        "website",
        "website_sale",
        "zoopet_sale_order_tags",
        "l10n_es_partner",
        "purchase",
        "account_invoice_date_due",
        'stock_picking_all_done',
        'sale_order_picking_all_done',
    ],
    "license": "AGPL-3",
    "data": [
        # layout
        "views/layout/external_layout_clean.xml",
        # delivery
        "views/delivery/report_delivery_document_without_price.xml",
        "views/delivery/report_delivery_document_valued.xml",
        # delivery Labels
        "views/delivery_print_labels/report_label_25_x_38.xml",
        "views/delivery_print_labels/report_label_50_x_100.xml",
        # sale_order
        "views/sale/report_saleorder_document.xml",
        "views/sale/sale_without_price.xml",
        # Purchase_order
        "views/purchase/report_purchaseorder_document.xml",
        # Invoice
        "views/invoice/report_invoice_document.xml",
        "views/invoice/report_invoice.xml",
        # Invoice Agrupada
        "views/invoice/report_invoice_grouped_document.xml",
        "views/invoice/report_invoice_grouped.xml",
        #Invoice Agrupada - NO USAR
        "views/invoice/report_invoice_grouped_document_no_usar.xml",
        "views/invoice/report_invoice_grouped_no_usar.xml",
        #Invoice - NO USAR
        "views/invoice/report_invoice_document_no_usar.xml",
        "views/invoice/report_invoice_no_usar.xml",
        # Product Label
        "views/product_label/paper_format.xml",
        "views/product_label/label_template.xml",
        #Albarán en pedidos
        "views/sale_delivery/sale_delivery_without_price.xml",
        "views/sale_delivery/sale_delivery.xml",

        #"views/sale_delivery/sale_delivery_delivered_qty.xml",

        #Res_Partner
        "views/res_partner/res_partner_view.xml",

        #Añadir JS del POS
        "templates/assets.xml",


    ],
    "qweb": [
        "static/src/xml/pos.xml",
    ],
    "installable": True,
    "auto_install": False,
}
