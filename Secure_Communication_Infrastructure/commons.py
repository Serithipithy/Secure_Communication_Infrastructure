from Crypto.Cipher import AES

KPrime = b'\xfce\xf8$fU\xfd3\xc1x\xb9\x82{\xb6\x12\xcd'
init_vector = b'\xfce\xf8$fU\xb6\x12\xb9\x82{\xfd3\xc1x\xcd'


def AES_decrypt_key(key):
    aes = AES.new(KPrime, AES.MODE_ECB)
    decr_key = aes.decrypt(key)
    return decr_key
