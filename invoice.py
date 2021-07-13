# -*- coding: utf-8 -*-
"""
@author: Mac Meldi Roch

        *-* Clase que representa una factura de compra o venta *-*
ID:
    - Punto de venta
    - Numero de comprobante
Almacena:
    - Fecha
    - Tipo de factura (Fact. A, Nota de cred. A)
    - Importe Exento
    - Importe de Conceptos No Gravados
    - Importe de Conceptos Gravados, correspondiente IVA y alicuota
    - Importe de Percepciones (IIBB, Ganancias, IVA)
    - Importe de Impuestos Municipales
    - Importe de Impuestos Internos
"""
LENGHT_PV = 5
LENGHT_NUM = 20
ALIQUOT_CODE = {'105': '4',
                '21': '5',
                '27': '6'}

'''************************************************************************'''
'''                                   AUX                                  '''
'''************************************************************************'''
def normalize(parameter, characters):
    parameter = str(parameter)
    return (characters - len(parameter)) * '0' + parameter

'''************************************************************************'''
'''                          Class: INVOICE                                '''
'''************************************************************************'''

class Invoice:
    def __init__(self, pv, num, cuit, date, name, typei):
        '''
        Initializer.

        Parameters
        ----------
        pv : int
            Numero de punto de venta de la factura. Puede ser formato completo
            '00015' o compacto '15'.
            *El punto de venta no puede ser '0', se reemplaza por '1'.*
        num : int
            Numero de comprobante de la factura. Puede ser formato completo
            '00000748' o compacto '748'.
        cuit : int
            Numero de cuit del cliente/proveedor.
        date : datetime.date
            Fecha del comprobante.
        name : str
            Razón social.
        typei : str
            Tipo de comprobante: "A" o "C". Si el campo es una cadena vacía se
            reemplaza por "A".

        Returns
        -------
        None.

        '''
        if pv == 0:
            pv = 1
            
        if typei == '':
            typei = 'A'
            
        self.id = (normalize(pv, LENGHT_PV), normalize(num, LENGHT_NUM)) #(str, str)
        self.cuit = str(cuit) #str
        self.date = date #datatime.date
        self.name = name #str
        self.typei = typei #str
        self.exempt = 0 
        self.cng = 0
        self.taxes = [0., 0., 0.] #pVat, pIncome, pGross
        self.vat = {}
    
    def __eq__(self, other):
        '''
        Parameters
        ----------
        other : OBJECT.INVOICE
            Instancia de la clase "Invoice".

        Returns
        -------
        boolean
            True: si ambas instancias son idénticas. Caso contrario False.

        '''
        return self.id[0] == other.id[0] and self.id[1] == other.id[1] and self.cuit == other.cuit

        '''---------->>            SETTERS            <<----------'''
        
    def setExempt(self, amount):
        '''
        Almacena el importe exento de la factura.

        Parameters
        ----------
        amount : str
            Importe a agregar.

        Returns
        -------
        None.

        '''
        self.exempt = self.exempt + amount
        
    def setCNG(self, amount):
        '''
        Almacena el importe neto no gravado de la factura.

        Parameters
        ----------
        amount : str
            Importe a agregar.

        Returns
        -------
        None.

        '''
        self.cng = self.cng + amount
        
    def setTaxes(self, vat, income, gross):
        '''
        Almacena las percepciones de la factura.
        ** Falta implementar que tenga en cuenta los Impuestos Municipales
        e Impuestos Internos.**

        Parameters
        ----------
        vat : str
            Importe de Percepciones de IVA a agregar.
        iibb : str
            Importe de Percepciones de Ingresos Brutos a agregar.
        gcias : str
            Importe de Percepciones de Ganancias a agregar.

        Returns
        -------
        None.

        '''
        self.taxes[0] = self.taxes[0] + vat
        self.taxes[1] = self.taxes[1] + income
        self.taxes[2] = self.taxes[2] + gross
        
    def setVat(self, ali, net, vat):
        '''
        Almacena la informacion de Neto e IVA de determinada alicuota

        Parameters
        ----------
        ali : str
            Valor de alicuota de IVA. Formato aceptado: '10.5', '10,5' o '105'
        net : str
            Importe Neto a agregar.
        vat : str
            Importe de IVA a agregar.

        Returns
        -------
        None.

        '''
        if vat != 0:
            self.vat[ali] = (net, vat)
            
            '''---------->>            GETTERS            <<----------'''
            
    def isWithholding(self):
        '''
        Evalua si la instancia representa a un comprobante de retencion en lugar de
        una factura de compra/venta.

        Returns
        -------
        boolean
            Si es un comprobante de retencion: True
            Si es una factura: False.

        '''
        totalvat = 0
        totalnet = 0
        
        for v in self.vat:    
            totalnet = totalnet + self.vat[v][0]
            totalvat = totalvat + self.vat[v][1]
        
        return totalnet == 0 and totalvat == 0  and self.exempt == 0 and self.cng == 0
    
    def getTotal(self):
        '''
        Evectua la sumatoria de importes de los conceptos de la factura

        Returns
        -------
        float
            Importe total de la factura.

        '''
        subtotal = self.exempt + self.cng
        for t in self.taxes:
            subtotal = subtotal + t
            
        totalvat = 0
        totalnet = 0
        
        for v in self.vat:    
            totalnet = totalnet + self.vat[v][0]
            totalvat = totalvat + self.vat[v][1]
            
        return subtotal + totalnet + totalvat
    
    def getType(self):
        '''
        Evalua el importe total de la factura y lo asocia al tipo de comprobante
        que representa.
        ** Si el total es positivo, devuelve Factura A = '001' o Factura C = '011'
        ** Si el total es negativo, devuelve Nota de Crédito A = '003' o Nota de Crédito A = '013'
        
        *! Se asume que en el Libro IVA no pueden cargarse Comprobantes del tipo B !*

        Returns
        -------
        str
            Codigo de comprobante con el formato '000'.

        '''
        if self.getTotal() < 0:
            if self.typei == 'C':
                return '013'
            return '003'
        else:
            if self.typei == 'C':
                return '011'
            return '001'

    def getID(self):
        return self.id
    
    def getName(self):
        return self.name
    
    def getCNG(self):
        return self.cng
    
    def getCUIT(self):
        return self.cuit
    
    def getExempt(self):
        return self.exempt
    
    def getTaxes(self):
        return self.taxes
    
    def getVats(self):
        if (self.vat == {}) and not (self.typei == 'C'):
            return {3: (0., 0.)}
        return self.vat
    
    def getDate(self):
        y = normalize(self.date.year, 4)
        m = normalize(self.date.month, 2)
        d = normalize(self.date.day, 2)
        
        return y + m + d
