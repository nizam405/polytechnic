from django.core.exceptions import ValidationError

def valid_result(result):
    result = float(result)
    if not 2.00 <= result <= 5.00:
        raise ValidationError("Expecting value 2.00 - 5.00")
    
        
