
def parseFloat(str):
    if len(str) == 0:
        return None
    if str == 'NaN':
        return None
    return float(str)
