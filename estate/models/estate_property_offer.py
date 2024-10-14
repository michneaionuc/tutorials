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
            # Check if create_date exists
            if record.create_date:
                # Convert create_date to date
                create_date = record.create_date.date()
                # Calculate validity based on create_date
                record.validity = (record.date_deadline - create_date).days
            else:
                # Fallback: assume today as create_date
                create_date = fields.Date.today()
                record.validity = (record.date_deadline - create_date).days
