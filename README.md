MARC'S SUBSCRIBER WEB SERVER
Demonstrating REST API using Django

HOW TO TEST

Client Test Tool Used: 
HTTPie https://httpie.org/

============================================
FUNCTIONAL TEST SAMPLES
============================================
Requirement 1: User Subscriber Registration

Input:
http post http://127.0.0.1:8000/subscribers/ email_address="marc@company.com" password="marcpassword" first_name="Marc" last_name="Concepcion"

Output:
C:\>http post http://127.0.0.1:8000/subscribers/ email_address="marc@company.com" password="marcpassword" first_name="Marc" last_name="Concepcion"
HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 128
Content-Type: application/json
Date: Fri, 07 Aug 2020 01:50:43 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [],
    "user": {
        "email_address": "marc@company.com",
        "first_name": "Marc",
        "last_name": "Concepcion",
        "password": "marcpassword"
    }
}

============================================
Requirement 2: User Activation

Input:
http put http://127.0.0.1:8000/subscribers/15/ token=mAixZ120MtXUNtvIlzyjdjgblPDZGJ

Output:
C:\>http put http://127.0.0.1:8000/subscribers/15/ token=mAixZ120MtXUNtvIlzyjdjgblPDZGJ
HTTP/1.1 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 102
Content-Type: application/json
Date: Fri, 07 Aug 2020 01:52:08 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [],
    "user": {
        "email_address": "marc@company.com",
        "first_name": "Marc",
        "last_name": "Concepcion"
    }
}


Note: The activation field in the Subscribers Model API database is only internal to the server and should never be shown to the user clients. However, the activation flag has been set to True.
============================================
Requirement 3: User Login

Input:
http get http://127.0.0.1:8000/subscribers/15/ email_address="marc@company.com" password="marcpassword"

Output:
C:\Users\concepcion>http get http://127.0.0.1:8000/subscribers/15/ email_address="marc@company.com" password="marcpassword"
HTTP/1.1 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 63
Content-Type: application/json
Date: Fri, 07 Aug 2020 01:54:47 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [],
    "user": {
        "token": "nH754yMk648dOg0yKCYnv10Pa92BiH"
    }
}

============================================
Requirement 4: Users List
----------
Case 4-1: With Token
----------
Input:
http get http://127.0.0.1:8000/subscribers/ token=mAixZ120MtXUNtvIlzyjdjgblPDZGJ

Output:
C:\>http get http://127.0.0.1:8000/subscribers/ token=mAixZ120MtXUNtvIlzyjdjgblPDZGJ
HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 104
Content-Type: application/json
Date: Fri, 07 Aug 2020 02:03:41 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [],
    "user": [
        {
            "email_address": "marc@company.com",
            "first_name": "Marc",
            "last_name": "Concepcion"
        }
    ]
}

----------
Case 4-2: Without Token
----------
Input:
http get http://127.0.0.1:8000/subscribers/

Output:
C:\Users\concepcion>http get http://127.0.0.1:8000/subscribers/
HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 44
Content-Type: application/json
Date: Fri, 07 Aug 2020 02:05:00 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [],
    "user": [
        {
            "first_name": "Marc"
        }
    ]
}

============================================
Requirement 5: Change Password 

Input:
http patch http://127.0.0.1:8000/subscribers/15/ password="marcpassword" new_password="marcnewpassword" token=mAixZ120MtXUNtvIlzyjdjgblPDZGJ

Output:
C:\>http patch http://127.0.0.1:8000/subscribers/15/ password="marcpassword" new_password="marcnewpassword" token=mAixZ120MtXUNtvIlzyjdjgblPDZGJ
HTTP/1.1 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 131
Content-Type: application/json
Date: Fri, 07 Aug 2020 01:59:17 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [],
    "user": {
        "email_address": "marc@company.com",
        "first_name": "Marc",
        "last_name": "Concepcion",
        "password": "marcnewpassword"
    }
}
============================================

END
