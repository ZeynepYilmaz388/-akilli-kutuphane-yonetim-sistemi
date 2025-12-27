# app/models/__init__.py
# Tüm modelleri buradan import et(dahil etmek )

from app.models.user import User
from app.models.book import Book
from app.models.loan import Loan
from app.models.author import Author
from app.models.category import Category

__all__ = ['User', 'Book', 'Loan', 'Author', 'Category']