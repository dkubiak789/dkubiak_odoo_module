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
* Sale Order workflow with Approval Request
* Creates VIP Partner model

If you create Sale Order and you select Create Invoice: 'On Delivery Order' or 'Before Delivery'. Then you confirm the sale, the Sale Order receives 'Sale Order' status and the Notification email will be send to the Customer.

Sales person has no right to comfirm Sale Order. There is new Request Approval button to send email to the manager to confirm the Sale.

VIP Partner is a simple example of model with tree and form views.
""",
    'website': 'http://www.openerp.com',
    'depends': ['sale_stock', 'base_action_rule'],
    'data': [
        'email_template.xml',
        'sale_action_rules.xml',
        'sale_view.xml',
        'sale_workflow.xml',
        'vip_partner.xml',
        'ir_actions.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
