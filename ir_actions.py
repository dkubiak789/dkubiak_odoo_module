# -*- coding: utf-8 -*-

import time
import base64
from openerp.osv import fields, osv


##
# Actions that are run on the server side
#
class actions_server(osv.osv):
    _inherit = 'ir.actions.server'

    _columns = {
        'email_template_id':fields.many2one('email.template', 'Email Template'),
        'state': fields.selection([
            ('client_action','Client Action'),
            ('dummy','Dummy'),
            ('loop','Iteration'),
            ('code','Python Code'),
            ('trigger','Trigger'),
            ('email','Email'),
            ('template','Email Template'),
            ('sms','SMS'),
            ('object_create','Create Object'),
            ('object_copy','Copy Object'),
            ('object_write','Write Object'),
            ('other','Multi Actions'),
        ], 'Action Type', required=True, size=32, help="Type of the Action that is to be executed"),
        }


    def _get_sale_order_xml(self, cr, uid, ids, context=None):
        """Create xml content for Sale Order
        """
        if context is None:
            context = {}

        sale_order_obj = self.pool.get('sale.order').browse(cr, uid, context['active_id'], context)
        return """
        <record id="sale_order_{sale_order_id}" model="sale.order">
            <field name="partner_id">{partner_id}</field>
            <field name="partner_invoice_id">{partner_invoice_id}</field>
            <field name="partner_shipping_id">{partner_shipping_id}</field>
            <field name="shop_id">{shop_id}</field>
            <field name="user_id">{user_id}</field>
            <field name="pricelist_id">{pricelist_id}</field>
            <field name="order_policy">{order_policy}</field>
        </record>
        """.format(
            sale_order_id = sale_order_obj.id or None,
            partner_id = sale_order_obj.partner_id.id or None,
            partner_invoice_id = sale_order_obj.partner_invoice_id.id or None,
            partner_shipping_id = sale_order_obj.partner_shipping_id.id or None,
            shop_id = sale_order_obj.shop_id.id or None,
            user_id = sale_order_obj.user_id.id or None,
            pricelist_id = sale_order_obj.pricelist_id.id or None,
            order_policy = sale_order_obj.order_policy or None,
        )


    def _create_xml(self, cr, uid, ids, context=None):
        """Create encoded xml content
        """
        if context is None:
            context = {}

        xml_records = ''

        # add more records for other models
        if context['active_model'] == 'sale.order':
            xml_records = self._get_sale_order_xml(cr, uid, ids, context)

        if not xml_records:
            return False

        xml = """
<?xml version="1.0"?>
<openerp>
    <data>
        {xml_records}
    </data>
</openerp>
        """.format(xml_records=xml_records)
        return base64.b64encode(xml)


    def run(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        result = False

        user = self.pool.get('res.users').browse(cr, uid, uid)
        for action in self.browse(cr, uid, ids, context):
            obj = None
            obj_pool = self.pool.get(action.model_id.model)
            if context.get('active_model') == action.model_id.model and context.get('active_id'):
                obj = obj_pool.browse(cr, uid, context['active_id'], context=context)
            cxt = {
                'self': obj_pool,
                'object': obj,
                'obj': obj,
                'pool': self.pool,
                'time': time,
                'cr': cr,
                'context': dict(context), # copy context to prevent side-effects of eval
                'uid': uid,
                'user': user
            }
            expr = eval(str(action.condition), cxt)
            if not expr:
                continue

            # send templates with xml attachment
            if action.state == 'template':

                # send_mail is overwritten to send email with attachment
                encoded_xml = self._create_xml(cr, uid, ids, context)
                if encoded_xml:
                    context['attachments'] = [[obj.name, encoded_xml]]

                # send email with attachment
                actions_server_obj = self.pool.get('ir.actions.server').browse(cr, uid, ids[0])
                template_id = actions_server_obj.email_template_id.id
                result = self.pool.get('email.template').send_mail(cr, uid, template_id, context['active_id'], force_send=True, context=context)

            # call parent function
            super(actions_server, self).run(cr, uid, ids, context)
        return result
