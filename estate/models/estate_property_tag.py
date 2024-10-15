from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "A list of tags shortly describing the property: cozy, renovated, etc."
    _order = "name"

    name = fields.Char()
    color = fields.Integer()

    _sql_constraints = [
        ('check_tag_name', 'unique(name)',
         'A property tag name must be unique')
    ]
