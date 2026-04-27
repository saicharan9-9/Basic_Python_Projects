import random
import string

passwords = {}

try : 
    with open('passwords.txt','r') as file:
        for line in file:
            web , pwd  = line.strip().split(':')
            passwords[web] = pwd
except:
    pass        


    
def password_generator():
    chars = string.ascii_letters + string.digits + '!@#$%^&*(_+-)/*.<>?[]`~'
    password = ''
    for i in range(8):
        password += random.choice(chars)
    return password
    

while True:
    print("""--------PASSWORD MANAGER ----------
         1.Save Password
         2.View Passwords
         3.Generate Password
         4.Exit""")
    
    choice = input("Enter Your Choice : ")

    if choice == '1':
            website = input("Enter Website Name : ")
            password = input("Enter Password : ")
            passwords[website] = password
            with open('passwords.txt','a') as file:
                 file.write(f'{website}:{password}\n')
            print('Password Saved Successfully !')     

    elif choice == '2':    
            if not passwords:
                 print('No Passwords are Saved Yet !')
            else:
                 for web , pwd in passwords.items():
                      print(f'Website Name : {web}\nPassword : {pwd}')     
    elif choice == '3':
           print("Password : ",password_generator())
    elif choice == '4':
         print("Ok bye !")
         break
    else :
         print("Invalid Input , Give Correct Input !")