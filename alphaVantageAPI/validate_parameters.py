# -*- coding: utf-8 -*-

def _alidate_parameters(api_indicator_matype, option, parameters:dict, **kwargs): # -> dict
    """Validates kwargs and attaches them to parameters."""

    # APO, PPO, BBANDS
    matype = int(math.fabs(kwargs['matype'])) if 'matype' in kwargs else None
    if option == 'matype' and matype is not None and matype in api_indicator_matype:
        parameters['matype'] = matype

    # BBANDS
    nbdevup = math.fabs(kwargs['nbdevup']) if 'nbdevup' in kwargs else None
    nbdevdn = math.fabs(kwargs['nbdevdn']) if 'nbdevdn' in kwargs else None
    if option == 'nbdevup' and nbdevup is not None:
        parameters['nbdevup'] = nbdevup
    if option == 'nbdevdn' and nbdevdn is not None:
        parameters['nbdevdn'] = nbdevdn

    # ULTOSC
    timeperiod1 = int(math.fabs(kwargs['timeperiod1'])) if 'timeperiod1' in kwargs else None
    timeperiod2 = int(math.fabs(kwargs['timeperiod2'])) if 'timeperiod2' in kwargs else None
    timeperiod3 = int(math.fabs(kwargs['timeperiod3'])) if 'timeperiod3' in kwargs else None
    if option == 'timeperiod1' and timeperiod1 is not None:
        parameters['timeperiod1'] = timeperiod1
    if option == 'timeperiod2' and timeperiod2 is not None:
        parameters['timeperiod2'] = timeperiod2
    if option == 'timeperiod3' and timeperiod3 is not None:
        parameters['timeperiod3'] = timeperiod3

    # SAR
    acceleration = math.fabs(float(kwargs['acceleration'])) if 'acceleration' in kwargs else None
    maximum = math.fabs(float(kwargs['maximum'])) if 'maximum' in kwargs else None
    if option == 'acceleration' and acceleration is not None:
        parameters['acceleration'] = acceleration
    if option == 'maximum' and maximum is not None:
        parameters['maximum'] = maximum

    # MAMA
    fastlimit = math.fabs(float(kwargs['fastlimit'])) if 'fastlimit' in kwargs else None
    slowlimit = math.fabs(float(kwargs['slowlimit'])) if 'slowlimit' in kwargs else None
    if option == 'fastlimit' and fastlimit is not None and fastlimit > 0 and fastlimit < 1:
        parameters['fastlimit'] = fastlimit
    if option == 'slowlimit' and slowlimit is not None and slowlimit > 0 and slowlimit < 1:
        parameters['slowlimit'] = slowlimit

    # MACD, APO, PPO, ADOSC
    fastperiod = int(math.fabs(kwargs['fastperiod'])) if 'fastperiod' in kwargs else None
    slowperiod = int(math.fabs(kwargs['slowperiod'])) if 'slowperiod' in kwargs else None
    signalperiod = int(math.fabs(kwargs['signalperiod'])) if 'signalperiod' in kwargs else None
    if option == 'fastperiod' and fastperiod is not None:
        parameters['fastperiod'] = fastperiod                            
    if option == 'slowperiod' and slowperiod is not None:
        parameters['slowperiod'] = slowperiod
    if option == 'signalperiod' and signalperiod is not None:
        parameters['signalperiod'] = signalperiod

    # MACDEXT
    fastmatype = int(math.fabs(kwargs['fastmatype'])) if 'fastmatype' in kwargs else None
    slowmatype = int(math.fabs(kwargs['slowmatype'])) if 'slowmatype' in kwargs else None
    signalmatype = int(math.fabs(kwargs['signalmatype'])) if 'signalmatype' in kwargs else None
    if option == 'fastmatype' and fastmatype is not None and fastmatype in api_indicator_matype:
        parameters['fastmatype'] = fastmatype
    if option == 'slowmatype' and slowmatype is not None and slowmatype in api_indicator_matype:
        parameters['slowmatype'] = slowmatype
    if option == 'signalmatype' and signalmatype is not None and signalmatype in api_indicator_matype:
        parameters['signalmatype'] = signalmatype

    # STOCH(F), STOCHRSI
    fastkperiod = int(math.fabs(kwargs['fastkperiod'])) if 'fastkperiod' in kwargs else None
    fastdperiod = int(math.fabs(kwargs['fastdperiod'])) if 'fastdperiod' in kwargs else None
    fastdmatype = int(math.fabs(kwargs['fastdmatype'])) if 'fastdmatype' in kwargs else None
    if option == 'fastkperiod' and fastkperiod is not None:
        parameters['fastkperiod'] = fastkperiod
    if option == 'fastdperiod' and fastdperiod is not None:
        parameters['fastdperiod'] = fastdperiod
    if option == 'fastdmatype' and fastdmatype is not None and fastdmatype in api_indicator_matype:
        parameters['fastdmatype'] = fastdmatype

    # STOCH(F), STOCHRSI
    slowkperiod = int(math.fabs(kwargs['slowkperiod'])) if 'slowkperiod' in kwargs else None
    slowdperiod = int(math.fabs(kwargs['slowdperiod'])) if 'slowdperiod' in kwargs else None
    slowkmatype = int(math.fabs(kwargs['slowkmatype'])) if 'slowkmatype' in kwargs else None
    slowdmatype = int(math.fabs(kwargs['slowdmatype'])) if 'slowdmatype' in kwargs else None
    if option == 'slowkperiod' and slowkperiod is not None:
        parameters['slowkperiod'] = slowkperiod
    if option == 'slowdperiod' and slowdperiod is not None:
        parameters['slowdperiod'] = slowdperiod
    if option == 'slowkmatype' and slowkmatype is not None and slowkmatype in api_indicator_matype:
        parameters['slowkmatype'] = slowkmatype
    if option == 'slowdmatype' and slowdmatype is not None and slowdmatype in api_indicator_matype:
        parameters['slowdmatype'] = slowdmatype

    return parameters