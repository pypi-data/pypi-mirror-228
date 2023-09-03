import random
import string
import secrets, time
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256

class Token:
    def __init__(self, token, signed_token, name, signed_name):
        self.signed_token = signed_token
        self.token = token
        self.name = name
        self.signed_name = signed_name

    def __str__(self):
        return f"ntcdtkn<{self.signed_token}>"

    def Token(self):
        return f"ntcdtkn<{self.token}>"

    def token_with_name(self):
        return f"ntcdtkn<{self.token}:{self.name}>"
    def token_with_signed_name(self):
        return f"ntcdtkn<{self.token}:{self.signed_name}>"
    def signed_token_with_signed_name(self):
        return f"ntcdtkn<{self.signed_token}:{self.signed_name}>"
    def signed_token_with_name(self):
        return f"ntcdtkn<{self.signed_token}:{self.name}>"

class Grade:
    def __init__(self, grade):
        self.grade = grade


def generate_key():
    private_key = RSA.generate(2048)
    public_key = private_key.publickey()
    return public_key, private_key


def sign_token(token, private_key):
    h = SHA256.new(token.encode())
    signature = pkcs1_15.new(private_key).sign(h)
    return signature

def verify_token(token, signature, public_key):
    h = SHA256.new(token.encode())
    try:
        pkcs1_15.new(public_key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False 


MAXLENGTH=200
MINLENGTH=200
DEFAULT_CHARACTERS = string.ascii_letters + string.digits + string.punctuation

def calculate_complexity(password, log=False):
    length = len(password)
    has_lower = any(char.islower() for char in password)
    has_upper = any(char.isupper() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(char in string.punctuation for char in password)
    
    complexity = 0
    if length >= 8:
        complexity += 1
        if log:
            print("min length: yes")
    else:
        if log:
            print("min length: no")
    if length >= 12:
        complexity += 1
        if log:
            print("medium length: yes")
    else:
        if log:
            print("medium length: no")
    if has_lower and has_upper:
        complexity += 1
        if log:
            print("uppers and lowers: yes")
    else:
        if log:
            print("uppers and lowers: no")
    if has_digit:
        complexity += 1
        if log:
            print("digit: yes")
    else:
        if log:
            print("digit: no")
    if has_special:
        complexity += 1
        if log:
            print("specials: yes")
    else:
        if log:
            print("specials: no")

    Complexity = Grade(complexity)
    return Complexity

def complexity_word(complexity):
    try:
        if complexity.grade == 0:
            complexity = "too weak"
        elif complexity.grade  == 1:
            complexity = "weak"
        elif complexity.grade  in [2, 3]:
            complexity = "medium"
        elif complexity.grade  == 4:
            complexity = "good"
        elif complexity.grade  == 5:
            complexity = "perfect"
    except:
        complexity = "The grade need to be a Grade variable"
    
    return complexity

def setlength(min_length=None, max_length=None):
    global MAXLENGTH
    global MINLENGTH
    if min_length == None and not max_length == None:
        print("Please specify min_lenght")
        exit(1)
    elif not min_length == None and max_length == None:
        print("Please specify max_lenght")
        exit(1)
    elif min_length == None and max_length == None:
        print("Please specify min_lenght and max_lenght")
        exit(1)
    else:
        MAXLENGTH = max_length
        MINLENGTH = min_length

def generate_password(custom_characters=None):
    length = random.randint(MINLENGTH, MAXLENGTH)
    characters = custom_characters if custom_characters else DEFAULT_CHARACTERS
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def generate_token(name=None, minlength=160, maxlength=300):
    public_key, private_key=generate_key()
    if maxlength > 2000:
        print("Max length less than 2000")
        exit(1)
    if maxlength < 10:
        print("Max length more than 10")
        exit(1)
    
    timestamp = int(time.time() * 1000)  # Multiplicato per 1000 per ottenere millisecondi
    random_part = random.randint(0, 90000)
    unique_token = f"{timestamp}-"
    length = random.randint(minlength, maxlength)
    characters = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(characters + str(random_part)) for _ in range(length))
    
    signed_token = sign_token(token, private_key)  # Firma il token generato
    signed_name = sign_token(name, private_key)
    is_valid = verify_token(token, signed_token, private_key)

    token = Token(f"{token}", f"{signed_token}", f"{name}", f"{signed_name}")
    if is_valid:
        return token
    else:
        return "Unknown error"