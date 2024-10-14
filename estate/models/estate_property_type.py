from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property: House, Apartment, etc."

    name = fields.Char(required=True)
