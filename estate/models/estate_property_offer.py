from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "An offer containing the price, partner and the status"
    _order = "price desc"

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
    
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
         'An offer price must be strictly positive')
    ]

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    @api.model_create_multi 
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            offer_price = vals.get('price')
            if property_id:
                property_record = self.env['estate.property'].browse(property_id)
                existing_offers = self.search([('property_id', '=', property_id)])
                if existing_offers:
                    highest_offer = max(existing_offers.mapped('price'))
                    if offer_price <= highest_offer:
                        raise ValidationError(f"An existing offer of {highest_offer} is higher than or equal to the new offer price {offer_price}.")
                property_record.status = 'offer_received'

        return super(EstatePropertyOffer, self).create(vals_list)

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
            other_offers = self.search([('property_id', '=', offer.property_id.id), ('id', '!=', offer.id), ('status', '=', 'accepted')])
            if other_offers:
                raise ValidationError("There is already an accepted offer for this property.")
            offer.status = "accepted"
            offer.property_id.partner_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.status = 'offer_accepted'

            return True

    def action_refuse_offer(self):
        for offer in self:
            offer.status = "refused"
            offer.property_id.partner_id = None
            offer.property_id.selling_price = None
        return True
