"""
Library Management System (Python OOP)
========================================
"""
# 1. Person (Parent Class)
class Person:

    # Class variable - tracks total number of Person objects created
    total_people = 0

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        Person.total_people += 1

    def display_info(self):
        print(f"Name : {self.name}")
        print(f"Age  : {self.age}")

    @classmethod
    def get_total_people(cls):
        return cls.total_people

    @staticmethod
    def is_valid_age(age) -> bool:
        """Static method to validate age without needing an instance."""
        try:
            return int(age) > 0
        except (ValueError, TypeError):
            return False

# 2. Member (Child of Person) -> Inheritance
class Member(Person):

    # Class variable - tracks total members registered
    total_members = 0

    def __init__(self, member_id: str, name: str, age: int):
        super().__init__(name, age)          # Reuse parent constructor
        self.member_id = member_id
        self.borrowed_books = []             # list of Book objects
        Member.total_members += 1

    def borrow_book(self, book: "Book"):
        """Add a book to this member's borrowed list."""
        self.borrowed_books.append(book)

    def return_book(self, book: "Book"):
        """Remove a book from this member's borrowed list."""
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)

    def has_borrowed(self, book: "Book") -> bool:
        return book in self.borrowed_books

    def display_info(self):  # Method Overriding
        print(f"Member ID : {self.member_id}")
        print(f"Name      : {self.name}")
        print(f"Age       : {self.age}")
        print(f"Borrowed Books : {len(self.borrowed_books)}")

# 3. Book
class Book:

    total_books = 0

    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn
        self._available = True          # private attribute (encapsulation)
        Book.total_books += 1

    # ---- Getter ----
    @property
    def available(self) -> bool:
        return self._available

    # ---- Setter ----
    @available.setter
    def available(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("available must be a boolean value.")
        self._available = value

    # ---- Read-only property ----
    @property
    def status(self) -> str:
        return "Available" if self._available else "Borrowed"

    def display_book(self):
        print(f"ISBN   : {self.isbn}")
        print(f"Title  : {self.title}")
        print(f"Author : {self.author}")
        print(f"Status : {self.status}")


# 4. Library -> Composition (Library "has" Books and Members)
class Library:

    def __init__(self):
        self.books = {}      # isbn -> Book
        self.members = {}    # member_id -> Member

    # ---------------- Book Operations ----------------
    def add_book(self, title: str, author: str, isbn: str):
        title = title.strip()
        author = author.strip()
        isbn = isbn.strip()

        if not title:
            raise ValueError("Book title cannot be empty.")
        if not author:
            raise ValueError("Author name cannot be empty.")
        if not isbn:
            raise ValueError("ISBN cannot be empty.")
        if isbn in self.books:
            raise ValueError("ISBN already exists.")

        self.books[isbn] = Book(title, author, isbn)
        print("Book added successfully!")

    def show_books(self):
        if not self.books:
            print("No books available in the library.")
            return
        print("------------- BOOK LIST -------------")
        for book in self.books.values():
            book.display_book()
            print("-------------------------------------")

    def search_book(self, title: str):
        title = title.strip().lower()
        for book in self.books.values():
            if book.title.strip().lower() == title:
                print("Book Found!")
                book.display_book()
                return book
        print("Book not found.")
        return None

    # ---------------- Member Operations ----------------
    def register_member(self, member_id: str, name: str, age):
        member_id = member_id.strip()
        name = name.strip()

        if not member_id:
            raise ValueError("Member ID cannot be empty.")
        if not name:
            raise ValueError("Name cannot be empty.")
        if member_id in self.members:
            raise ValueError("Member ID already exists.")
        if not Person.is_valid_age(age):
            raise ValueError("Age must be greater than 0.")

        self.members[member_id] = Member(member_id, name, int(age))
        print("Member registered successfully!")

    def show_members(self):
        if not self.members:
            print("No members registered.")
            return
        print("----------- MEMBER LIST ------------")
        for member in self.members.values():
            member.display_info()
            print("------------------------------------")

    # ---------------- Borrow / Return ----------------
    def borrow_book(self, member_id: str, isbn: str):
        member_id = member_id.strip()
        isbn = isbn.strip()

        member = self.members.get(member_id)
        if member is None:
            raise LookupError("Member not found.")

        book = self.books.get(isbn)
        if book is None:
            raise LookupError("Book not found.")

        if member.has_borrowed(book):
            raise ValueError("This member has already borrowed this book.")

        if not book.available:
            print("Sorry! This book is currently unavailable.")
            return

        book.available = False
        member.borrow_book(book)
        print("Book borrowed successfully.")

    def return_book(self, member_id: str, isbn: str):
        member_id = member_id.strip()
        isbn = isbn.strip()

        member = self.members.get(member_id)
        if member is None:
            raise LookupError("Member not found.")

        book = self.books.get(isbn)
        if book is None:
            raise LookupError("Book not found.")

        if not member.has_borrowed(book):
            raise ValueError("This member has not borrowed this book.")

        book.available = True
        member.return_book(book)
        print("Book returned successfully.")

# Helper input functions
def get_non_empty_input(prompt: str) -> str:
    value = input(prompt).strip()
    if not value:
        raise ValueError("Input cannot be empty.")
    return value


def get_valid_age(prompt: str) -> int:
    value = input(prompt).strip()
    if not value:
        raise ValueError("Input cannot be empty.")
    age = int(value)  # may raise ValueError if not a number
    if age <= 0:
        raise ValueError("Age must be greater than 0.")
    return age


# Console Menu / Main Program
def print_menu():
    print("=========================================")
    print("LIBRARY MANAGEMENT SYSTEM")
    print("=========================================")
    print("1. Add Book")
    print("2. Register Member")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Show All Books")
    print("6. Show All Members")
    print("7. Search Book")
    print("8. Exit")


def main():
    library = Library()

    while True:
        print_menu()
        try:
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                print("----- Add New Book -----")
                try:
                    title = get_non_empty_input("Enter Book Title : ")
                    author = get_non_empty_input("Enter Author : ")
                    isbn = get_non_empty_input("Enter ISBN : ")
                    library.add_book(title, author, isbn)
                except ValueError as e:
                    print(f"Error: {e}")

            elif choice == "2":
                print("----- Register Member -----")
                try:
                    member_id = get_non_empty_input("Enter Member ID : ")
                    name = get_non_empty_input("Enter Name : ")
                    age = get_valid_age("Enter Age : ")
                    library.register_member(member_id, name, age)
                except ValueError as e:
                    print(f"Error: {e}")

            elif choice == "3":
                print("------ Borrow Book ------")
                try:
                    member_id = get_non_empty_input("Enter Member ID : ")
                    isbn = get_non_empty_input("Enter Book ISBN : ")
                    library.borrow_book(member_id, isbn)
                except (ValueError, LookupError) as e:
                    print(f"{e}")

            elif choice == "4":
                print("------ Return Book ------")
                try:
                    member_id = get_non_empty_input("Enter Member ID : ")
                    isbn = get_non_empty_input("Enter Book ISBN : ")
                    library.return_book(member_id, isbn)
                except (ValueError, LookupError) as e:
                    print(f"{e}")

            elif choice == "5":
                library.show_books()

            elif choice == "6":
                library.show_members()

            elif choice == "7":
                print("------ Search Book ------")
                try:
                    title = get_non_empty_input("Enter Book Title : ")
                    library.search_book(title)
                except ValueError as e:
                    print(f"Error: {e}")

            elif choice == "8":
                print("Thank you for using Library Management System.")
                print("Goodbye!")
                break

            else:
                print("Invalid choice! Please enter a number between 1 and 8.")

        except ValueError:
            # Catches invalid age input (non-numeric) and empty input
            print("Error: Invalid input. Please try again.")
        except Exception as e:
            # Catches any unexpected runtime error so the program never crashes
            print(f"Unexpected error: {e}")

        input("Press Enter to continue...")


if __name__ == "__main__":
    main()
