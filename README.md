# TrinityGo Online-payment Processing Platform (OPP)
- **Title:** Project ReadMe file
- **Course:** NEU CS5500 Fall 2023
- **Date:** Nov 2, 2023
- **Author:** Yiwen Wang, Xinyi Gao, Yijia Ma
- **Version:** 1.0

**Revision History**
|Date|Version|Description|Author|
|:----:|:----:|:----:|:----:|
|Nov 2, 2023|1.0|Initial release| Yiwen Wang|

## Deisgn Stage
**Design Documents**
- High Level Design:
    - [HLD_digram]:Diagram of our overall architecture
    - [Backend_Module_Description]: Description of each of our backend modules
    - [Wireframes_UI]: Wireframes of our UI
- Low Level Deisgn:
    - [ER_Diagram]:Entity Relationship Diagram of our database
    - [API_Sequence_Diagram]: Sequence Diagram of each ReST API
    - [ReST_API_Design]: ReST API design
    - [Backend_Module_Functional_Logic]:Description of how each backend module performs its job with class UML

**High Level Design**
- Architecture
![HLD](https://github.com/TrinityGo/opp-api/blob/main/design-documents/HLD.JPG)

**Low Level Design**
- ER Diagram:
![ER_Diagram_show](https://github.com/TrinityGo/opp-api/blob/main/design-documents/ER_Diagram_for_Online_Payment_System.jpeg)
- API Sequence Diagram:
![API_Sequence](https://github.com/TrinityGo/opp-api/blob/main/design-documents/Sequence_Diagram/Sequence_Diagram1.png)
- Backend Drafted functionality logic Class UML:
```mermaid
---
title: OPP Backend
---
classDiagram
      class User {
          +Integer ID
          +String Email
          +String HashedPassword
          +Decimal Balance
          +ValidateCredentials(email, password) Boolean
          +UpdateProfile(profileData)
          +AddPaymentMethod(paymentMethod)
      }
      class PaymentMethod {
          +Integer ID
          +Integer UserID
          +String CardNumber
          +Date ExpiryDate
          +Integer CVV
          +Validate() Boolean
      }
      class Transaction {
          +Integer ID
          +Integer UserID
          +Decimal Amount
          +String Status
          +DateTime Timestamp
          +LogSuccess()
          +LogFailure()
      }
      class Session {
          +String Token
          +Integer UserID
          +DateTime ExpiresAt
          +IsValid() Boolean
          +Invalidate()
      }
      class AuthenticationService {
          +Authenticate(email, password) Session
          +Logout(sessionToken)
      }
      class PaymentService {
          +InitiatePayment(paymentDetails) PaymentResult
          +ProcessPayment(transaction) PaymentResult
      }
      class TransactionService {
          +CreateTransaction(user, paymentDetails) Transaction
          +GetTransactionHistory(user) Transaction[]
      }
      class UserService {
          +GetUserDetails(userId) User
          +UpdateUserBalance(user, amount)
      }
      class SecurityService {
          +HashPassword(password) String
          +VerifyPassword(password, hash) Boolean
          +GenerateToken(userId) String
          +EncryptData(data) String
      }

      User "1" *-- "many" PaymentMethod : has
      User "1" *-- "many" Transaction : has
      Transaction "n" -- "1" PaymentService : is processed by
      Session "n" -- "1" AuthenticationService : is created by
      PaymentMethod "1" -- "1" SecurityService : is validated by
```

----------------

## Introduction
- *This is a course project for NEU CS5500 all the descriptions below is a mock situation for our project with course project requirments.*


Welcome to the repository for our innovative Online Payment Processing Platform (OPP). Our startup(course project), comprising a dedicated team of business development consultants, solutions architects, and software engineers, is on the cutting edge of digital payment solutions. Having secured Series-B funding, we are excited to develop a robust platform designed to facilitate online transactions for consumers and businesses, providing a superior alternative to traditional point-of-sale systems.


Our mission is to deliver a state-of-the-art platform that rivals established services such as PayPal, Square, and Stripe, catering to a diverse clientele that includes software developers and small-to-medium-sized business owners.

## Objective
The primary goal of this project is to architect and implement the backend infrastructure necessary to support RESTful APIs for our platform. Concurrently, we aim to create a streamlined frontend interface that offers an intuitive user experience.

## Target Users
- **Software Developers:** We offer well-documented REST APIs that are easy to integrate, empowering developers to build seamless payment applications on top of our platform.
- **Business Owners:** Our platform promises a hassle-free transition from traditional POS systems to a user-friendly web application for managing transactions.

## Core Features
Our software system is engineered to support the following functionalities:
- **Processing Transactions:** Securely process credit card charges for customer purchases.
- **Balance Calculations:**
    - Provide real-time calculations of the total balance from fully processed funds.
    - Calculate and report the total balance over specified time periods.
- **Transaction Management:**
    - Retrieve comprehensive lists of all transactions affecting the total balance.
    - Track accounts receivables, including pending purchases.
- **Fraud Detection:** Utilize rigorous validation processes to identify and reject fraudulent credit card transactions.
- **Funds Verification:** Ensure debit cards have sufficient funds before authorizing purchases.
- **Account Management:** Enable users to create and manage their accounts with the platform seamlessly.


## Requirements
- Debit Card Transactions: Must be instantly processed, bypassing delays commonly associated with the banking system.
- Credit Card Transactions: Require a minimum of two calendar days in the processing state before reflecting in the total balance as 'processed'.
- Card Validation: Implement the Lund Algorithm for credit card number validation as part of our commitment to security and authenticity.
- Security Measures:
    - Mandatory user authentication to safeguard against unauthorized access.
    - Enforce encryption and other security protocols for data transmission to ensure confidentiality and integrity.

## Security & Compliance
Security is not just a feature; it is the foundation of our platform. We are deeply committed to protecting our users and their data through industry-standard practices and compliance with regulatory requirements.


<!-- auto references -->
[ReST_API_Design]: https://github.com/TrinityGo/opp-api/blob/main/design-documents/ReST_API_design.md
[HLD_digram]:https://github.com/TrinityGo/opp-api/blob/main/design-documents/HLD.JPG
[Backend_Module_Description]: https://github.com/TrinityGo/opp-api/blob/main/design-documents/Backend_Module_Description.md
[ER_Diagram]:https://github.com/TrinityGo/opp-api/blob/main/design-documents/ER_Diagram_for_Online_Payment_System.jpeg
[Backend_Module_Functional_Logic]:https://github.com/TrinityGo/opp-api/blob/main/design-documents/Backend_Module_Functional_Logic.md
[API_Sequence_Diagram]: https://github.com/TrinityGo/opp-api/blob/main/design-documents/Sequence_Diagram/Sequence_Diagram1.png
[Wireframes_UI]:
