from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Transaction, Income, Expense, Saving, Transfer, Category

from Account.models import Account
from GoalSetter.models import Goal
from datetime import datetime

import json

def transaction_list(request):
    # Displays all transactions
    transactions = Transaction.objects.all().order_by('-timestamp')
    context = {
        'transactions': transactions
    }
    return render(request, 'transactionList.html', context)

def _process_transaction_data(data, ModelClass, instance=None):

    # Handle Common Fields
    try:
        # Must pass a valid accountId and timestamp (date) from the frontend
        # Assuming accountId comes from the form data (or user session)
        account_id = data.get('accountId') or 1  # Default to 1 if missing
        instance.accountId = Account.objects.get(pk=account_id)

        instance.amount = data.get('amount')
        date_str = data.get('date')
        try:
            # parsing MM/DD/YYYY (Flatpickr)
            instance.timestamp = datetime.strptime(date_str, '%m/%d/%Y')
        except ValueError:
            # Fallback to YYYY-MM-DD (standard)
            instance.timestamp = datetime.strptime(date_str, '%Y-%m-%d')

        instance.notes = data.get('notes', '')
        instance.type = data.get('type')

    except (Account.DoesNotExist, ValueError, TypeError) as e:
        # Handle missing FK or bad date format
        raise ValueError(f"Invalid common field data: {e}")

    # Handle Subclass Fields (Foreign Keys)
    t_type = instance.type

    if t_type == 'I':
        instance.source = data.get('source', '')

    elif t_type == 'E':
        category_id = data.get('category') or 1  # Default to 1 if missing
        instance.categoryId = Category.objects.get(pk=category_id)
        instance.name = data.get('notes', 'Expense')  # Using notes as a default name

    elif t_type == 'S':
        goal_id = data.get('goal') or 1  # Default to 1 if missing
        instance.goalId = Goal.objects.get(pk=goal_id)

    elif t_type == 'T':
        # Assuming receiver is an account ID
        receiver_id = data.get('receiver') or 2  # Default to 2 if missing
        instance.receiverId = Account.objects.get(pk=receiver_id)

    return instance

@csrf_exempt
@require_http_methods(["POST"])
def save_transaction(request):
    """Handles Create and Edit (Update) functions."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    transaction_id = data.get('transaction_id')
    transaction_type = data.get('type')

    # Determine the model class based on type
    ModelClass = Transaction
    if transaction_type == 'I':
        ModelClass = Income
    elif transaction_type == 'E':
        ModelClass = Expense
    elif transaction_type == 'S':
        ModelClass = Saving
    elif transaction_type == 'T':
        ModelClass = Transfer
    else:
        return JsonResponse({'error': 'Invalid transaction type.'}, status=400)

    try:
        # Handle Edit
        if transaction_id:
            # Use get_subclass_instance to fetch the correct subtype for editing
            parent_instance = get_object_or_404(Transaction, pk=transaction_id)
            instance = parent_instance.get_subclass_instance()

           # this assumes the transaction type does NOT change during an edit.

        # Handle Create
        else:
            instance = ModelClass()

        # Process and validate all fields, including FKs
        instance = _process_transaction_data(data, ModelClass, instance)

        instance.save()  # Saves to the database

        # Return the saved data needed for UI update (frontend fix)
        response_data = {
            'success': True,
            'transaction_id': instance.pk,
            'type': instance.type,
            'amount': str(instance.amount),
            'date': instance.timestamp.strftime('%Y-%m-%d'),
            'notes': instance.notes,
            # Include specific fields for UI refresh
            'source': getattr(instance, 'source', None),
            'category': getattr(instance, 'categoryId_id', None),
            'goal': getattr(instance, 'goalId_id', None),
            'receiver': getattr(instance, 'receiverId_id', None),
        }
        return JsonResponse(response_data)

    except (ValueError, Goal.DoesNotExist, Category.DoesNotExist, Account.DoesNotExist) as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'A server error occurred: {e}'}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])  # Changed to require DELETE method
def delete_transaction(request, pk):
    """Deletes a transaction from the database."""
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.delete()
    return JsonResponse({'success': True, 'message': 'Transaction deleted successfully!'})


def get_transaction_details(request, pk):
    """Fetches existing transaction details to populate form."""
    transaction = get_object_or_404(Transaction, pk=pk)

    # Use get_subclass_instance to fetch the specific fields
    subclass_instance = transaction.get_subclass_instance()

    data = {
        'transaction_id': transaction.transactionId,
        'amount': str(transaction.amount),
        'accountId': transaction.accountId.pk,  # Primary Account FK
        'date': transaction.timestamp.strftime('%m/%d/%Y'),  # Use Flatpickr format
        'notes': transaction.notes,
        'type': transaction.type,
    }

    # Add fields specific to the transaction type
    if transaction.type == 'I':
        data['source'] = subclass_instance.source
    elif transaction.type == 'E':
        data['category'] = subclass_instance.categoryId.pk
    elif transaction.type == 'S':
        data['goal'] = subclass_instance.goalId.pk
    elif transaction.type == 'T':
        data['receiver'] = subclass_instance.receiverId.pk  # Receiving Account FK

    return JsonResponse(data)


# from django.shortcuts import render, redirect, get_object_or_404
# from django.views.decorators.http import require_http_methods
# from django.http import JsonResponse
# from .models import Transaction, Income, Expense, Saving, Transfer, Category
# # from Account.models import Account
# # from GoalSetter.models import Goal
#
# import json
#
# def transaction_list(request):
#     # Displays all transactions
#     transactions = Transaction.objects.all().order_by('-timestamp')
#     context = {
#         'transactions': transactions
#     }
#     return render(request, 'transactionList.html', context)
#
# # AJAX Views
# @require_http_methods(["POST"])
# def save_transaction(request):
#     # Handles Create and Edit functions
#     # Assuming the form data is sent as JSON via AJAX
#     try:
#         data = json.loads(request.body)
#     except json.JSONDecodeError:
#         return JsonResponse({'error': 'Invalid JSON format'}, status=400)
#
#     transaction_id = data.get('transaction_id')
#     transaction_type = data.get('type')  # 'I', 'E', 'S', or 'T'
#
#     # Determine the model class based on type
#     if transaction_type == 'I':
#         ModelClass = Income
#     elif transaction_type == 'E':
#         ModelClass = Expense
#     elif transaction_type == 'S':
#         ModelClass = Saving
#     else:
#         ModelClass = Transfer
#
#     # Handle Edit and Create
#     if transaction_id:
#         # Edit existing transaction
#         instance = get_object_or_404(ModelClass, pk=transaction_id)
#     else:
#         # Create new transaction
#         instance = ModelClass()
#
#     # Update common fields (handled by parent Transaction)
#     # instance.accountId = ... (get from data)
#     instance.amount = data.get('amount')
#     instance.timestamp = data.get('date')
#     instance.notes = data.get('notes')
#     instance.type = transaction_type
#
#     # Update specific fields (handled by subtype model)
#     if transaction_type == 'I':
#         instance.source = data.get('source')
#     elif transaction_type == 'E':
#         instance.source = data.get('category')
#     elif transaction_type == 'S':
#         instance.source = data.get('goal')
#     else:
#         instance.source = data.get('receiver')
#
#     instance.save()
#
#     return JsonResponse({'success': True, 'id': instance.pk, 'message': 'Transaction saved successfully!'})
#
# @require_http_methods(["GET", "POST"])
# def delete_transaction(request, pk):
#     # Handles delete confirmation pop-up
#     transaction = get_object_or_404(Transaction, pk=pk)
#
#     if request.method == 'POST':
#         transaction.delete()
#         return JsonResponse({'success': True, 'message': 'Transaction deleted successfully!'})
#
#     return JsonResponse({
#         'amount': str(transaction.amount),
#         'type': transaction.get_type_display()
#     })
#
#
# def get_transaction_details(request, pk):
#     # Fetches existing transaction details to populate form
#     transaction = get_object_or_404(Transaction, pk=pk)
#
#     subclass_instance = transaction.get_subclass_instance()
#
#     data = {
#         'id': transaction.transactionId,
#         'amount': str(transaction.amount),
#         # 'accountId': transaction.accountId.pk,
#         'date': transaction.timestamp.strftime('%Y-%m-%d'),
#         'notes': transaction.notes,
#         'type': transaction.type,  # 'I', 'E', 'S', or 'T'
#     }
#
#     # Add fields specific to the transaction type
#     if transaction.type == 'I':
#         data['source'] = subclass_instance.source
#     elif transaction.type == 'E':
#         data['category'] = subclass_instance.categoryId.pk
#     elif transaction.type == 'S':
#         data['goal'] = subclass_instance.goalId.pk
#     else:
#         data['receiver'] = subclass_instance.receiverId.pk
#
#     return JsonResponse(data)