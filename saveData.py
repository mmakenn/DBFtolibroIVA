# -*- coding: utf-8 -*-

from invoice import *
from string import Template 
import os

'''************************************************************************'''
'''                                 FORMATS                                '''
'''************************************************************************'''
INVOICEFILE = {'PURCHASES': Template('/${period}COMPRAS_COMPROBANTES.txt'),
                'SALES': Template('/${period}VENTAS_COMPROBANTES.txt')}

ALIQUOTFILE = {'PURCHASES': Template('/${period}COMPRAS_ALICUOTAS.txt'),
                'SALES': Template('/${period}VENTAS_ALICUOTAS.txt')}

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
    
def calcVatTotal(vats):
    total = 0
    for vat in vats:
        total = total + vats[vat][1]
    return round(total, 2)

def normalize(parameter, characters, ptype = float):
    if ptype == str:
        return parameter + ' ' * (characters - len(parameter))
    
    parameter = str(parameter)
    if ptype == float:
        if not ('.' in parameter):
            parameter = parameter + '00'
        elif parameter.index('.') + 2 == len(parameter):
            parameter = parameter + '0'
    parameter = parameter.replace('.', '').replace(',', '').replace('-', '')
    return (characters - len(parameter)) * '0' + parameter
    
'''************************************************************************'''
'''                                  SAVE                                  '''
'''************************************************************************'''
def saveData(invoices, invoicesType, period, path):
    # path = os.getcwd()
    # path = path.replace('\dist\interface', '')
    invoiceFilename = path + INVOICEFILE[invoicesType].substitute(period = period)
    aliquotFilename = path + ALIQUOTFILE[invoicesType].substitute(period = period)
    
    invoiceFile = open(invoiceFilename, 'w')
    aliquotFile = open(aliquotFilename, 'w')
    
    if invoiceFile and aliquotFile:
        for invoice in invoices:
            date = invoice.getDate()
            itype = invoice.getType()
            pv, num = invoice.getID()[0], invoice.getID()[1]
            cuit = invoice.getCUIT()
            docType = assignDocCode(cuit)
            cuit = normalize(cuit, 20, 'cuit')
            name = normalize(invoice.getName(), 30, str)         
            total = normalize(invoice.getTotal(), 15)            
            cng = normalize(invoice.getCNG(), 15)             
            exempt = normalize(invoice.getExempt(), 15)            
            pVat = normalize(invoice.getTaxes()[0], 15)  
            pIncome = normalize(invoice.getTaxes()[1], 15)  
            pGross = normalize(invoice.getTaxes()[2], 15)
            
            vats = invoice.getVats()
            
            if invoicesType == 'SALES':
                fieldInvoice5 = num
                fieldInvoice11 = pVat
                fieldInvoice12 = exempt
                fieldInvoice21 = '0' * 23
            else:
                fieldInvoice5 = ' ' * 16
                fieldInvoice11 = exempt
                fieldInvoice12 = pVat
                vatTotal = calcVatTotal(vats)
                fieldInvoice21 = normalize(vatTotal, 15) + '0' * 26 + ' ' * 30 + '0' * 15
                
            line = INVOICEFORMAT.substitute(field1 = date, field2 = itype,
                                            field3 = pv, field4 = num,
                                            field5 = fieldInvoice5, 
                                            field6 = docType, field7 = cuit, 
                                            field8 = name, field9 = total, 
                                            field10 = cng,
                                            field11 = fieldInvoice11, 
                                            field12 = fieldInvoice12,
                                            field13 = pGross, field14 = pIncome,
                                            field19 = len(vats), 
                                            field21 = fieldInvoice21)
            invoiceFile.write(line + '\n')
            
            if invoicesType == 'SALES':
                fieldAliquot4 = ''
                fieldAliquot5 = ''
            else:
                fieldAliquot4 = docType
                fieldAliquot5 = cuit
            
            for aliCode in vats:
                net = normalize(vats[aliCode][0], 15)
                vat = normalize(vats[aliCode][1], 15)
                line = ALIQUOTFORMAT.substitute(field1 = itype, field2 = pv,
                                                field3 = num, field4 = fieldAliquot4,
                                                field5 = fieldAliquot5, field6 = net, 
                                                field7 = aliCode, field8 = vat)
                aliquotFile.write(line + '\n')
                
    invoiceFile.close()
    aliquotFile.close()
    