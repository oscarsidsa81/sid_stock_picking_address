# -*- coding: utf-8 -*-
{
    "name": "sid_stock_picking_address",
    "version": "15.0.1.0.0",
    "category": "Inventory",
    "summary": "Modulariza la direccion de entrega en stock.picking y su uso en el reporte batch.",
    "author": "oscarsidsa81",
    "license": "LGPL-3",
    "depends": [
        "stock",
        "stock_picking_batch",
    ],
    "data": [
        "views/stock_picking_views.xml",
        "views/stock_picking_batch_report.xml",
    ],
    "installable": True,
    "application": False,
}
