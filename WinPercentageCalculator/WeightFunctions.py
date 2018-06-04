import math


class WeightFunctions:
    """
    Class containing a different types of weight functions:
    - identity
    - polynomial
    - exponential
    """

    @staticmethod
    def polynomial(x, coef):
        """
        Given the input, x and the coefficients of the polynomial, evaluates and returns the value of
        the polynomial function (f(x) = a_0 * x^0 + a_1 * x^1 + ... + a_i * x^i + ... + a_n * x^n)
        """
        value = 0  # initialize the polynomial value to zero
        for coef_idx in range(len(coef)):  # for every coefficient
            value += coef[coef_idx] * math.pow(x, coef_idx)  # add the current term to the value
        return value  # return the total value

    @staticmethod
    def identity(x, coef):
        """
        Given the input, x and the coefficients, returns the input value as the output (f(x) = x)
        """
        return x  # return the input value

    @staticmethod
    def exponential(x, coef):
        """
        Given the input, x and the coefficients of the polynomial in the exponent, evaluates and returns the
        value of the exponential function (f(x) = e^(a_0 * x^0 + a_1 * x^1 + ... + a_i * x^i + ... + a_n * x^n))
        """
        # evaluate and return the value of the exponential function
        return math.exp(WeightFunctions.polynomial(x, coef))
