__author__ = 'fmca'

def clear_dobson_paddy(relevance, accuracy):
    """
    Calculate the certainity level using the approach presented in
    Clear, Adrian K., Simon Dobson, and Paddy Nixon.
    "An approach to dealing with uncertainty in context-aware pervasive systems."
    UK/IE IEEE SMC Cybernetic Systems Conference. 2007.
    :param relevance: relevance of the result (scale: 0..1)
    :param accuracy: accuracy of the sensor data
    :return: certainty level
    """
    return accuracy + (relevance * accuracy)

