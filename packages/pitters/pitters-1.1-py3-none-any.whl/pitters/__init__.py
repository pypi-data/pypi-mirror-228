import unicodedata

def sanitize_spaces(string):
    return ' '.join(string.split())


def convert_case(string, case='original'):
    #Deja el case requerido
    if case == 'original':
        return string
    elif case == 'upper' or case == 'uppercase' or case == 'mayus':
        string = string.upper()

    elif case =='lower' or case == 'lowercase' or case == 'minus':
        string = string.lower()

    elif case == 'capitalize' or case == 'capital':
        string = string.capitalize()

    else:
        ValueError("El argumento de 'case' = ['original', 'upper', 'lower', 'capitalize']")


def to_ascii(string, enie=False):
    if enie == True:
        string = string.replace("ñ", "#!#").replace("Ñ", "$!$")
        string = unicodedata.normalize('NFKD', string).encode('ascii','ignore').decode('ascii')
        string = string.replace("#!#", "ñ").replace("$!$", "Ñ")
    else:
        string = unicodedata.normalize('NFKD', string).encode('ascii','ignore').decode('ascii')
    return string


def magic(string, case='original', enie=False):
    string = sanitize_spaces(string)
    string = convert_case(string, case=case)
    string = to_ascii(string, enie=enie)
    return string