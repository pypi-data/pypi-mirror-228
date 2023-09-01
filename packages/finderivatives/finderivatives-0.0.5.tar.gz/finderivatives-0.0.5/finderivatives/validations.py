"""

"""

import numpy as np
from finderivatives.errors import PositionError, SpotError

    
def validate_position(position):
    try:
        # Validate postion as int or float
        if (isinstance(position, int) | isinstance(position, float)) &\
           (position in [1, -1, 1.0, -1.0]):
            return int(position)
        
        # Validate postion as str
        elif (isinstance(position, str)) & (position in ['1', '-1']):
            return int(position)
        
        # Raise error
        else:
            raise PositionError()
    
    # Catch error
    except PositionError as error:
        error.set_value_error(position)
        raise error



def validate_strike(strike):
    try:
        if (isinstance(strike, int)) | (isinstance(strike, float)):
            return strike
        else:
            raise TypeError
            
    except TypeError:
        message = 'The argument "strike" must be of type int or float'
        raise TypeError(message)


def validate_premium(premium):
    try:
        if (isinstance(premium, int)) | (isinstance(premium, float)):
            return premium
        else:
            raise TypeError
            
    except TypeError:
        message = 'The argument "premium" must be of type int or float'
        raise TypeError(message)



def validate_maturity(maturity):
    try:
        # Validate type
        if not (isinstance(maturity, int)) | (isinstance(maturity, float)):
            raise TypeError
        
        # Validate value
        elif maturity < 0:
            raise ValueError
            
        else:
            return maturity
    
    except TypeError:
        message = 'The argument "maturity" must be of type int or float'
        raise TypeError(message)
        
    except ValueError:
        message = 'The argument "maturity" must be a positive value'
        raise ValueError(message)



def validate_spot(spot):
    try:
        # Validate unique numbers
        if isinstance(spot, int) | isinstance(spot, float):
            return np.array(spot)
        
        # Validate lists and tuples
        elif isinstance(spot, list) | isinstance(spot, tuple):
            for i in spot:
                if isinstance(i, int) | isinstance(i, float):
                    pass
                else:
                    raise SpotError()
            return np.array(spot)
        
        # Validate array
        elif isinstance(spot, np.ndarray):
            return spot
        
        # Raise error
        else:
            raise SpotError()
    
    # Catch error
    except SpotError as error:
        error.set_value_error(spot)
        raise error



if __name__ == '__main__':
    print(' Ejecucion directa ... \n')
    # a = validate_position(0)
    # b = validate_spot([1, 2, 3, 4, '1'])
    # print('Ejecucion completa')





