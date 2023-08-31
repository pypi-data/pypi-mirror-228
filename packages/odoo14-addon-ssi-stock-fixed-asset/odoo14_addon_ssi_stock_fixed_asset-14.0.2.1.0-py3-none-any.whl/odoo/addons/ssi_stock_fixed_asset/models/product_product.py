# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = ["product.product"]

    fixed_asset_category_id = fields.Many2one(
        string="Fixed Asset Category",
        comodel_name="fixed.asset.category",
    )
    auto_create_fixed_asset = fields.Boolean(
        string="Auto Create Fixed Asset",
        default=False,
    )
