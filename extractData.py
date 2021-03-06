# -*- coding: utf-8 -*-

from invoice import *
from dbfread import DBF

HEADERFLOAT = ['NROFACT', 'NROFACTURA', 'FECFACTURA', 'CUITCLIE', 'IMPIVA1',
               'NETOFACT', 'EXENTFACT', 'CNGFACT', 'IVA1MOD', 'RIVA', 'RIB', 'RGAN']
HEADERSTR = ['NOMBRECLIE', 'FACTIPO']

'''************************************************************************'''
'''                                   AUX                                  '''
'''************************************************************************'''   
def extractData(row, invoicesType):
    '''
    

    Parameters
    ----------
    row : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    if invoicesType == 'SALES':
        HEADER = HEADERFLOAT[:-3] + HEADERSTR
    else:
        HEADER = HEADERFLOAT + HEADERSTR
        
    data = {}
    for key in HEADER:
        field = row[key]
        if field == None:
            if (key in HEADERSTR):
                field = ''
            else:
                field = 0
        data[key] = field
    return data    

def deleteWithholdings(invoicesList):
    '''
    

    Parameters
    ----------
    invoicesList : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    cleanList = []
    for invoice in invoicesList:
        if not invoice.isWithholding():
            cleanList.append(invoice)
            
    return cleanList

'''************************************************************************'''
'''                                 EXTRACT                                '''
'''************************************************************************'''

def extract(file, invoicesType, cuit):
    finished = False
    while not finished:
        table = None
        try:
            table = DBF(file, encoding= 'unicode_escape')
        except IOError:
            return []
        
        if table:
            invoices = []
            for row in table:
                if str(row['CUIT']) == cuit:
                    data = extractData(row, invoicesType)
                    newInvoice = Invoice(data['NROFACT'], data['NROFACTURA'], data['CUITCLIE'], 
                                         data['FECFACTURA'], data['NOMBRECLIE'], data['FACTIPO'])
                    exists = False               
                    i = 0
                    while (not exists and i < len(invoices)):
                        if newInvoice == invoices[i]:
                            newInvoice = invoices[i]
                            exists = True
                        i += 1
                    
                    newInvoice.setExempt(data['EXENTFACT'])
                    newInvoice.setCNG(data['CNGFACT'])
                    if invoicesType == 'PURCHASES':
                        newInvoice.setTaxes(data['RIVA'], data['RIB'], data['RGAN'])
                    newInvoice.setVat(data['IVA1MOD'], data['NETOFACT'], data['IMPIVA1'])
                    
                    if not exists:
                        invoices.append(newInvoice)
                
            finished = True
    invoices = deleteWithholdings(invoices)
    return invoices
 
