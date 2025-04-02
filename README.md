# Library Management API

## Authentication

- **POST** `/auth/login/`  
  Login to the system.

- **POST** `/auth/logout/`  
  Logout from the system.

- **GET** `/auth/profile/`  
  View the profile details of the logged-in user.

- **PATCH** `/auth/profile/`  
  Partially update the profile of the logged-in user.

- **POST** `/auth/register-library/`  
  Register a new library.

## Books

- **GET** `/books/book/{id}/`  
  Retrieve details of a single book.

- **PUT** `/books/book/{id}/`  
  Update the details of a specific book (for admin and library staff only).

- **DELETE** `/books/book/{id}/`  
  Delete a specific book (for admin and library staff only).

- **GET** `/books/books/`  
  Retrieve a list of all books.

- **POST** `/books/books/`  
  Add a new book (for admin and library staff only).

- **GET** `/books/search/book/`  
  Search for books based on query parameters.

- **POST** `/books/upload-excel/`  
  Upload an Excel file and return the list of books from the file (for admin and library staff only).

- **POST** `/books/add-books/`  
  Add books from the list extracted from an Excel file (for admin and library staff only).

## Libraries

- **GET** `/libraries/libraries/`  
  Retrieve a list of all libraries.

- **PATCH** `/libraries/library/activate/{id}/`  
  Activate a library (for admin only).

- **GET** `/libraries/library/{id}/`  
  Retrieve details of a specific library.

- **DELETE** `/libraries/library/{id}/`  
  Delete a specific library (for admin only).
