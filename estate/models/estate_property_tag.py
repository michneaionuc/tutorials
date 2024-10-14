from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "A list of tags shortly describing the property: cozy, renovated, etc."

    name = fields.Char()

    _sql_constraints = [
        ('check_tag_name', 'unique(name)',
         'A property tag name must be unique')
    ]
