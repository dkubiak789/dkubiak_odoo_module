# -*- coding: utf-8 -*-
"""
VIP Partner is a simple example of model with tree and form views.
"""

from openerp.osv import osv, fields

class vip_partner(osv.osv):
    _description = 'VIP Partner'
    _name = 'vip.partner'

    _columns = {
        'first_name': fields.char('First Name', size=128, required=True),
        'last_name': fields.char('Last Name', size=128, required=True),
        'birth_date': fields.date('Date of Birth'),
        'active': fields.boolean('Active', help="Allows you to hide the VIP Partner without removing it."),
        }
    _order = "first_name"
    _defaults = {
        'active': 1,
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
