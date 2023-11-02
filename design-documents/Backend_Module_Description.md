# Description of each module in the backend (i.e., what the module does)
## Payment Ingestion:
1.	Receive Tokenized Payment information (card info, security code) and payment details (amount, merchant ID) from the user via the merchant interface.
2.	Encrypt payment information.
3.	Combine encrypted payment info and payment details into a Payment Object to be ready to be passed to the next stage, generate a unique payment ID and a timestamp for each Payment Object
4.	Insert Payment object into the database with pending state.
5.	Send payment object to job queue towards Payment Processor
## Payment Processor:
1.	Obtain Payment job from the queue and conduct inhouse payment validation (check card number length, security code length, etc.)
2.	Send validation request to merchant’s bank.
3.	If the validation request returned a failure response code, update the database with that  transaction ID to the declined state.
4.	Check the transaction type if the validation request returned a successful response code.
a.	If debit card, update database transaction to approved state.
b.	If credit card, update database transaction to in-process state
5.	Send payment object to Payment settlement module.
## Payment Settlement:
1.	Run at the end of each day.
2.	Run query from database to obtain transactions with in-progress state and filter out transactions ready to be converted to “approved” based on current timestamp and timestamp recorded, convert them to approved state.
3.	Send settlement requests for all approved transactions to the backend.  
