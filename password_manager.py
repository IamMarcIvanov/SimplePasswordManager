import string, random
import pyperclip as pc

# index in pwd_mgr + 1 = No value

path = r"D:\Mimisbrunnr\The Eye of Odin\The Keys Copy.txt"
with open(path, "r") as f:
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


def search(s="", name_given=False):
    if not name_given:
        s = input("Enter string to search for: ")
    matched_records = []
    for ind, name in enumerate(pwd_mgr["NAME"]):
        if name.lower().strip().find(s.lower().strip()) != -1:
            matched_records.append(ind)
    if len(matched_records) == 0:
        print("No record found with that substring in name.")
    else:
        print("The following records were found: ")
        for i in matched_records:
            for col_name in cols:
                print("{:>20}: {}".format(col_name, pwd_mgr[col_name][i]))
            print()
        if not name_given:
            choice = input("Enter No of record whose password you want to copy to clipboard (-1 if none): ")
            try:
                if int(choice) - 1 in matched_records:
                    pc.copy(pwd_mgr["PASSWORD"][int(choice) - 1])
                    print("Successfully added the requested password to clipboard.")
                else:
                    print("You have hosen not to copy anything to clipboard.")
            except ValueError:
                print("Invalid input.")
    return matched_records


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
    write_string = ""
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
    if insertion[0] == "No":
        open(path, "w").close()
        with open(path, "a") as f:
            f.write(write_string.strip())
    else:
        with open(path, "a") as f:
            f.write("\n" + write_string.strip())


def insert():
    insertion = [str(len(pwd_mgr["No"]) + 1)]
    for col_name in cols[1:]:
        if col_name == "NAME":
            s = input("Enter NAME: ")
            print("Checking if entry already exists:")
            if search(s, name_given=True):
                print("Entry already exists. Either delete and re-enter or update.")
                return
            else:
                print("Confirmed that entry is new. Name accepted.")
                insertion.append(s)
        elif col_name == "PASSWORD":
            choice1 = input(
                "For PASSWORD enter either 1 or 2:\n1. Enter password\n2. Generate password\n"
            )
            if choice1 == "2":
                pwd = generate_password()
                insertion.append(pwd)
            elif choice == "1":
                s = input("Enter {}: ".format(col_name))
                insertion.append(s)
            else:
                print("Only enter 1 or 2. No other input accepted")
                return
            if input("Enter 1 if you want to add the password to clipboard: ") == "1":
                pc.copy(insertion[-1])
                print("Password successfully copied to clipboard")
        elif col_name == "EMAIL":
            email = [
                "lordheisenbergpoirot@gmail.com",
                "f20180103@hyderabad.bits-pilani.ac.in",
                "marcivanovofearth@gmail.com",
            ]
            choice = input(
                "For EMAIL enter 1, 2, 3 or 4:\n1. "
                + email[0]
                + "\n2. "
                + email[1]
                + "\n3. "
                + email[2]
                + "\n4. Enter email\n"
            )
            if choice in ["1", "2", "3"]:
                print("You have chosen email as:", email[int(choice) - 1])
                insertion.append(email[int(choice) - 1])
            elif choice == "4":
                s = input("Enter {}: ".format(col_name))
                insertion.append(s)
            else:
                print("Only enter 1, 2, 3 or 4. No other input accepted")
                return
        else:
            s = input("Enter {}: ".format(col_name))
            insertion.append(s)
    add_to_file(insertion)
    add_to_pwd_mgr(insertion)

    print("\nThe data that has been entered is:")
    for val, col_name in zip(insertion, cols):
        print("{:>20}: {}".format(col_name, val))
    print()


def add_to_pwd_mgr(insertion):
    for data, col_name in zip(insertion, cols):
        pwd_mgr[col_name].append(data)


def delete():
    matched_records = search()
    if matched_records:
        choice = input(
            "If (any of) the above record(s) match(es) the one you want to delete, enter its 'No' else enter -1: "
        )
        if int(choice) - 1 in matched_records:
            print("The record you have chosen to delete is:")
            for col_name in cols:
                print("{:>20}: {}".format(col_name, pwd_mgr[col_name][int(choice) - 1]))
            if (
                int(
                    input(
                        "Enter 1 if you are ABSOLUTELY SURE about deleting this entry: "
                    )
                )
                == 1
            ):
                add_to_file(cols)
                ind = 0
                del_ind = -1
                while ind < len(pwd_mgr["No"]):
                    if ind + 1 < int(choice):
                        add_to_file([pwd_mgr[col_name][ind] for col_name in cols])
                    elif ind + 1 == int(choice):
                            pwd_mgr[col_name][ind] = "00"
                            del_ind = ind
                    else:
                        pwd_mgr["No"][ind] = str(ind)
                        add_to_file([pwd_mgr[col_name][ind] for col_name in cols])
                    ind += 1
                if del_ind != -1:
                    for col_name in cols:
                        pwd_mgr[col_name].pop(del_ind)
                    print("The chosen record has been deleted.\n")
                else:
                    print("There has been some error.\n")
        else:
            print("Wrong input.")
        
print("PASSWORD MANAGER".center(26, "-"))
flag = True
while flag:
    choice = input("\nEnter 1, 2, 3 or 4:\n1. Search\n2. Insert\n3. Delete\n4. Exit\n")
    if choice == "1":
        print("You have chosen to SEARCH")
        search()
    elif choice == "2":
        print("You have chosen to INSERT")
        insert()
    elif choice == "3":
        print("You have chosen to DELETE")
        delete()
    elif choice == "4":
        print("You have chosen to EXIT")
        print("Bye!".center(26, "-"))
        flag = False
    else:
        print("Enter only 1, 2 or 3. No other input accepted.")
