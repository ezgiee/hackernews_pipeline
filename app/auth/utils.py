from passlib.context import CryptContext

# CryptContext is initialized to use bcrypt hashing for password encryption
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash a plain text password using bcrypt
def hash_password(password: str) -> str:
    """
    Hashes a plain text password using bcrypt.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

# Verify if the plain text password matches the hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against a hashed password.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)
