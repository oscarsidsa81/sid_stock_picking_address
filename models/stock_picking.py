from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    sid_direccion = fields.Text(
        string="Dirección de entrega",
        compute="_compute_sid_direccion",
        readonly=True,
        store=False,
    )

    @api.depends(
        "partner_id",
        "partner_id.street",
        "partner_id.street2",
        "partner_id.city",
        "partner_id.state_id",
        "partner_id.zip",
    )
    def _compute_sid_direccion(self):
        for picking in self:
            partner = picking.partner_id
            if not partner:
                picking.sid_direccion = ""
                continue

            address_parts = [
                partner.street or "",
                partner.street2 or "",
                partner.city or "",
                partner.state_id.name or "",
                partner.zip or "",
            ]
            picking.sid_direccion = "\n".join(
                part for part in address_parts if part
            )
