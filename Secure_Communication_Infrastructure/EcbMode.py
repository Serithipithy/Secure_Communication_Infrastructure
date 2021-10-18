# se genereaza ciphertextul pentru un singur bloc de text
def xor_ecb(block, key):
    ciphertext = bytes(a ^ b for (a, b) in zip(block, key))
    return ciphertext


class EcbMode:
    def __init__(self, key):
        self.key = key

    def encryption(self, plaintext):
        ciphertext = b''

        # vor fi luati primii 16 biti din plaintext pentru a genera ciphertextul pentru acel bloc si se vor sterge
        # acestia pentru a continua criptarea restului de text
        while plaintext:
            block = plaintext[0:16]
            plaintext = plaintext[16:]

            encrypt_result = xor_ecb(block, self.key)
            ciphertext = ciphertext + encrypt_result

        return ciphertext

    def decryption(self, ciphertext):
        plaintext = b''

        # asemenea criptarii se va genera plaintextul din ciphertext pentru decriptare luand blocuri de cate 16 biti
        while ciphertext:
            block = ciphertext[0:16]
            ciphertext = ciphertext[16:]

            decrypt_result = xor_ecb(block, self.key)
            plaintext = plaintext + decrypt_result

        return plaintext
