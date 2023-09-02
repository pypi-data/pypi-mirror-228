class esat:
    def __init__(self, tem):
        self.tem = tem

    def hitung_saturasi(self):
        import math

        #saturation water vapor pressure
        return 611.21 * math.exp(17.502*((self.tem - 273.16)/(self.tem - 32.19)))