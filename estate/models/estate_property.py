from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
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
    best_price = fields.Float(string="Best Offer",
                              compute="_compute_best_price")
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
    total_area = fields.Float(compute="_compute_total_area",
                              string="Total Area (sqm)")
    status = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        string="Status",
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

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'A property expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'A property selling price must be positive')
    ]


    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                best_price = 0
                for offer_record in record.offer_ids:
                    if offer_record.price > best_price:
                        best_price = offer_record.price
                record.best_price = best_price

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for property in self:
            min_price = 0.9 * property.expected_price
            if (float_compare(property.selling_price, min_price, precision_rounding=0.01) < 0 and 
                    not float_is_zero(property.selling_price, precision_rounding=0.01)):
                raise ValidationError("The selling price cannot be lower than 90% of the expected price.")

    def action_set_sold(self):
        for record in self:
            if record.status == 'canceled':
                raise UserError("Canceled properties cannot be sold.")
            record.status = "sold"
        return True

    def action_set_cancel(self):
        for record in self:
            if record.status == 'sold':
                raise UserError("Sold properties cannot be canceled.")
            record.status = "canceled"
        return True
