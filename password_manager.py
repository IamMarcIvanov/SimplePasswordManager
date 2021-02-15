import string, random

file_path = '' # put in the path to the file that stores the passwords
with open(file_path, "r") as f:
    cols = ["No", "NAME", "USERNAME", "EMAIL", "PASSWORD", "NOTES"]
    col_nos = []
    pwd_mgr = {col_name: [] for col_name in cols}
    for line_nos, line in enumerate(f.readlines()):
        if line_nos == 0:
            col_nos = [line.index(col_name) for col_name in cols]
            col_nos.append(1000)
        else:
            for i, col_name in enumerate(cols):
                pwd_mgr[col_name].append(line[col_nos[i] : col_nos[i + 1]].strip())


def search():
    s = input("Enter string to search for: ")
    for ind, names in enumerate(pwd_mgr["NAME"]):
        if names.lower().find(s.lower()) != -1:
            for col_name in cols[1:]:
                print("{:>10}: {}".format(col_name, pwd_mgr[col_name][ind]))
            print()


def generate_password():
    length = int(input("{:>42}".format("Enter total length: ")))
    min_digits = int((input("{:>42}".format("Enter minimum nos of digits: "))))
    min_upcases = int(
        (input("{:>42}".format("Enter minimum nos of uppercase letters: ")))
    )
    min_lowcases = int(
        (input("{:>42}".format("Enter minimum nos of lowercase letters: ")))
    )
    min_spchars = int(
        (input("{:>42}".format("Enter minimum nos of special characters: ")))
    )

    min_sum = min_digits + min_upcases + min_lowcases + min_spchars
    if min_sum > length:
        print("Error: Sum of least > length")
    else:
        all_allowed = ""
        if min_digits:
            all_allowed += string.digits
        if min_upcases:
            all_allowed += string.ascii_uppercase
        if min_lowcases:
            all_allowed += string.ascii_lowercase
        if min_spchars:
            all_allowed += string.punctuation

        digits = random.choices(string.digits, k=min_digits)
        upcases = random.choices(string.ascii_uppercase, k=min_upcases)
        lowcases = random.choices(string.ascii_lowercase, k=min_lowcases)
        spchars = random.choices(string.punctuation, k=min_spchars)

        password_elements = digits + upcases + lowcases + spchars
        password_elements += random.choices(all_allowed, k=length - min_sum)
        random.shuffle(password_elements)
        return "".join(password_elements)


def add_to_file(insertion):
    write_string = "\n"
    used = 0
    for i, item in enumerate(insertion):
        write_string += item
        used += len(item)
        nos_spaces = col_nos[i + 1] - used
        if nos_spaces <= 0:
            print("Error: item too large")
            break
        used += nos_spaces
        write_string += " " * nos_spaces
    with open(file_path, "a") as f:
        f.write(write_string)


def insert():
    insertion = [str(len(pwd_mgr["No"]) + 2)]
    for col_name in cols[1:]:
        if col_name == "PASSWORD":
            choice = input(
                "Enter either 1 or 2:\n1. Enter password\n2. Generate password\n"
            )
            if choice == "2":
                pwd = generate_password()
                insertion.append(pwd)
            elif choice == "1":
                s = input("Enter {}: ".format(col_name))
                insertion.append(s)
            else:
                print("Only enter 1 or 2. No other input accepted")
                return
        else:
            s = input("Enter {}: ".format(col_name))
            insertion.append(s)
    add_to_file(insertion)

    print("\nThe data that has been entered is:")
    for val, col_name in zip(insertion, cols):
        print("{:>20}: {}".format(col_name, val))
    print()


print("PASSWORD MANAGER".center(26, "-"))
flag = True
while flag:
    choice = input("Enter 1, 2 or 3:\n1. Search\n2. Insert\n3. Exit\n")
    if choice == "1":
        search()
    elif choice == "2":
        insert()
    elif choice == "3":
        print("Bye!".center(26, "-"))
        flag = False
    else:
        print("Enter only 1, 2 or 3. No other input accepted.")
