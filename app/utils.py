from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password) :
    return pwd_context.verify(plain_password, hashed_password)

def format_mac(hex_mac):
    clean_mac = hex_mac.replace(" ", "")
    formatted_mac = ":".join([clean_mac[i:i+2] for i in range(0, len(clean_mac), 2)])
    return formatted_mac
