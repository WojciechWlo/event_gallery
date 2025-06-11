import bcrypt

plain_phrase = input("Input phrase to hash: ")

hashed_phrase = bcrypt.hashpw(plain_phrase.encode(), bcrypt.gensalt())

print("Hashed phrase:")
print(hashed_phrase.decode())