from abc import ABC, abstractmethod
from datetime import datetime
import uuid

# 1. Abstraction: Abstract Base Class
class BankAccount(ABC):
    def __init__(self, account_holder: str, initial_balance: float = 0.0):
        self.account_number = str(uuid.uuid4())[:8].upper()
        self.account_holder = account_holder
        # 2. Encapsulation: Private attribute for balance
        self.__balance = initial_balance
        self.__transactions = []
        if initial_balance > 0:
            self._record_transaction("Initial Deposit", initial_balance)

    @property
    def balance(self) -> float:
        return self.__balance

    def _update_balance(self, amount: float):
        self.__balance += amount

    def _record_transaction(self, txn_type: str, amount: float):
        self.__transactions.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": txn_type,
            "amount": amount,
            "balance_after": self.__balance
        })

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._update_balance(amount)
        self._record_transaction("Deposit", amount)
        print(f"Deposited ₹{amount:.2f}. New Balance: ₹{self.__balance:.2f}")

    @abstractmethod
    def withdraw(self, amount: float):
        """Must be implemented by subclasses"""
        pass

    def get_transaction_history(self):
        print(f"\n--- Transaction History for {self.account_holder} ({self.account_number}) ---")
        for txn in self.__transactions:
            print(f"[{txn['timestamp']}] {txn['type']}: ₹{txn['amount']:.2f} | Balance: ₹{txn['balance_after']:.2f}")
        print("-" * 60)


# 3. Inheritance & 4. Polymorphism: SavingsAccount
class SavingsAccount(BankAccount):
    MIN_BALANCE = 500.0

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance - amount < self.MIN_BALANCE:
            print(f"Transaction Failed: Minimum balance of ₹{self.MIN_BALANCE:.2f} required.")
            return
        self._update_balance(-amount)
        self._record_transaction("Withdrawal", amount)
        print(f"Withdrew ₹{amount:.2f}. New Balance: ₹{self.balance:.2f}")


# 3. Inheritance & 4. Polymorphism: CurrentAccount (with Overdraft)
class CurrentAccount(BankAccount):
    def __init__(self, account_holder: str, initial_balance: float = 0.0, overdraft_limit: float = 5000.0):
        super().__init__(account_holder, initial_balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance + self.overdraft_limit < amount:
            print("Transaction Failed: Exceeds overdraft limit.")
            return
        self._update_balance(-amount)
        self._record_transaction("Withdrawal", amount)
        print(f"Withdrew ₹{amount:.2f}. New Balance: ₹{self.balance:.2f}")


# --- Example Usage ---
if __name__ == "__main__":
    # Creating Savings Account
    acc1 = SavingsAccount("Vinita Rao", 2000.0)
    acc1.deposit(1500.0)
    acc1.withdraw(2800.0)
    acc1.withdraw(500.0)  # Should fail due to min balance rule
    acc1.get_transaction_history()
  
