# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# Copyright (C) 2016 MARLON FALCON HDEZ (<http://www.marlonfalcon.cl>).
# contact: contacto@marlonfalcon.cl

from odoo import fields, models, api, _
from datetime import datetime
from odoo.exceptions import UserError

class HotelWizard(models.TransientModel):
    _name = "hotel.wizard"
    doc_type = fields.Selection(
            [('D','RUT Chile'),
            ('P','Pasaportes'),
            ('C ','Permiso de conducir Chile '),
            ('I','Carta o documento de identidad'),
            ('X','Permiso de residencia UE'),
            ('N','Permiso de residencia Chile ')],
            'Tipo de Documento', size=1)
    
    @api.multi
    def set_call_my_def_wyzard(self):
        traveler_obj = self.env['traveler.register']
        travelers = traveler_obj.search([('doc_type','=',self.doc_type)])
        if not travelers:
            raise UserError(_('No exiten registros con ese tipo de documento'))
        traveler_ids = [x.id for x in travelers]
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('mfh_hotel_wizard.mfh_hotel_wizard_qweb_view')
        docargs = {
            'doc_ids': traveler_ids,
            'doc_model': report.model,
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'mfh_hotel_wizard.mfh_hotel_wizard_qweb_view',
            'datas': docargs,
            'nodestroy': True,
        }
        
