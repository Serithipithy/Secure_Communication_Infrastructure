# se genereaza ciphertextul pentru un singur bloc de text cu xor pe vectorul de initailizare si cheie, apoi pe bloc
def xor_ofb(block, iv, key):
    iv_xor_key = bytes(a ^ b for (a, b) in zip(iv, key))
    ciphertext = bytes(a ^ b for (a, b) in zip(block, iv_xor_key))
    return ciphertext


class OfbMode:
    def __init__(self, init_vector, key):
        self.init_vector = init_vector
        self.key = key

    def encryption(self, plaintext):
        ciphertext = b''
        init_vector = self.init_vector

        # vor fi luati primii 16 biti din plaintext pentru a genera ciphertextul pentru acel bloc si se vor sterge
        # acestia pentru a continua criptarea restului de text si tot odata se va actualiza vectorul de initializare
        while plaintext:
            block = plaintext[0:16]
            plaintext = plaintext[16:]

            encrypt_result = xor_ofb(block, self.init_vector, self.key)
            init_vector = bytes(a ^ b for (a, b) in zip(init_vector, self.key)) # actualizam vectorul de initializare

            ciphertext = ciphertext + encrypt_result
        return ciphertext

    def decryption(self, ciphertext):
        plaintext = b''
        init_vector = self.init_vector

        # asemenea criptarii se va genera plaintextul din ciphertext pentru decriptare luand blocuri de cate 16 biti
        while ciphertext:
            block = ciphertext[0:16]
            plaintext = ciphertext[16:]

            decrypt_result = xor_ofb(block, self.init_vector, self.key)
            init_vector = bytes(a ^ b for (a, b) in zip(init_vector, self.key)) # actualizam vectorul de initializare

            plaintext = plaintext + decrypt_result
        return plaintext
