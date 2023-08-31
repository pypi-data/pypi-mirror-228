# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Inventory + Fixed Asset Integration",
    "version": "14.0.2.1.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_stock_account",
        "ssi_fixed_asset",
    ],
    "data": [
        "views/product_product_views.xml",
        "views/fixed_asset_asset_views.xml",
        "views/stock_production_lot_views.xml",
    ],
    "demo": [],
}
