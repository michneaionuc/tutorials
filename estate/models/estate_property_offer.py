from odoo import models, fields, api
from datetime import timedelta


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
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", 
                                compute="_compute_date_deadline",
                                inverse="_inverse_date_deadline", store=True)
    property_id = fields.Many2one("estate.property",
                                  required=True,
                                  readonly=True)

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                create_date = record.create_date.date()
                record.validity = (record.date_deadline - create_date).days
            else:
                create_date = fields.Date.today()
                record.validity = (record.date_deadline - create_date).days

    def action_accept_offer(self):
        for offer in self:
            offer.status = "accepted"
            offer.property_id.partner_id = offer.partner_id
            offer.property_id.selling_price = offer.price

            other_offers = self.search([('property_id', '=', offer.property_id.id), ('id', '!=', offer.id)])
            other_offers.write({"status":"refused"})
        return True

    def action_refuse_offer(self):
        for offer in self:
            offer.status = "refused"
            offer.property_id.partner_id = None
            offer.property_id.selling_price = None
        return True
