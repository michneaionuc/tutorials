from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property: House, Apartment, etc."

    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_type_name', 'unique(name)',
         'A property type name must be unique')
    ]
