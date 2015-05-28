# -*- coding: utf-8 -*-

import logging
from openerp.osv import osv, fields
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

class sale_order(osv.osv):
    _inherit = 'sale.order'

    _columns = {
          'state': fields.selection([
            ('draft', 'Draft Quotation'),
            ('sent', 'Quotation Sent'),
            ('request_approval', 'Request Approval'),
            ('cancel', 'Cancelled'),
            ('waiting_date', 'Waiting Schedule'),
            ('progress', 'Sales Order'),
            ('manual', 'Sale to Invoice'),
            ('shipping_except', 'Shipping Exception'),
            ('invoice_except', 'Invoice Exception'),
            ('done', 'Done'),
            ], 'Status', readonly=True, track_visibility='onchange',
            help="Gives the status of the quotation or sales order.\
              \nThe exception status is automatically set when a cancel operation occurs \
              in the invoice validation (Invoice Exception) or in the picking list process (Shipping Exception).\nThe 'Waiting Schedule' status is set when the invoice is confirmed\
               but waiting for the scheduler to run on the order date.", select=True),
        }

    def action_button_request(self, cr, uid, ids, context=None):
        """Send request to the manager to approve the Sale Order or Quotation
        """

        # get the user's manager_id to send him request for Sale Order approval email

        # user_id = self.pool.get('res.users').browse(cr, uid, uid, context).id
        emp_obj = self.pool.get('hr.employee')
        # emp_id = emp_obj.search(cr, uid, [('user_id', '=', user_id)], context=context)[0]

        emp_id = emp_obj.search(cr, uid, [('user_id', '=', uid)], context=context)[0]
        manager_obj = emp_obj.browse(cr, uid, emp_id, context).parent_id
        if not manager_obj:
            raise osv.except_osv(_('No Manager Defined!'),_("You must first have your manager assigned to send thim the request!") )

        manager_id = manager_obj.user_id.partner_id.id

        # add the the manager id to the recipient list in context
        context['recipient_ids'] = [manager_id]

        try:
            ir_model_data = self.pool.get('ir.model.data')
            template_id = ir_model_data.get_object_reference(cr, uid, 'dkubiak_odoo_module', 'sale_order_approval_request')[1]
            # template_id = 14
            _logger.debug("action_button_request() template_id=%s, ids=%s, context=%s" % (template_id, ids, context))
            self.pool.get('email.template').send_mail(cr, uid, template_id, ids[0], force_send=True, context=context)
        except ValueError:
            pass

        self.write(cr, uid, ids, {'state': 'request_approval'})

        return True


    # def action_request_send(self, cr, uid, ids, context=None):
    #     _logger.info("action_request_send() >>>")

sale_order()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
