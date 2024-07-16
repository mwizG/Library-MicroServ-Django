from django.db import models

class Loan(models.Model):
    user_id = models.IntegerField()
    book_id = models.IntegerField()
    book_title = models.CharField(max_length=255,null=True,blank=True)  # New field to store the book title
    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"Loan - User: {self.user_id}, Book: {self.book_id}, Title: {self.book_title}"
