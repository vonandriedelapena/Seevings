from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Transaction, Income, Expense, Saving, Transfer, Category

from Account.models import Account
from GoalSetter.models import Goal
from datetime import datetime

import json

def transaction_list_view(request):
    return render(request, 'transactionList.html')

def load_categories(request):
    categories = Category.objects.all()
    data = [{'id': c.pk, 'name': c.name} for c in categories]
    return JsonResponse({'categories': data})

def load_goals(request):
    goals = Goal.objects.all()
    data = [{'id': g.pk, 'name': g.name} for g in goals]
    return JsonResponse({'goals': data})

def load_accounts(request):
    accounts = Account.objects.all()
    data = [{'id': a.pk, 'createdAt': a.createdAt} for a in accounts]
    return JsonResponse({'accounts': data})

def load_transactions(request):
    transactions = Transaction.objects.all().order_by('-timestamp')
    data = []

    for t in transactions:
        try:
            sub = t.get_subclass_instance()
        except Exception:
            # Missing child row — skip or treat as base transaction
            sub = None

        row = {
            'id': t.transactionId,
            'type': t.type,
            'amount': float(t.amount),
            'notes': t.notes,
            'timestamp': t.timestamp.strftime('%Y-%m-%d'),
        }

        if sub:
            if t.type == 'E':
                row['category'] = sub.categoryId.name
                row['name'] = sub.name
            elif t.type == 'I':
                row['source'] = sub.source
            elif t.type == 'S':
                row['goal'] = sub.goalId.name
            elif t.type == 'T':
                row['receiver'] = sub.receiverId

        data.append(row)

    return JsonResponse({'transactions': data})

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

        # Assign string directly; do NOT treat as Account FK
        receiver_value = data.get('receiver', '').strip()
        if not receiver_value:
            raise ValueError("Receiver cannot be empty for Transfer")
        instance.receiverId = receiver_value

    return instance

@csrf_exempt
@require_http_methods(["POST"])
def save_transaction(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    transaction_id = data.get('transaction_id')
    new_type = data.get('type')

    ModelClass = {
        'I': Income,
        'E': Expense,
        'S': Saving,
        'T': Transfer
    }.get(new_type)

    if not ModelClass:
        return JsonResponse({'error': 'Invalid transaction type.'}, status=400)

    try:
        if transaction_id:
            parent_instance = get_object_or_404(Transaction, pk=transaction_id)

            # If type changed, delete old subclass and create new subclass
            if parent_instance.type != new_type:
                # Delete old subclass instance
                try:
                    old_sub = parent_instance.get_subclass_instance()
                    old_sub.delete()
                except Exception:
                    pass  # No subclass, ignore

                # Create new subclass linked to the same Transaction ID
                instance = ModelClass(transactionId=parent_instance.transactionId)
            else:
                instance = parent_instance.get_subclass_instance()
        else:
            instance = ModelClass()

        # Process all fields (amount, notes, type, subclass fields)
        instance = _process_transaction_data(data, ModelClass, instance)
        instance.save()

        response_data = {
            'success': True,
            'transaction_id': instance.pk,
            'type': instance.type,
            'amount': str(instance.amount),
            'date': instance.timestamp.strftime('%Y-%m-%d'),
            'notes': instance.notes,
            'source': getattr(instance, 'source', None),
            'category': getattr(instance, 'categoryId_id', None),
            'goal': getattr(instance, 'goalId_id', None),
            'receiver': getattr(instance, 'receiverId', None),
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