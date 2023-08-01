import datetime
from functions_general import *

def show(this,target, plan_type):
    if target != plan_type:
        return 'display: none'

def paymentType(this,plan_type):
    if plan_type == 'diario':
        return 'único'
    if plan_type == 'mensual':
        return 'mensual'

def multiply(this,n1, n2):
    return formatNumber(n1 * n2)

def formatDate(this,input_date):
    parts = str(input_date).split("-")
    return f"{parts[2]}/{parts[1]}/{parts[0]}"

def zfill(this,number, width):
    number = int(number)
    number_output = abs(number)
    number_str = str(number_output)
    length = len(number_str)
    zero = "0"

    if width <= length:
        if number < 0:
            return "-" + number_str
        else:
            return number_str
    else:
        if number < 0:
            return "-" + zero * (width - length) + number_str
        else:
            return zero * (width - length) + number_str

def drawX(this,condition):
    return "X" if condition else ""

def drawXinverse(this,condition):
    return "" if condition else "X"

def drawXToSelection(this,currency_str, value):
    return "X" if value == currency_str else ""

def parseCell(this,field):
    return "-" if field is None or field == "" else field

def numAdditionalsInsureds(this,additionals_insureds):
    return f"({len(additionals_insureds)})"

def getAge(date):
    dob = datetime.datetime.strptime(date, "%Y-%m-%d")
    today = datetime.datetime.today()
    age = today.year - dob.year
    if today.month < dob.month or (today.month == dob.month and today.day < dob.day):
        age -= 1
    return age

def areOlderThanAge(insureds):
    for i in insureds:
        if getAge(i['birthdate']) > 54:
            return True
    return False

def insuredPlan(this,policy_holder, additionals_insureds, plan_code):
    age = getAge(policy_holder['birthdate'])
    insured_older = areOlderThanAge(additionals_insureds) if additionals_insureds else False
    if plan_code == 1 or plan_code == 2 or plan_code == 3 or plan_code == 4 or plan_code == 5 or plan_code == 6 or plan_code == 7 or plan_code == 8:
        return "X"
    else:
        return ""


