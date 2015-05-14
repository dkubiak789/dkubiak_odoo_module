# -*- coding: utf-8 -*-
{
    'name': 'Example Odoo Module by Dariusz Kubiak',
    'version': '1.0',
    'author': 'Dariusz Kubiak',
    'category': 'Sales Management',
    'description': """
Main features:
--------------
* Send notification of a Sales Orders status to Customer
* Creates VIP Partner model

If you create Sale Order and you select Create Invoice: 'On Delivery Order' or 'Before Delivery'. Then you confirm the sale, the Sale Order receives 'Sale Order' status and the Notification email will be send to the Customer.

VIP Partner is a simple example of model with tree and form views.
""",
    'website': 'http://www.openerp.com',
    'depends': ['sale', 'base_action_rule'],
    'data': [
        'sale_action_rules.xml',
        'vip_partner.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
