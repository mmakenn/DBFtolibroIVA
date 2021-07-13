# -*- coding: utf-8 -*-

from invoice import *
from string import Template 
import os

'''************************************************************************'''
'''                                 FORMATS                                '''
'''************************************************************************'''
INVOICEFILE = {'PURCHASES': Template('COMPRAS_COMPROBANTES${period}.txt'),
                'SALES': Template('VENTAS_COMPROBANTES${period}.txt')}

ALIQUOTFILE = {'PURCHASES': Template('COMPRAS_${period}.txt'),
                'SALES': Template('VENTAS_${period}.txt')}

INVOICEFORMAT = Template('${field1}${field2}${field3}${field4}${field5}' +
                         '${field6}${field7}${field8}${field9}${field10}' +
                         '${field11}${field12}${field13}${field14}' + '0' * 30 +
                         'PES0001' + '0' * 6 + '${field19}' + ' ' + '${field21}')
# En compras field5=" "*16 en ventas field5=field4
# En compras field11=exento field12=perciva en ventas field11=perciva field12=exento
# En compras field21=CF field22=0*30+30*" "+0*15 en ventas  field21=0*15 field22=0*8

ALIQUOTFORMAT = Template('${field1}${field2}${field3}${field4}${field5}' +
                         '${field6}${field7}${field8}')
# En VENTAS field4=field5=""

'''************************************************************************'''
'''                                   AUX                                  '''
'''************************************************************************'''
def assignDocCode(cuit):
    '''
    

    Parameters
    ----------
    cuit : TYPE
        DESCRIPTION.

    Returns
    -------
    str
        DESCRIPTION.

    '''
    if cuit == 0:
        return '99'
    if len(str(cuit)) == 11:
        return '80'
    else:
        return '96'
    
'''************************************************************************'''
'''                                  SAVE                                  '''
'''************************************************************************'''
def saveData(invoices, invoicesType, period):
    period = period.rstrip('/', '')
    
    path = os.getcwd()
    invoiceFilename = path + INVOICEFILE[invoicesType].substitute(period = period)
    aliquotFilename = path + ALIQUOTFILE[invoicesType].substitute(period = period)
    
    finished = False
    while not finished:
        invoiceFile = open(invoiceFilename, 'a')
        aliquotFile = open(aliquotFilename, 'a')
        
        if invoiceFile and aliquotFile:
            for invoice in invoices:
                date = invoice.getDate()
                itype = invoice.getType()
                pv, num = invoice.getID()[0], invoice.getID()[1]
                cuit = invoice.getCUIT()  #20char
                docType = assignDocCode(cuit)
                name = invoice.getName() #30char
                total = invoice.getTotal() #normalize . , 15
                cng = invoice.getCNG()  #normalize . , 15
                exempt = invoice.getExempt()  #normalize . , 15
                pVat, pIncome, pGross = income.getTaxes()[0], income.getTaxes()[1], income.getTaxes()[2]  #normalize . , 15
                vats = invoice.getVats()
                
                if invoicesType == 'SALES':
                    fieldInvoice5 = num
                    fieldInvoice21 = '0' * 23
                else:
                    fieldInvoice5 = ' ' * 16
                    fieldInvoice21 = vatTotal + '0' * 26 + ' ' * 30 + '0' * 15
    