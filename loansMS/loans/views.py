from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import requests
from . models import Loan
from . forms import LoanForm

@csrf_exempt
def borrow_book(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        book_id = request.POST.get('book_id')
        
        if not user_id or not book_id:
            # Redirect to an error page or render an error message
            return render(request, 'error.html', {'error_message': 'User ID and Book ID are required.'})

        # Save user_id and book_id in the session
        request.session['user_id'] = user_id
        request.session['book_id'] = book_id
        
        # Display the form to input return date
        form = LoanForm()
        return render(request, 'borrow.html', {'form': form})
    
    return redirect('mybooks')  # Redirect to mybooks if the request is not POST
@csrf_exempt
def create_loan(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        book_id = request.session.get('book_id')
        return_date=request.POST.get('return_date')
        
        if not user_id or not book_id:
            # Redirect to an error page or render an error message
            return render(request, 'error.html', {'error_message': 'Session expired. Please try borrowing the book again.'})

        form = LoanForm(request.POST)
        if 'return_date' in request.POST:
            if form.is_valid():
                new_loan = form.save(commit=False)
                new_loan.user_id = user_id
                new_loan.book_id = book_id
                new_loan.return_date=return_date
                new_loan.save()
                
                book_details_url = 'http://127.0.0.1:8000/details/{}'.format(book_id)
                
                # Redirect to another page after successfully saving the loan
                return redirect(book_details_url)# Change 'success_page' to the actual URL name or path you want to redirect to
            else:
                return render(request, 'create.html', {'form': form, 'error_message': 'Please provide a valid return date'})
        else:
            return render(request, 'return.html', {'form': form, 'error_message': 'Please provide a return date'})
    
    return redirect('mybooks')  # Redirect to mybooks if the request is not POST




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