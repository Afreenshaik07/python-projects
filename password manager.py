from cryptography.fernet import Fernet
import os

# ✅ STEP 1: Generate and save the key
def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    print("[+] New key generated and saved to key.key")

# ✅ STEP 2: Load the key (generate if not found)
def load_key():
    if not os.path.exists("key.key"):
        print("[!] key.key not found. Generating one...")
        write_key()
    with open("key.key", "rb") as key_file:
        return key_file.read()

# ✅ Load encryption key
key = load_key()
fer = Fernet(key)

# ✅ STEP 3: View all stored passwords
def view():
    try:
        with open('passwords.txt', 'r') as f:
            for line in f.readlines():
                if "|" not in line:
                    continue
                user, passw = line.strip().split("|")
                decrypted = fer.decrypt(passw.encode()).decode()
                print(f"User: {user} | Password: {decrypted}")
    except FileNotFoundError:
        print("[!] passwords.txt not found.")
    except Exception as e:
        print(f"[!] Error reading file: {e}")

# ✅ STEP 4: Add a new password
def add():
    name = input("Account Name: ")
    pwd = input("Password: ")
    encrypted = fer.encrypt(pwd.encode()).decode()
    with open("passwords.txt", "a") as f:
        f.write(name + "|" + encrypted + "\n")
    print("[+] Password added successfully.")

# ✅ STEP 5: Main loop
while True:
    print("\n[Password Manager]")
    mode = input("Would you like to (add), (view), or (q)uit? ").lower()

    if mode == "q":
        break
    elif mode == "add":
        add()
    elif mode == "view":
        view()
    else:
        print("[!] Invalid option. Please type 'add', 'view', or 'q'.")
