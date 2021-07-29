# -*- coding: utf-8 -*-

import os
from extractData import *
from saveData import *

def start(period, purchasesFile, salesFile, outputPath, cuit = ''):
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
            saveData(sales, 'SALES', period, outputPath)
        elif salesFile == '':
            purchases = extract(purchasesFile, 'PURCHASES', cuit)
            saveData(purchases, 'PURCHASES', period, outputPath)
        else:
            sales = extract(salesFile, 'SALES', cuit)
            saveData(sales, 'SALES', period, outputPath)
            purchases = extract(purchasesFile, 'PURCHASES', cuit)
            saveData(purchases, 'PURCHASES', period, outputPath)
            
        return 'OK'
    except:
        return 'FAILED'