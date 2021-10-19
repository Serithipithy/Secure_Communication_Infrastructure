# se genereaza ciphertextul pentru un singur bloc de text
from Crypto.Cipher import AES


# def xor_ecb(block, key):
#     ciphertext = bytes(a ^ b for (a, b) in zip(block, key))
#     return ciphertext


class EcbMode:
    def __init__(self, key):
        self.key = key

    def encryption(self, plaintext):
        ciphertext = b''
        padding = 16 - len(plaintext) % 16
        plaintext = plaintext + bytes([padding] * padding) #adauga padding

        # vor fi luati primii 16 biti din plaintext pentru a genera ciphertextul pentru acel bloc si se vor sterge
        # acestia pentru a continua criptarea restului de text
        while plaintext:
            block = plaintext[0:16]
            plaintext = plaintext[16:]

            # encrypt_result = xor_ecb(block, self.key)
            aes = AES.new(self.key, AES.MODE_ECB)
            encrypt_result = aes.encrypt(block)

            ciphertext += encrypt_result

        return ciphertext

    def decryption(self, ciphertext):
        if len(ciphertext) % 16 != 0 :
            print('incorrect ciphertext')
            return
        plaintext = b''

        # asemenea criptarii se va genera plaintextul din ciphertext pentru decriptare luand blocuri de cate 16 biti
        while ciphertext:
            block = ciphertext[0:16]
            ciphertext = ciphertext[16:]

            # decrypt_result = xor_ecb(block, self.key)
            aes = AES.new(self.key, AES.MODE_ECB)
            decrypt_result = aes.decrypt(block)

            plaintext += decrypt_result

        # cauta padding in cazul in care exista
        count = 0
        current_pad = 0
        for c in plaintext[-16:]:
            if c != current_pad:
                current_pad = c
                count = 1
            else:
                count += 1
        if count != current_pad:
            print('Incorrect padding')
            return
        return plaintext[:-count]
        # return plaintext
