import tenseal as ts

class HEManager:
    def __init__(self):
        # Initialize BFV context for integer operations
        self.context = ts.context(
            ts.SCHEME_TYPE.BFV, poly_modulus_degree=8192, plain_modulus=1032193
        )
        self.context.generate_galois_keys()
        self.context.generate_relin_keys()

    def encrypt_choice(self, choice):
        """Encrypt a user's choice or the coin flip result."""
        return ts.bfv_vector(self.context, [choice])

    def compare_choices(self, encrypted_user, encrypted_coin):
        """Compare user choice and coin flip result."""
        # Subtract encrypted values; if result is 0, they match
        return encrypted_user - encrypted_coin

    def decrypt_result(self, encrypted_result):
        """Decrypt the comparison result."""
        result = encrypted_result.decrypt()
        return 1 if result[0] == 0 else 0  # 1 for win, 0 for lose
