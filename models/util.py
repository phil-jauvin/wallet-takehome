from pydantic import condecimal

# A decimal that must have a value greater than or equal to 0
NonNegativeDecimal = condecimal(ge=0)
