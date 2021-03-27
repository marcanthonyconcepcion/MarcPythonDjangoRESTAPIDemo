# MARC'S SUBSCRIBER WEB SERVER
### Demonstrating REST API using Django

## HOW TO TEST

Client Test Tool Used: 
HTTPie https://httpie.org/

## FUNCTIONAL TEST SAMPLES

### Requirement 1: User Subscriber Registration

#### Case 1-1: E-mail Address, Password, First Name, Last Name provided
```
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
```
#### Case 1-2: Only E-mail Address, Password provided
```
C:\>http post http://127.0.0.1:8000/subscribers/ email_address="kevin@company.com" password="kevinpassword"

HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 116
Content-Type: application/json
Date: Fri, 07 Aug 2020 03:09:15 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [],
    "user": {
        "email_address": "kevin@company.com",
        "first_name": "",
        "last_name": "",
        "password": "kevinpassword"
    }
}
```
### Requirement 2: User Activation
```
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
```
Note: The activation field in the Subscribers Model API database is only internal to the server and should never be shown to the user clients. However, the activation flag has been set to True.

### Requirement 3: User Login
```
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
```
### Requirement 4: Users List

#### Case 4-1: With Token
```
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
```
```
C:\>http get http://127.0.0.1:8000/subscribers/ token=mAixZ120MtXUNtvIlzyjdjgblPDZGJ

HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 248
Content-Type: application/json
Date: Fri, 07 Aug 2020 04:12:10 GMT
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
        },
        {
            "email_address": "kevin@company.com",
            "first_name": "",
            "last_name": ""
        },
        {
            "email_address": "roy@company.com",
            "first_name": "Roy",
            "last_name": "Berry"
        }
    ]
}
```
#### Case 4-2: Without Token
```
C:\>http get http://127.0.0.1:8000/subscribers/

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
```
```
C:\>http get http://127.0.0.1:8000/subscribers/

HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 83
Content-Type: application/json
Date: Fri, 07 Aug 2020 04:12:45 GMT
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
        },
        {
            "first_name": ""
        },
        {
            "first_name": "Roy"
        }
    ]
}
```
### Requirement 5: Change Password 
```
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
```
## ERROR SCENARIOS

### Error 1: Attempt to delete a subscriber which is not part of the requirements.
```
C:\>http delete http://127.0.0.1:8000/subscribers/15/

HTTP/1.1 405 Method Not Allowed
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 103
Content-Type: application/json
Date: Fri, 07 Aug 2020 02:47:48 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "email_address": [
                "Deleting your account through this API is not allowed."
            ]
        }
    ],
    "user": "null"
}
```
### Error 2: Attempts to access a non-existent user ID
```
C:\>http get http://127.0.0.1:8000/subscribers/100/ email_address="marc@company.com" password="marcpassword"

HTTP/1.1 404 Not Found
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 75
Content-Type: application/json
Date: Fri, 07 Aug 2020 02:51:29 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "email_address": [
                "Subscriber does not exist."
            ]
        }
    ],
    "user": "null"
}
```
```
C:\>http put http://127.0.0.1:8000/subscribers/100/ token=mAixZ120MtXUNtvIlzyjdjgblPDZGJ

HTTP/1.1 404 Not Found
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 75
Content-Type: application/json
Date: Fri, 07 Aug 2020 02:55:25 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "email_address": [
                "Subscriber does not exist."
            ]
        }
    ],
    "user": "null"
}
```
```
C:\>http patch http://127.0.0.1:8000/subscribers/100/ password="marcpassword" new_password="marcnewpassword" token=mAixZ120MtXUNtvIlzyjdjgblPDZGJ

HTTP/1.1 404 Not Found
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 75
Content-Type: application/json
Date: Fri, 07 Aug 2020 02:57:49 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "email_address": [
                "Subscriber does not exist."
            ]
        }
    ],
    "user": "null"
}
```
```
C:\>http delete http://127.0.0.1:8000/subscribers/100/

HTTP/1.1 404 Not Found
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 75
Content-Type: application/json
Date: Fri, 07 Aug 2020 02:59:55 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "email_address": [
                "Subscriber does not exist."
            ]
        }
    ],
    "user": "null"
}
```
### Error Handling on Requirement 1: User Subscriber Registration

#### Error 1-1: Attempt to register to an existing subscriber
```
C:\>http post http://127.0.0.1:8000/subscribers/ email_address="marc@company.com" password="marcpassword" first_name="Marc" last_name="Concepcion"

HTTP/1.1 409 Conflict
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 76
Content-Type: application/json
Date: Fri, 07 Aug 2020 03:05:27 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "email_address": [
                "User e-mail already exists."
            ]
        }
    ],
    "user": "null"
}
```
#### Error 1-2: Attempt to register without either the required E-mail address or Password 
```
C:\>http post http://127.0.0.1:8000/subscribers/ email_address="roy@company.com" first_name="Roy" last_name="Berry"

HTTP/1.1 400 Bad Request
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 67
Content-Type: application/json
Date: Fri, 07 Aug 2020 03:12:29 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "password": [
                "This field is required."
            ]
        }
    ],
    "user": "null"
}
```
```
C:\>http post http://127.0.0.1:8000/subscribers/ password="roypassword"

HTTP/1.1 400 Bad Request
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 72
Content-Type: application/json
Date: Fri, 07 Aug 2020 03:13:17 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "email_address": [
                "This field is required."
            ]
        }
    ],
    "user": "null"
}
```
```
C:\>http post http://127.0.0.1:8000/subscribers/

HTTP/1.1 400 Bad Request
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 111
Content-Type: application/json
Date: Fri, 07 Aug 2020 03:13:52 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "email_address": [
                "This field is required."
            ],
            "password": [
                "This field is required."
            ]
        }
    ],
    "user": "null"
}
```
#### Error 1-3: Subscriber Web Service fails to e-mail token due to SMTP issues with e-mail server.
```
C:\>http post http://127.0.0.1:8000/subscribers/ email_address="roy@company.com" first_name="Roy" last_name="Berry" password="roypassword"

HTTP/1.1 500 Internal Server Error
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 100
Content-Type: application/json
Date: Fri, 07 Aug 2020 04:05:05 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "token": [
                "Server error. Fail to e-mail token. Subscriber not created."
            ]
        }
    ],
    "user": "null"
}
```
#### Error 1-4: Internal server error due to failure to grant token by the authentication server
```
C:\>http post http://127.0.0.1:8000/subscribers/ email_address="gerry@company.com" password="gerrypassword"

HTTP/1.1 500 Internal Server Error
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 131
Content-Type: application/json
Date: Fri, 07 Aug 2020 06:46:37 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "token": [
                "Internal server error in generating token. Subscriber not created. No e-mail will be sent."
            ]
        }
    ],
    "user": "null"
}
```
### Error Handling on Requirement 2: User Activation

#### Error 2-1: Attempt to activate an already activated subscriber
```
C:\>http put http://127.0.0.1:8000/subscribers/15/ token=mAixZ120MtXUNtvIlzyjdjgblPDZGJ

HTTP/1.1 400 Bad Request
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 91
Content-Type: application/json
Date: Fri, 07 Aug 2020 03:16:05 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "activation": [
                "Subscriber has already been activated before."
            ]
        }
    ],
    "user": "null"
}
```
#### Error 2-2: Attempt to activate without a token
```
C:\>http put http://127.0.0.1:8000/subscribers/15/

HTTP/1.1 401 Unauthorized
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 85
Content-Type: application/json
Date: Fri, 07 Aug 2020 03:18:50 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "token": [
                "Subscriber is not activated. Token required."
            ]
        }
    ],
    "user": "null"
}
```
#### Error 2-3: Attempt to activate with an invalid token
```
C:\>http put http://127.0.0.1:8000/subscribers/15/ token=invalid

HTTP/1.1 401 Unauthorized
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 84
Content-Type: application/json
Date: Fri, 07 Aug 2020 03:19:38 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "token": [
                "Subscriber is not activated. Invalid token."
            ]
        }
    ],
    "user": "null"
}
```
### Error Handling on Requirement 3: User Login

#### Error 3-1: Attempt to login with neither the required e-mail address nor the password
```
C:\>http get http://127.0.0.1:8000/subscribers/15/ email_address="marc@company.com"

HTTP/1.1 400 Bad Request
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 59
Content-Type: application/json
Date: Fri, 07 Aug 2020 03:22:12 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "password": [
                "Field required."
            ]
        }
    ],
    "user": "null"
}
```
```
C:\>http get http://127.0.0.1:8000/subscribers/15/ password="password"

HTTP/1.1 400 Bad Request
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 64
Content-Type: application/json
Date: Fri, 07 Aug 2020 03:22:48 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "email_address": [
                "Field required."
            ]
        }
    ],
    "user": "null"
}
```
```
C:\>http get http://127.0.0.1:8000/subscribers/15/

HTTP/1.1 400 Bad Request
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 97
Content-Type: application/json
Date: Fri, 07 Aug 2020 03:23:15 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "email_address": [
                "Field required."
            ]
        },
        {
            "password": [
                "Field required."
            ]
        }
    ],
    "user": "null"
}
```
#### Error 3-2: Attempt to login with an invalid user name or password
```
C:\>http get http://127.0.0.1:8000/subscribers/15/ email_address="nonexistent@company.com" password="none"

HTTP/1.1 401 Unauthorized
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 82
Content-Type: application/json
Date: Fri, 07 Aug 2020 03:24:58 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "email_address": [
                "E-mail does not match the user's."
            ]
        }
    ],
    "user": "null"
}
```
```
C:\>http get http://127.0.0.1:8000/subscribers/15/ email_address="marc@company.com" password="wrong"

HTTP/1.1 401 Unauthorized
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 79
Content-Type: application/json
Date: Fri, 07 Aug 2020 03:26:03 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "password": [
                "Password does not match the user's."
            ]
        }
    ],
    "user": "null"
}
```
#### Error 3-3: Attempt to login with an unactivated subscriber account
```
C:\>http get http://127.0.0.1:8000/subscribers/17/ email_address="kevin@company.com" password="kevinpassword"

HTTP/1.1 401 Unauthorized
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 81
Content-Type: application/json
Date: Fri, 07 Aug 2020 03:27:46 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "email_address": [
                "User has not been activated yet."
            ]
        }
    ],
    "user": "null"
}
```
#### Error 3-4: Internal server error due to failure to grant token by the authentication server
```
C:\>http get http://127.0.0.1:8000/subscribers/15/ email_address="marc@company.com" password="marcpassword"

HTTP/1.1 500 Internal Server Error
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 82
Content-Type: application/json
Date: Fri, 07 Aug 2020 06:31:49 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "token": [
                "Login failure. Internal error in generating token."
            ]
        }
    ],
    "user": "null"
}
```
### Error Handling on Requirement 4: Users List

#### Error 4-1: Attempt to request for a users list giving an invalid token
```
C:\>http get http://127.0.0.1:8000/subscribers/ token=invalid

HTTP/1.1 401 Unauthorized
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 55
Content-Type: application/json
Date: Fri, 07 Aug 2020 03:30:59 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "token": [
                "Invalid token."
            ]
        }
    ],
    "user": "null"
}
```
### Error Handling on Requirement 5: Change Password

#### Error 5-1: Attempt to change password giving an invalid token
```
C:\>http patch http://127.0.0.1:8000/subscribers/15/ password="marcpassword" new_password="marcnewpassword" token=invalid

HTTP/1.1 401 Unauthorized
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 79
Content-Type: application/json
Date: Fri, 07 Aug 2020 03:33:07 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "token": [
                "Unauthorized operation. Invalid token."
            ]
        }
    ],
    "user": "null"
}
```
#### Error 5-2: Attempt to change password giving an invalid current password
```
C:\>http patch http://127.0.0.1:8000/subscribers/15/ password="wrongpassword" new_password="marcnewpassword" token=mAixZ120MtXUNtvIlzyjdjgblPDZGJ

HTTP/1.1 401 Unauthorized
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 66
Content-Type: application/json
Date: Fri, 07 Aug 2020 03:34:17 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "password": [
                "Invalid user password."
            ]
        }
    ],
    "user": "null"
}
```
#### Error 5-3: Attempt to change password giving insufficient parameters
```
C:\>http patch http://127.0.0.1:8000/subscribers/15/ password="marcpassword" new_password="marcnewpassword"

HTTP/1.1 400 Bad Request
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 56
Content-Type: application/json
Date: Fri, 07 Aug 2020 03:36:59 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "token": [
                "Field required."
            ]
        }
    ],
    "user": "null"
}
```
```
C:\>http patch http://127.0.0.1:8000/subscribers/15/ new_password="marcnewpassword" token=mAixZ120MtXUNtvIlzyjdjgblPDZGJ

HTTP/1.1 400 Bad Request
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 59
Content-Type: application/json
Date: Fri, 07 Aug 2020 03:37:25 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "password": [
                "Field required."
            ]
        }
    ],
    "user": "null"
}
```
```
C:\>http patch http://127.0.0.1:8000/subscribers/15/ password="wrongpassword" token=mAixZ120MtXUNtvIlzyjdjgblPDZGJ

HTTP/1.1 400 Bad Request
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 63
Content-Type: application/json
Date: Fri, 07 Aug 2020 03:38:16 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "new_password": [
                "Field required."
            ]
        }
    ],
    "user": "null"
}
```
```
C:\>http patch http://127.0.0.1:8000/subscribers/15/ password="wrongpassword"

HTTP/1.1 400 Bad Request
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 93
Content-Type: application/json
Date: Fri, 07 Aug 2020 03:38:55 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "new_password": [
                "Field required."
            ]
        },
        {
            "token": [
                "Field required."
            ]
        }
    ],
    "user": "null"
}
```
```
C:\>http patch http://127.0.0.1:8000/subscribers/15/ new_password="marcnewpassword"

HTTP/1.1 400 Bad Request
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 89
Content-Type: application/json
Date: Fri, 07 Aug 2020 03:39:46 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "password": [
                "Field required."
            ]
        },
        {
            "token": [
                "Field required."
            ]
        }
    ],
    "user": "null"
}
```
```
C:\>http patch http://127.0.0.1:8000/subscribers/15/

HTTP/1.1 400 Bad Request
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 126
Content-Type: application/json
Date: Fri, 07 Aug 2020 03:40:04 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.8.5
Vary: Accept, Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "errors": [
        {
            "password": [
                "Field required."
            ]
        },
        {
            "new_password": [
                "Field required."
            ]
        },
        {
            "token": [
                "Field required."
            ]
        }
    ],
    "user": "null"
}
```

For more inquiries, please feel free to e-mail me at marcanthonyconcepcion@gmail.com.
Thank you.

# END
