from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "An offer containing the price, partner and the status"

    price = fields.Float(string="Price")
    partner_id = fields.Many2one("res.partner",
                                 string="Partner",
                                 required=True)
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ],
        copy=False,
        string="Status"
    )
    property_id = fields.Many2one("estate.property",
                                  required=True,
                                  readonly=True)
