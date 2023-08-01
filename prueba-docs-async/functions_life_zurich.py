from functions_general import *



array_coverages = {
    'Muerte': 'ZuVida',
    'Invalidez': 'ZuITP',
    'Muerte Accidental': 'ZuMA',
    'Urgencias Medicas': 'ZuMe',
}


def checkCoverage(this,name_cover, arrive_cove, value):
    val_coverages = array_coverages.get(name_cover, '')
    value_return = ''
    for item in arrive_cove:
        if item["code"] == 'ZuMa':
            item["code"] = 'ZuMA'
        if item["code"] == val_coverages or item["code"] == 'ZuMe':
            value_return = value
    return value_return


def getAmountCoverage(this,name_cover, coverages):
    val_coverages = array_coverages.get(name_cover, '')
    value_return = 0
    added_value = 0
    for item in coverages:
        if item["code"] == 'ZuMa':
            item["code"] = 'ZuMA'
        if item["code"] == val_coverages:
            value_return += item["totalAmount"] or 0
        if item["code"] == 'ZuMe':
            added_value = item["totalAmount"]
    if name_cover == 'Muerte Accidental':
        value_return += added_value
    if value_return != 0:
        return formatNumber(this,value_return)
    else:
        return ''


def sumCoverageColum(this,array_coverage, column):
    calculated_value = 0
    for item in array_coverage:
        if column == 'exempt':
            if isPremiumExempt(item["code"]):
                calculated_value += item["premium"]
        if column == 'affected':
            if not isPremiumExempt(item["code"]):
                calculated_value += (item["premium"] / 1.19)
        if column == 'tax':
            if not isPremiumExempt(item["code"]):
                calculated_value += (item["premium"] - item["premium"] / 1.19)
        if column == 'gross':
            calculated_value += item["premium"]
    calculated_value = round(calculated_value, 4)
    return formatNumber(this,calculated_value)


def getCoverageName(this,code):
    if code == 'ZuMa':
        code = 'ZuMA'
    coverage_array_name = {
        'ZuVida': 'Fallecimiento',
        'ZuITP': 'ITP',
        'ZuMA': 'Muerte Accidental',
        'ZuMe': 'MA + Asist. Urgen.'
    }
    return coverage_array_name.get(code, '')


def getCoverageLongName(this,code):
    if code == 'ZuMa':
        code = 'ZuMA'
    coverage_array_long_name = {
        'ZuVida': 'Fallecimiento por muerte natural o accidental',
        'ZuITP': 'Invalidez Total y Permanente (ITP)',
        'ZuMA': 'Doble capital en caso de muerte accidental',
        'ZuMe': 'Muerte Accidental y Urgencias médicas'
    }
    return coverage_array_long_name.get(code, '')


def getCoverageCmfCode(this,code):
    if code == 'ZuMa':
        code = 'ZuMA'
    coverage_array_name = {
        'ZuVida': 'POL220190013',
        'ZuITP': 'CAD320190015',
        'ZuMA': 'CAD220190014',
        'ZuMe': 'CAD220190014'
    }
    return coverage_array_name.get(code, '')


def isPremiumExempt(code):
    if code == 'ZuMa':
        code = 'ZuMA'
    coverage_array_name = {
        'ZuVida': True,
        'ZuITP': False,
        'ZuMA': True,
        'ZuMe': True
    }
    return coverage_array_name.get(code, False)


def printPremium(this, code, value, field_name):
    calculated_value = None
    if field_name == 'gross':
        calculated_value = value
    elif field_name == 'exempt':
        if isPremiumExempt(code):
            calculated_value = value
    elif field_name == 'affected':
        if not isPremiumExempt(code):
            calculated_value = value / 1.19
    elif field_name == 'tax':
        if not isPremiumExempt(code):
            calculated_value = value - value / 1.19
    if isinstance(calculated_value, float):
        calculated_value = formatNumber(this,format(calculated_value, '.4f'))
    return calculated_value


def getPaymentMethodGeneric(this, code):
    generic_name = {
        'visa': 'Tarjetade Credito',
        'mastercard': 'Tarjeta de Credito',
        'mach': 'Prepago',
        'webpay': 'Tarjeta de Debito',
        'americanexpress': 'Tarjeta de Credito',
        'magna': 'Tarjeta de Credito',
        'redcompra': 'Tarjeta de Debito',
        'prepago': 'Prepago',
        '': ''
    }
    if isinstance(code, str):
        return generic_name.get(code.lower(), '')
    else:
        return ''


def getCoverageText(this, code):
    if code == 'ZuMa':
        code = 'ZuMA'

    coverage_array_text = {
        'ZuVida': 'Fallecimiento (POL220190013): El capital asegurado señalado en estas Condiciones Particulares será pagado por la compañía aseguradora a él o los beneficiarios, después del fallecimiento del asegurado, si este ocurre durante la vigencia de la póliza, por una causa no excluida de cobertura.',
        'ZuMA': 'Muerte Accidental (CAD220190014): La Compañía Aseguradora pagará a él o los beneficiarios de la póliza, el capital asegurado señalado en estas Condiciones Particulares, si el fallecimiento del asegurado se produce a consecuencia directa e inmediata de un accidente. En este caso, los beneficiarios recibirán el pago del capital asegurado considerado para la cobertura de fallecimiento y el de muerte accidental, siempre que el siniestro se encuentre cubierto por la póliza. <br/><br/>Se entenderá cómo fallecimiento inmediato aquel que ocurra a más tardar dentro de los sesenta (60) días corridos siguientes de ocurrido el accidente. Para los efectos de este seguro se entiende por accidente, todo suceso imprevisto, involuntario, repentino y fortuito, causado por medios externos, que afecte el organismo del asegurado provocándole lesiones, que se manifiesten por heridas visibles o contusiones internas.',
        'ZuITP': 'Invalidez Total y Permanente 2/3 (CAD320190015): La Compañía Aseguradora pagará anticipadamente al asegurado el capital señalado en estas Condiciones Particulares para el caso de fallecimiento, en caso de invalidez permanente dos tercios del asegurado (no se suman capitales), siempre que se cumplan las siguientes condiciones: <br/><br/>a) Que la póliza principal esté vigente. <br/>b) Que el asegurado cumple con los requisitos de asegurabilidad. <br/>c) Que la invalidez permanente dos tercios sea causada por enfermedad diagnosticada o accidente ocurrido durante la vigencia de esta cláusula adicional. <br/><br/>En consecuencia, se extinguirá el derecho al cobro de otras indemnizaciones.',
    }
    return coverage_array_text.get(code, '')


def getAssistanceLongName(this,code):
    if code == 'DocOn':
        code = 'ZuDocOn'
    if code == 'MedDom':
        code = 'ZuMedDom'
    if code == 'MedTel':
        code = 'ZuMedTel'

    assistance_array_long_name = {
        'ZuDocOn': 'Doctor online',
        'ZuNutTel': 'Orientación nutricional telefónica',
        'ZuMedDom': 'Médico a domicilio',
        'ZuNocMed': 'Compra nocturna de medicamentos',
        'ZuKinDom': 'Kinesiólogo respiratorio a domicilio',
        'ZuMedTel': 'Orientación médica telefónica',
    }
    return assistance_array_long_name.get(code, '')


def getAssistanceText(this,code):
    if code == 'DocOn':
        code = 'ZuDocOn'
    if code == 'MedDom':
        code = 'ZuMedDom'
    if code == 'MedTel':
        code = 'ZuMedTel'

    assistance_array_text = {
        'ZuDocOn': 'Resuelve tus consultas sobre medicina general y pediatría con un doctor en línea. <br/>· Podrás conectarte por video llamada, ya sea por tu computador o smartphone, con médicos generales y pediatras para resolver consultas sobre tu salud. <br/>Solo debes descargar el app del servicio. <br/>· Condiciones: podrás contactar a un médico general o pediatra entre las 16:00 y las 24:00 horas, según la disponibilidad y la agenda de cada especialista. <br/>· Tope de uso: 2 veces al año. <br/>· Tope de precio: no tiene.',
        'ZuNutTel': 'Podrás consultar por teléfono sobre información de nutrición. <br/>· Podrás consultar información nutricional a nuestros expertos para ayudarte con tu recomendaciones de alimentación, ingesta de calorías según peso y estatura, entre otros. <br/>· Podrás consultar por: Información Telefónica sobre Nutrición; Métodos de evaluación antropométrica; Cantidad de calorías a ingerir según peso y estatura; Cantidad de calorías de diferentes alimentos; Cantidad de calorías de que se queman por la práctica de ejercicios. <br/>Cantidad de ejercicios que se pueden realizar según objetivos; Tipos de alimentos polivitamínicos que se pueden ingerir para aumentar condición aeróbica, capacidad muscular; Enfermedades de los deportistas; Recomendaciones higiénico- dietéticas; <br/>Consultas sobre evolución de distintos tratamientos. <br/>· Tope de uso: Ilimitado.<br/>· Tope de precio: no tiene.',
        'ZuMedDom': 'Podrás pedir por teléfono un servicio de atención médica general a domicilio. <br/>· Si te sientes mal y no puedes salir de tu hogar, podrás solicitar la visita de un médico en medicina general a tu domicilio. <br/>· Condiciones: horario hábil sujeto a zona geográfica y disponibilidad; en caso de reembolsos debes llamar por teléfono previamente para solicitar el beneficio y tener en tu poder los documentos necesarios para gestionar la devolución. <br/>· Tope de uso: 2 veces al año. <br/>· Tope de precio: 3 UF por evento.',
        'ZuNocMed': 'Podrás pedir por teléfono que un mensajero compre y entregue tus medicamentos.<br/>· En caso que no puedas acudir a una farmacia en horario nocturno, este servicio te permite solicitar la compra de medicamentos y despacho a tu domicilio de los medicamentos que requieras.<br/>· Condiciones: disponible sólo para compras en la noche, entre las 23:00 y las 6:00hrs; la compra debe ser superior a $10.000; no podrás usar este servicio para comprar medicamentos con receta retenida ni utilizar cupones de descuento; tu domicilio debe estar dentro del radio urbano de tu ciudad. Por radio urbano se define la ciudad como tal y 20 km máximo a su alrededor desde sus límites siempre que las rutas de acceso lo permitan (camino transitable por un automóvil).<br/>· Tope de uso: Ilimitado.<br/>· Tope de precio: no tiene.',
        'ZuKinDom': 'Podrás pedir por teléfono que un kinesiólogo te atienda a domicilio. <br/>· Si alguien en tu casa necesita ayuda por una enfermedad respiratoria, podrás solicitar la visita de un kinesiólogo respiratorio a domicilio. <br/>· Condiciones: el costo del servicio dependerá del horario de la solicitud y tu ubicación geográfica; se requiere una orden médica; se excluyen lesiones y enfermedades traumatológicas. <br/>· Tope de uso: 1 vez al año. <br/>· Tope de precio: 1 UF. Si el costo del servicio es superior a 1 UF, deberás pagar la diferencia directamente al kinesiólogo.',
        'ZuMedTel': 'Servicio informativo sobre dudas y consultas de tu salud. <br/>· En caso de que tengas dudas sobre algún síntoma, tratamiento, medicamento o alguna enfermedad, podrás llamar y contar con un servicio informativo de tu salud. <br/>· Condiciones: no tiene.<br/>· Tope de uso: Ilimitado.<br/>· Tope de precio: no tiene.',
        }
    return assistance_array_text.get(code, '')

def getCoverageExclusionText(this,coverages):
    ptext = ' y en las Cláusulas Adicionales '
    for item in coverages:
        if item['code'] == 'ZuITP' or item['code'] == 'ZuMA' or item['code'] == 'ZuMa':
            ptext += getCoverageCmfCode(this,item['code']) + ', '
    ptext += 'las que se encuentran depositadas en la Comisión para el Mercado Financiero'
    return ptext

def isCoveragePrintable(this, coverages, code_coverage):
    for coverage in coverages:
        if coverage['code'] == 'ZuMa':
            coverage['code'] = 'ZuMA'
        if coverage['code'] == code_coverage:
            return True
    return False

def isBeneficiary(this, beneficiaries):
    if len(beneficiaries) > 0:
        return True
    else:
        return False

def printFullName(this, person):
    #print(person)
    return person['name'] + ' ' + person['paternalLastname'] + ' ' + person['maternalLastname']
