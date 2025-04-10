# Library Management API

## Authentication

- **POST** `api/v1/auth/login/`  
  Login to the system.

- **POST** `api/v1/auth/logout/`  
  Logout from the system.

- **GET** `api/v1/auth/profile/`  
  View the profile details of the logged-in user.

- **PATCH** `api/v1/auth/profile/`  
  Partially update the profile of the logged-in user.

- **POST** `api/v1/auth/register-library/`  
  Register a new library.

## Books

- **GET** `api/v1/books/book/{id}/`  
  Retrieve details of a single book.

- **PUT** `api/v1/books/book/{id}/`  
  Update the details of a specific book (for admin and library staff only).

- **DELETE** `api/v1/books/book/{id}/`  
  Delete a specific book (for admin and library staff only).

- **GET** `api/v1/books/books/`  
  Retrieve a list of all books.

- **POST** `api/v1/books/books/`  
  Add a new book (for admin and library staff only).

- **GET** `api/v1/books/search/book/`  
  Search for books based on query parameters.

- **POST** `api/v1/books/upload-excel/`  
  Upload an Excel file and return the list of books from the file (for admin and library staff only).

- **POST** `api/v1/books/add-books/`  
  Add books from the list extracted from an Excel file (for admin and library staff only).

## Libraries

- **GET** `api/v1/libraries/libraries/`  
  Retrieve a list of all libraries.

- **PATCH** `api/v1/libraries/library/activate/{id}/`  
  Activate a library (for admin only).

- **DELETE** `api/v1/libraries/library/deactivate/{id}/`  
  Deactivate a library (for admin only).

- **GET** `api/v1/libraries/library/{id}/`  
  Retrieve details of a specific library.
