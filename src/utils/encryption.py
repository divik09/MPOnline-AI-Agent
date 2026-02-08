"""Encryption utilities for sensitive user data."""
from cryptography.fernet import Fernet
from typing import Any
import json
import base64
from src import config


class DataEncryptor:
    """Handles encryption and decryption of user data."""
    
    def __init__(self):
        """Initialize encryptor with key from config."""
        if config.ENCRYPT_USER_DATA:
            # Generate key from provided encryption key
            key = config.ENCRYPTION_KEY.encode()
            # Ensure key is 32 bytes (use padding or hashing if needed)
            if len(key) < 32:
                key = key.ljust(32, b'0')
            elif len(key) > 32:
                key = key[:32]
            
            # Convert to valid Fernet key format
            self.key = base64.urlsafe_b64encode(key)
            self.cipher = Fernet(self.key)
        else:
            self.cipher = None
    
    def encrypt_data(self, data: dict) -> str:
        """
        Encrypt dictionary data to string.
        
        Args:
            data: Dictionary to encrypt
            
        Returns:
            Encrypted string
        """
        if not self.cipher or not config.ENCRYPT_USER_DATA:
            return json.dumps(data)
        
        json_str = json.dumps(data)
        encrypted = self.cipher.encrypt(json_str.encode())
        return encrypted.decode()
    
    def decrypt_data(self, encrypted_str: str) -> dict:
        """
        Decrypt string to dictionary data.
        
        Args:
            encrypted_str: Encrypted string
            
        Returns:
            Decrypted dictionary
        """
        if not self.cipher or not config.ENCRYPT_USER_DATA:
            return json.loads(encrypted_str)
        
        try:
            decrypted = self.cipher.decrypt(encrypted_str.encode())
            return json.loads(decrypted.decode())
        except Exception as e:
            # If decryption fails, assume it's unencrypted JSON
            return json.loads(encrypted_str)


# Global encryptor instance
encryptor = DataEncryptor()
