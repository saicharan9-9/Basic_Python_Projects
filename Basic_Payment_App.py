class User:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance

    def show_balance(self):
        print(f"Your balance : ₹ {self.balance} ")

    def add_balance(self, amount):
        self.balance += amount
        print(f"₹ {amount} added to your balance. Your Balance: ₹{self.balance}")

    def send_money(self, receiver, amount):
        if amount <= self.balance:
            self.balance -= amount
            receiver.balance += amount
            print(f"""Transaction Successful!
₹{amount} sent to {receiver.name}
Your Balance : {self.balance}""")
        else:
            print("Insufficient Funds!")


User1 = User("Ram", 1000)
User2 = User("Suresh", 700)

while True:
    print("\n --- Payment App ---")
    print("1. Show Balance")
    print("2. Add Money")
    print("3. Send Money")
    print("4. Exit")

    choice = int(input("Enter choice: "))

    if choice == 1:
        User1.show_balance()
    elif choice == 2:
        amt = float(input("Enter your amount: "))
        User1.add_balance(amt)
    elif choice == 3:
        amt = float(input("Enter amount to send: "))
        User1.send_money(User2, amt)
    elif choice == 4:
        break
    else:
        print("Invalid choice!")
