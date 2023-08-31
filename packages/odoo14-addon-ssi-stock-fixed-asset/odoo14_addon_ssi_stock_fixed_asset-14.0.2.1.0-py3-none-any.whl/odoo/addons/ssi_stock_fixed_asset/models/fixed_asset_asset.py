# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class FixedAssetAsset(models.Model):
    _name = "fixed.asset.asset"
    _inherit = ["fixed.asset.asset"]

    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
    )
    lot_id = fields.Many2one(
        string="# Serial Number",
        comodel_name="stock.production.lot",
        compute="_compute_lot_id",
        inverse="_inverse_lot_id",
        store=True,
    )
    lot_ids = fields.One2many(
        string="Serial Numbers",
        comodel_name="stock.production.lot",
        inverse_name="fixed_asset_id",
    )
    inventory_state = fields.Selection(
        string="Inventory State",
        selection=[
            ("none", "No Link"),
            ("one", "Link to One Serial Number"),
            ("multiple", "Link to Multiple Serial Number"),
        ],
        compute="_compute_inventory_state",
        store=True,
    )

    @api.depends(
        "lot_ids",
        "lot_ids.fixed_asset_id",
        "lot_id",
    )
    def _compute_inventory_state(self):
        for record in self:
            result = "none"
            if len(record.lot_ids) == 1:
                result = "one"
            elif len(record.lot_ids) > 1:
                result = "multiple"
            record.inventory_state = result

    @api.depends(
        "lot_ids",
        "lot_ids.fixed_asset_id",
    )
    def _compute_lot_id(self):
        for record in self:
            result = False
            if len(record.lot_ids) == 1:
                result = record.lot_ids[0]
            record.lot_id = result

    def _inverse_lot_id(self):
        if self.lot_ids:
            self.lot_ids.fixed_asset_id = False
        self.lot_id.fixed_asset_id = self

    @api.onchange(
        "product_id",
    )
    def onchange_lot_id(self):
        self.lot_id = False
