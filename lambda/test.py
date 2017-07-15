from xero                 import Xero
from xero.auth            import PublicCredentials
import sys

xero_credentials = {
    "key" : "TTRAOBPOHHZV5ZBFYX5YUMYF9SQN05",
    "secret" : "FMLLGRJTEZWQXAO5IPY8ZEQYNFMZLW"
}

credentials = PublicCredentials(xero_credentials["key"], xero_credentials["secret"])
print credentials.url
inpVerificationString = input("Please enter verification string: ")
credentials.verify(str(inpVerificationString))
xe = Xero(credentials)
print xe.invoices.all()