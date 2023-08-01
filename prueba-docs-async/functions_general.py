import re
def mapRelation(this,relationship):
    relations = {
        'spouse': 'Cónyuge',
        'couple': 'Pareja',
        'wife' : 'Esposa',
        'son': 'Hijo',
        'daughter': 'Hija',
        'father': 'Padre',
        'mother': 'Madre',
        'fatherinlaw': 'Suegro',
        'motherinlaw': 'Suegra',
        'stepson': 'Hijastro',
        'stepdaughter': 'Hijastra',
        'other': 'Otro'
    }
    return relations.get(relationship, '')


def getPercent(this,coverage):
    return f'{coverage * 100}%'


def formatDate(this,input_date):
    parts = str(input_date).split("-")
    return f'{parts[2]}/{parts[1]}/{parts[0]}'


class RegexRules:
    CLEAN_REGEX = r'[^\dk]+'
    GROUP_REGEX = r'(\d)(?=(\d{3})+\b)'
    GROUP_REPLACE = r'\1.'
    CLEAN_FINAL_STR_REGEX = r'\.'


def cleanRut(value):
    return re.sub(RegexRules.CLEAN_REGEX, '', value)


def formatRut(this,value):
    rut = cleanRut(value)
    if len(rut) < 3:
        return rut
    checksum = rut[-1].lower()
    digits = rut[:-1].lower()
    formatted_digits = re.sub(
        RegexRules.GROUP_REGEX,
        RegexRules.GROUP_REPLACE,
        digits
    )
    return f'{formatted_digits}-{checksum}'


def formatNumber(this,number):
    parts = str(number).split(".")
    parts[0] = re.sub(r'\B(?=(\d{3})+(?!\d))', ".", parts[0])
    return ",".join(parts)

def formatUf(this,number):
    return "{:,.2f}".format(number).replace(",", ".")

def getTypesBeneficiaries(this,beneficiaries, type, value):
    resp_return = ''
    if (len(beneficiaries) < 1 and type == 'law') or (len(beneficiaries) > 0 and type == 'others'):
        resp_return = value
    return resp_return