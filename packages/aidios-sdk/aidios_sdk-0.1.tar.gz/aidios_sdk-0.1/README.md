######Aidios SDK for Python#######


This SDK for the AIDIOS API, provides an easy to use pyton interface. It allows you to retrieve and store data, get digest information, and confirm data transactions.

#Installation
Using Pip:
pip install aidios_sdk

#Dependencies
requests
json
(note json, and requests will be downloaded when you install aidios_sdk. 'requests' is only used in the example_usage.py


#Usage
#Importing the SDK
First, import the SDK in your Python script:

from aidios_sdk import AidiosAPI


##Initializing the API Client
You can initialize the API client as follows:

api = AidiosAPI()


###Retrieve Data
To retrieve data, use the retrieve method and pass in the data ID:

data_id = "some_data_id"
response = api.retrieve(data_id)
print("Retrieve Response:", response)

####Store Data
Use the store method and pass a file:


with open("path/to/file", "rb") as file:
    file_content = file.read()

data = {"file_content": file_content}
response = api.store(data)
print("Store Response:", response)


#####Get Digest
To get digest information, use the digest method:


data_id = "some_data_id"
response = api.digest(data_id)
print("Digest Response:", response)


######Get Confirmations
Check this number of transactions and associated stats for a given (root)txid:

transaction_id = "some_transaction_id"
response = api.confirmations(transaction_id)
print("Confirmations Response:", response)


#######Example Script
An example script demonstrating these functionalities is included in the examples/ directory.

To run the example:

python examples/example_usage.py

The test script will prompt you to perform each of the functions( store, retrieve, digest and confirmations.


Have fun with aidios!