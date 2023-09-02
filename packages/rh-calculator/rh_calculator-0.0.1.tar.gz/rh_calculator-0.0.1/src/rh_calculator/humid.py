from esat import esat 

val_d = float(input("Enter dew point at 2 m (in Kelvin): "))
# print("d2m = ", val_d)
# e.g.: 297

val_t = float(input("Enter temperature at 2 m (in Kelvin): "))
# print("t2m = ", val_t)
# e.g. : 300

def hitung_rh(val_d, val_t):
    esat_d = esat(val_d)
    esat_t = esat(val_t)
    relhum = 100 * esat.hitung_saturasi(esat_d) / esat.hitung_saturasi(esat_t)
    return round(relhum,1)
    # print("Relative Humidity (%) = ",  round(relhum, 1))

y = hitung_rh(val_d, val_t)
print("Relative Humidity = ", y, "%")
# If d2m = 297 and t2m = 300, then relative humidity = 83.7 %