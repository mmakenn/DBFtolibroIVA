# -*- coding: utf-8 -*-

import os
from extractData import *
from saveData import *

def start(period, purchasesFile, salesFile, cuit = ''):
    '''
    

    Parameters
    ----------
    period : TYPE
        DESCRIPTION.
    purchasesfile : TYPE
        DESCRIPTION.
    salesfile : TYPE
        DESCRIPTION.
    cuit : TYPE, optional
        DESCRIPTION. The default is ''.

    Returns
    -------
    str
        DESCRIPTION.

    '''   
    try:
        if purchasesFile == '':
            sales = extract(salesFile, 'SALES', cuit)
            saveData(sales, 'SALES', period)
        elif salesFile == '':
            purchases = extract(purchasesFile, 'PURCHASES', cuit)
            saveData(purchases, 'PURCHASES', period)
        else:
            sales = extract(salesFile, 'SALES', cuit)
            saveData(sales, 'SALES', period)
            purchases = extract(purchasesFile, 'PURCHASES', cuit)
            saveData(purchases, 'PURCHASES', period)
            
        return 'OK'
    except:
        return 'FAILED'