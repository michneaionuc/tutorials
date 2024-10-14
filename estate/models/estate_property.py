from odoo import models, fields
from datetime import datetime, timedelta


class Property(models.Model):
    _name = "estate.property"
    _description = "Property details"

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    tag_ids = fields.Many2many("estate.property.tag",
                               string="Property Tags",
                               required=True)
    type_id = fields.Many2one("estate.property.type",
                              string="Property Type")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Availability Date",
        default=lambda self: datetime.today() + timedelta(days=90),
        copy=False
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price",
                                 readonly=True,
                                 copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation"
    )
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        string="State",
        required=True,
        copy=False,
        default='new'
    )
    active = fields.Boolean(string="Active", default=True)
    offer_ids = fields.One2many("estate.property.offer",
                                "property_id",
                                string="Offers")
    user_id = fields.Many2one('res.users', string="Salesman",
                              default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string="Buyer", copy=False)
