# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMoveLine(models.Model):
    _name = "account.move.line"
    _inherit = ["account.move.line"]

    def _prepare_create_fixed_asset(self):
        _super = super(AccountMoveLine, self)
        result = _super._prepare_create_fixed_asset()
        if self._check_fixed_asset_inventory_integration():
            result.update(self._prepare_inventory_data())
        return result

    def _check_fixed_asset_inventory_integration(self):
        self.ensure_one()

        if not self.move_id.stock_move_id:
            return False

        stock_move = self.move_id.stock_move_id

        if not stock_move.product_id.auto_create_fixed_asset:
            return False

        if len(stock_move.move_line_ids) > 1:
            return False

        return True

    def _prepare_inventory_data(self):
        self.ensure_one()
        stock_move = self.move_id.stock_move_id
        product = stock_move.product_id
        stock_move_line = stock_move.move_line_ids[0]

        return {
            "product_id": product.id,
            "lot_id": stock_move_line.lot_id.id,
        }
