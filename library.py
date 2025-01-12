from datetime import datetime, timedelta

# Book class to represent each book in the library
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_borrowed = False
        self.borrower = None

    def __str__(self):
        return f"{self.title} by {self.author}"

# Borrower class to represent each borrower
class Borrower:
    def __init__(self, name, membership):
        self.name = name
        self.membership = membership
        self.borrowed_books = []

    def __str__(self):
        return f"{self.name} ({self.membership} Membership)"

# Library class to manage books and borrowers
class Library:
    def __init__(self):
        self.books = []
        self.borrowers = []

    def add_book(self, book):
        self.books.append(book)
        print(f"Book added: {book}")

    def remove_book(self, title):
        for book in self.books:
            if book.title == title and not book.is_borrowed:
                self.books.remove(book)
                print(f"Book removed: {book}")
                return
        print("Book not found or currently borrowed.")

    def add_borrower(self, borrower):
        self.borrowers.append(borrower)
        print(f"Borrower added: {borrower}")

    def issue_book(self, title, borrower_name):
        for book in self.books:
            if book.title == title and not book.is_borrowed:
                for borrower in self.borrowers:
                    if borrower.name == borrower_name:
                        book.is_borrowed = True
                        book.borrower = borrower
                        borrower.borrowed_books.append((book, datetime.now()))
                        print(f"Book issued: {book} to {borrower}")
                        return
        print("Book not available or borrower not found.")

    def return_book(self, title, borrower_name):
        for borrower in self.borrowers:
            if borrower.name == borrower_name:
                for book, issue_date in borrower.borrowed_books:
                    if book.title == title:
                        borrower.borrowed_books.remove((book, issue_date))
                        book.is_borrowed = False
                        book.borrower = None
                        print(f"Book returned: {book} by {borrower}")

                        # Calculate late fee
                        days_borrowed = (datetime.now() - issue_date).days
                        allowed_days = self.get_allowed_days(borrower.membership)
                        if days_borrowed > allowed_days:
                            late_fee = (days_borrowed - allowed_days) * 10
                            print(f"Late fee: Rs. {late_fee}")
                        else:
                            print("No late fee.")
                        return
        print("Book not found for the borrower.")

    def get_allowed_days(self, membership):
        if membership == "Student":
            return 7
        elif membership == "Regular":
            return 14
        elif membership == "Premium":
            return 30
        return 0

    def display_books(self):
        print("Books in the library:")
        for book in self.books:
            status = "Available" if not book.is_borrowed else f"Borrowed by {book.borrower.name}"
            print(f"- {book} ({status})")

    def display_borrowers(self):
        print("Borrowers:")
        for borrower in self.borrowers:
            print(f"- {borrower} (Borrowed books: {[book.title for book, _ in borrower.borrowed_books]})")

# Example usage (you can use this in your video as a demo)
if __name__ == "__main__":
    library = Library()

    # Adding books
    library.add_book(Book("1984", "George Orwell"))
    library.add_book(Book("To Kill a Mockingbird", "Harper Lee"))

    # Adding borrowers
    library.add_borrower(Borrower("Alice", "Student"))
    library.add_borrower(Borrower("Bob", "Premium"))

    # Display books and borrowers
    library.display_books()
    library.display_borrowers()

    # Issuing and returning books
    library.issue_book("1984", "Alice")
    library.display_books()

    library.return_book("1984", "Alice")
    library.display_books()
