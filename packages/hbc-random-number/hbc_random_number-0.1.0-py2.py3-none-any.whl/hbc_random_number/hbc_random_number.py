"""Main module."""
import hashlib
import hmac


class ProvablyFairRandomNumberGenerator:
    def __init__(self, secret_key):
        self.secret_key = secret_key.encode()

    def generate_random_number(self, user_seed, min_value, max_value):
        combined_seed = user_seed.encode() + self.secret_key
        hmac_sha256 = hmac.new(self.secret_key, combined_seed, hashlib.sha256)
        hexdigest = hmac_sha256.hexdigest()
        scaled_random = min_value + (int(hexdigest, 16) % (max_value - min_value + 1))
        return scaled_random
