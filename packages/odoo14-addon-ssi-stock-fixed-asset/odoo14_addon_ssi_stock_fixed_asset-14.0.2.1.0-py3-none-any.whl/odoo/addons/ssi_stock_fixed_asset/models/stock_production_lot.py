# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockProductionLot(models.Model):
    _name = "stock.production.lot"
    _inherit = ["stock.production.lot"]

    fixed_asset_id = fields.Many2one(
        string="Fixed Assets",
        comodel_name="fixed.asset.asset",
    )
