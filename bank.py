class Account:
    def __init__(self, account_number, holder_name, balance=0):
        self._account_number = account_number
        self._holder_name = holder_name
        self._balance = balance

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print(f"Deposited {amount}. New balance: {self._balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > 0 and amount <= self._balance:
            self._balance -= amount
            print(f"Withdrew {amount}. New balance: {self._balance}")
        elif amount > self._balance:
            print("Insufficient balance.")
        else:
            print("Withdrawal amount must be positive.")

    def check_balance(self):
        print(f"Account Balance: {self._balance}")

    def __str__(self):
        return f"Account({self._account_number}, Holder: {self._holder_name}, Balance: {self._balance})"

class SavingsAccount(Account):
    def __init__(self, account_number, holder_name, balance=0, interest_rate=0.02):
        super().__init__(account_number, holder_name, balance)
        self._interest_rate = interest_rate

    def calculate_interest(self):
        interest = self._balance * self._interest_rate
        print(f"Interest for this period: {interest}")
        return interest

class CurrentAccount(Account):
    def __init__(self, account_number, holder_name, balance=0, overdraft_limit=500):
        super().__init__(account_number, holder_name, balance)
        self._overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > 0 and (self._balance - amount >= -self._overdraft_limit):
            self._balance -= amount
            print(f"Withdrew {amount}. New balance: {self._balance}")
        elif amount > 0:
            print("Overdraft limit exceeded.")
        else:
            print("Withdrawal amount must be positive.")

class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = {}

    def create_account(self, account_type, account_number, holder_name, balance=0, **kwargs):
        if account_number in self.accounts:
            print("Account number already exists.")
            return None

        if account_type == "Savings":
            account = SavingsAccount(account_number, holder_name, balance, kwargs.get('interest_rate', 0.02))
        elif account_type == "Current":
            account = CurrentAccount(account_number, holder_name, balance, kwargs.get('overdraft_limit', 500))
        else:
            print("Invalid account type.")
            return None

        self.accounts[account_number] = account
        print(f"Account created: {account}")
        return account

    def get_account(self, account_number):
        return self.accounts.get(account_number, None)

# Example usage:
if __name__ == "__main__":
    # Create a bank
    my_bank = Bank("MyBank")

    # Create accounts
    savings = my_bank.create_account("Savings", "001", "Alice", balance=1000, interest_rate=0.03)
    current = my_bank.create_account("Current", "002", "Bob", balance=500, overdraft_limit=1000)

    # Perform operations
    if savings:
        savings.deposit(500)
        savings.calculate_interest()
        savings.withdraw(300)
        savings.check_balance()

    if current:
        current.deposit(200)
        current.withdraw(800)  # Overdraft allowed
        current.withdraw(1000)  # Overdraft limit exceeded
        current.check_balance()
