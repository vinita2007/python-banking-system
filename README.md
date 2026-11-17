# Object-Oriented Python Banking System

## Overview
A clean-architecture Banking System built in Python demonstrating the four pillars of Object-Oriented Programming (OOP): Abstraction, Encapsulation, Inheritance, and Polymorphism.

## Class Diagram

```mermaid
classDiagram
    class BankAccount {
        <<Abstract>>
        +String account_number
        +String account_holder
        -Float __balance
        -List __transactions
        +balance() Float
        +deposit(amount: Float)
        +withdraw(amount: Float)*
        +get_transaction_history()
        #_update_balance(amount: Float)
        #_record_transaction(type: String, amount: Float)
    }

    class SavingsAccount {
        +Float MIN_BALANCE = 500.0
        +withdraw(amount: Float)
    }

    class CurrentAccount {
        +Float overdraft_limit
        +withdraw(amount: Float)
    }

    BankAccount <|-- SavingsAccount : Inherits
    BankAccount <|-- CurrentAccount : Inherits
