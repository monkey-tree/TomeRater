'''
class TypeWrongException(Exception):
    def __repr__(self):
        return 'The type of the parameter is wrong, please check!'

'''
Book_Instances = []
class User(object):
    '''

    '''
    def __init__(self, name, email):
        if not isinstance(name, str) or not isinstance(email, str):
            raise TypeError('Bad type for name')
        else:
            self.name = name
            self.email = email
            self.books = {}



    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address

    def __repr__(self):
        repr_books = ''
        for book in self.books:
            repr_books = repr_books + str(book) + ', user rating is ' + str(self.books[book])
        return ('[User ' + self.name + ', email: ' +
                self.email + ', ' + 'books read: ' +
                str(len(self.books)) + ', books: ' +
                repr_books  + ']')


    def __eq__(self, other_user):
        if other_user is None:
            return False
        elif self.name == other_user.name and self.email == other_user.email:
            return True
        else:
            return False

    def read_book(self, book, rating = None):
        if not isinstance(book, Book):
            raise TypeError('bad type for book')
        else:
            self.books[book] = rating

    def get_avg_ratings(self):
        if not len(self.books):
            return 0
        else:
            total_rating = 0
            for rating in self.books.values():
                if rating is None:
                    pass
                else:
                    total_rating = total_rating + rating
            return total_rating/len(self.books)


class Book:
    def __init__(self, title, isbn):
        if type(title) != str and type(isbn) != int:
            raise TypeError('bad type for title or isbn.')
        else:
            if len(Book_Instances) != 0:
                for book in Book_Instances:
                    if book.isbn == isbn:
                        raise Exception('Duplicated ISBN.')

            self.title = title
            self.isbn = isbn
            self.ratings = []

        Book_Instances.append(self)

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, isbn):
        if type(isbn) == int:
            self.isbn = isbn
        else:
            raise TypeError('bad type for isbn')

    def add_rating(self, rating):
        if type(rating) != int:
            raise TypeError('bad type for rating')
        else:
            if rating < 0 or rating > 4:
                print('Invalid Rating')
            else:
                self.ratings.append(rating)

    def __repr__(self):
        repr_ratings = ''
        for rating in self.ratings:
            repr_ratings = repr_ratings + ':{}'.format(rating)
        return ('\'Book title is: ' + self.title + ' and ISBN is: ' +
                str(self.isbn) + ' and there are ' + str(len(self.ratings)) +
                ' ratings and ratings are: ' + repr_ratings + '\'')

    def __eq__(self, other_book):
        if other_book is None:
            return False
        elif self.title == other_book.title and self.isbn == other_book.isbn:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.title, self.isbn))

    def get_avg_rating(self):
        if not len(self.ratings):
            return 0
        else:
            total_rating = 0
            for rating in self.ratings:
                total_rating = total_rating + rating
            return total_rating/len(self.ratings)


class Fiction(Book):
    def __init__(self, title, author, isbn):
        if type(title) != str or type(author) != str or type(isbn) != int:
            raise TypeError('bad type for title or author or isbn')
        else:
            super().__init__(title, isbn)
            self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        book_repr=super().__repr__()
        return '{} and author is: {}\''.format(book_repr[0:-1], self.author)



class NonFiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        book_repr = super().__repr__()
        return '{} and subject is: {} and level is: {}\''.format(book_repr[0:-1], self.subject, self.level)



class TomeRater:
    def __init__(self):
        self.users = {}
        self.books = {}

    def __repr__(self):
        repr_users = ''
        repr_books = ''
        for key, value in self.users.items():
            repr_users = repr_users + '{}: {} \n'.format(str(key), str(value))

        for key, value in self.books.items():
            repr_books = repr_books + '{}: {} \n'.format(str(key), str(value))

        return ("users: \n{}\nbooks:\n{}".format(repr_users, repr_books))

    def create_book(self, title, isbn):
        try:
            new_book = Book(title, isbn)
            return new_book
        except Exception:
            raise

    def __eq__(self, other_tome_rater):
        if other_tome_rater is None:
            return False
        else:
            for key, value in self.users.items():
                for other_key, other_value in other_tome_rater.users.items():
                    if key != other_key or value != other_value:
                        return False
            for key, value in self.books.items():
                for other_key, other_value in other_tome_rater.books.items():
                    if key != other_key or value != other_value:
                        return False

            return True



    def create_novel(self, title, author, isbn):
        try:
            new_novel = Fiction(title, author, isbn)
            return new_novel
        except Exception:
            raise

    def create_non_fiction(self, title, subject, level, isbn):
        try:
            new_non_fiction = NonFiction(title, subject, level, isbn)
            return new_non_fiction
        except Exception:
            raise

    def email_validate(self, email):
        if '@' in email and ('.com' in email or '.edu' in email or '.org' in email):
            return True
        else:
            return False

    def add_user(self, name, email, user_books = None):
        if not self.email_validate(email):
            print('It\'s not a valid email address.')
            return
        elif email in self.users.keys():
            print('The user already exists.')
            return
        else:
            try:
                new_user = User(name, email)
                self.users[email] = new_user
            except Exception:
                raise

        if user_books != None:
            for book in user_books:
                self.add_book_to_user(book, email)

    def dup_isbn(self, book):
        if self.books == {}:
            return False
        else:
            for user_book in self.books:
                if book.isbn == user_book.isbn:
                    return user_book
            return False


    def add_book_to_user(self, book, email, rating = None):
        if not self.email_validate(email) or not email in self.users:
            print('Not valid email address, or no user with this email.')
            return
        elif not isinstance(book, Book):
            print('Bad type for book.')
            return
        else:
            try:
                user = self.users.get(email)
                user.read_book(book, rating)
                if rating is None:
                    pass
                else:
                    book.add_rating(rating)
                if book in self.books.keys():
                    self.books[book] = self.books[book] + 1
                else:
                    self.books[book] = 1
            except Exception:
                raise

    def print_catalog(self):
        if self.books == {}:
            print('No books read.')
        else:
            for book in self.books:
                print(book)

    def print_users(self):
        if self.users == {}:
            print('No users')
        else:
            for user in self.users:
                print(self.users[user])

    def get_most_read_book(self):
        most_read_book = None
        most_read_num = 0
        if self.books == {}:
            return None
        else:
            for book in self.books:
                if self.books[book] > most_read_num:
                    most_read_num = self.books[book]
                    most_read_book = book
                else:
                    pass
        return most_read_book

    def sort_books_descend(self, books):
        if self.books == {}:
            return None
        else:
            read_book_descend = []
            most_read_book = None
            most_read_num = 0
            for book in self.books:
                if self.books[book] <= most_read_num:
                    read_book_descend.append(book)
                else:
                    most_read_num = self.books[book]
                    most_read_book = book

                    if len(read_book_descend) == 0:
                        read_book_descend.append(None)
                        read_book_descend[0] = book
                    else:
                        i = 0
                        read_book_descend.append(None)
                        while i <= len(read_book_descend) - 2:
                            if 0-i-2 == 0:
                                j = 0
                            else:
                                j = 0-i-2
                            if self.books[read_book_descend[j]] < most_read_num:
                                read_book_descend[0-i-1] = read_book_descend[j]
                                read_book_descend[j] = most_read_book
                            i = i + 1
            return read_book_descend

    def get_n_most_read_book(self, n):
        read_book_descend = self.sort_books_descend(self.books)
        read_book_descend_new = []
        for i in range(min(n, len(read_book_descend))):
            read_book_descend_new.append((read_book_descend[i], self.books[read_book_descend[i]]))
        return read_book_descend_new

    def highest_rated_book(self):
        highest_rated_book = None
        highest_rating = 0
        if self.books == {}:
            return None
        else:
            for book in self.books:
                avg_rating = book.get_avg_rating()
                if  highest_rating <= avg_rating:
                    highest_rating = avg_rating
                    highest_rated_book = book
                else:
                    pass
        return highest_rated_book

    def most_positive_user(self):
        highest_rating = 0
        most_positive_user = None
        if self.users == {}:
            return None
        else:
            for user in self.users.values():
                avg_rating = user.get_avg_ratings()
                if highest_rating <= avg_rating:
                    highest_rating = avg_rating
                    most_positive_user = user
        return most_positive_user
