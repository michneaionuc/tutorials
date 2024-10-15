from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of property: House, Apartment, etc."
    _order = "name"

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order property types")
    property_ids = fields.One2many(
        'estate.property', 
        'type_id', 
        string="Properties"
    )

    _sql_constraints = [
        ('check_type_name', 'unique(name)',
         'A property type name must be unique')
    ]
