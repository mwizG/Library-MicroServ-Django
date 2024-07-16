from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import requests
from . models import Loan
from . forms import LoanForm
from . serializers import LoanSerializer
@csrf_exempt
def borrow_book(request):
    if request.method == 'POST':
        print("borrow_book view called")
        user_id = request.POST.get('user_id')
        book_id = request.POST.get('book_id')
        book_title = request.POST.get('book_title')  # Get book title from the request

        print(f"Received POST request with user_id: {user_id}, book_id: {book_id}, book_title: {book_title}")
        
        if not user_id or not book_id or not book_title:
            print("User ID, Book ID, or Book Title missing")
            return JsonResponse({'error_message': 'User ID, Book ID, and Book Title are required.'}, status=400)
        
        form = LoanForm()
        print("Displaying the form for return date")
        return JsonResponse({'form': form.as_p()}, status=200)
    
    print("Request method is not POST")
    return JsonResponse({'error_message': 'Invalid request method.'}, status=400)

@csrf_exempt
def create_loan(request):
    if request.method == 'POST':
        print('we are running create loan')
        user_id = request.POST.get('user_id')
        book_id = request.POST.get('book_id')
        book_title = request.POST.get('book_title')  # Get book title from the request
        return_date = request.POST.get('return_date')
        print("date:", return_date)
        if not user_id or not book_id or not book_title:
            return JsonResponse({'error_message': 'Session expired. Please try borrowing the book again.'}, status=400)

        form = LoanForm(request.POST)
        if 'return_date' in request.POST:
            if form.is_valid():
                new_loan = form.save(commit=False)
                new_loan.user_id = user_id
                new_loan.book_id = book_id
                new_loan.book_title = book_title  # Set book title in the Loan instance
                new_loan.return_date = return_date
                new_loan.save()

                return JsonResponse({"message": "Book BORROWED successfully"}, status=201)
            else:
                return JsonResponse({'form': form.as_p(), 'error_message': 'Please provide a valid return date'}, status=400)
        else:
            return JsonResponse({'form': form.as_p(), 'error_message': 'Please provide a return date'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

class MyBooksView(APIView):
    permission_classes = []
    @csrf_exempt
    def get(self, request, user_id):
        print('listing my books has started')
        # Filter loans by user_id
        loans = Loan.objects.filter(user_id=user_id)
        # Serialize the loan data
        loan_serializer = LoanSerializer(loans, many=True)
        # Return the serialized data as a response
        return Response(loan_serializer.data)


class ReturnBookView(APIView):
    @csrf_exempt
    def post(self, request):
        user_id = request.data.get('user_id')
        book_id = request.data.get('book_id')

        # Make API requests to fetch user and book information
        user_info_response = requests.get(f'http://user_microservice/users/{user_id}/')
        book_info_response = requests.get(f'http://book_microservice/books/{book_id}/')

        if user_info_response.status_code == 200 and book_info_response.status_code == 200:
            # Perform logic for returning the book (e.g., updating database)
            # Assuming you have a Loan model and need to update the 'returned' field
            loan = Loan.objects.get(user_id=user_id, book_id=book_id)
            loan.returned = True
            loan.save()

            user_info = user_info_response.json()
            book_info = book_info_response.json()

            return Response({'user_info': user_info, 'book_info': book_info}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Failed to fetch user or book information'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response(status=status.HTTP_200_OK)
    

