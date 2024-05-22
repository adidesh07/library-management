from django.db import models
from usermanagement.models import Account


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(verbose_name="date joined", auto_now_add=True, blank=True, null=True)
    borrowed_by = models.ForeignKey(
        Account, related_name="borrowed_by", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self) -> str:
        return self.title

    @property
    def is_available(self):
        if self.borrowed_by:
            return False
        return True


class Borrow(models.Model):
    borrowed_by = models.ForeignKey(
        Account, related_name="borrowed_user", on_delete=models.SET_NULL, null=True, blank=True
    )
    book = models.ForeignKey(Book, related_name="borrowed_book", on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    due_date = models.DateTimeField(verbose_name="due date", blank=True, null=True)
