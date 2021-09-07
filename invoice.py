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
ALIQUOT_CODE = {'105': '0004',
                '210': '0005',
                '270': '0006',
                '21': '0005',
                '27': '0006'}
NEGINVOICE_CODE = {'A': '003',
                   'C': '013',
                   'B': '008'}
POSINVOICE_CODE = {'A': '001',
                   'C': '011',
                   'B': '006',
                   'Z': '082'}

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
            
        self.id = (normalize(pv, LENGHT_PV), normalize(num, LENGHT_NUM)) #(str, str)
        self.cuit = str(cuit) #str
        self.date = date #datatime.date
        self.name = name #str
        self.typei = typei.upper() #str
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
            ali = str(ali).replace(".", "").replace(",", "")
            self.vat[ALIQUOT_CODE[ali]] = (round(net, 2), round(vat, 2))
            
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
        Evectua la sumatoria de los conceptos de la factura

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
            
        return round(subtotal + totalnet + totalvat, 2)
    
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
        try:
            if self.getTotal() < 0:
                    cod = NEGINVOICE_CODE[self.typei]
            else:
                    cod = POSINVOICE_CODE[self.typei]
        except:
            cod = 'XXX'
        return cod

    def getID(self):
        return self.id
    
    def getName(self):
        return self.name
    
    def getCNG(self):
        return round(self.cng, 2)
    
    def getCUIT(self):
        return self.cuit
    
    def getExempt(self):
        return round(self.exempt, 2)
    
    def getTaxes(self):
        taxes = []
        for t in self.taxes:
            taxes.append(round(t, 2))
        return taxes
    
    def getVats(self):
        if (self.vat == {}) and (self.typei == 'A'):
            return {'0003': (0., 0.)}
        return self.vat
    
    def getDate(self):
        y = normalize(self.date.year, 4)
        m = normalize(self.date.month, 2)
        d = normalize(self.date.day, 2)
        
        return y + m + d
