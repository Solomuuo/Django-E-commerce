import json
from django.shortcuts import redirect, render
from django.http import JsonResponse
from app.models import Cart, Order
from .stk_push import stk_push_request
from .models import MpesaTransaction
from django.contrib import messages
from uuid import uuid4
from django.views.decorators.csrf import csrf_exempt

def stk_push_view(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    # Calculate total amount
    famount = sum(p.quantity * p.product.discounted_price for p in cart_items)
    total_amount = int(famount + 100)  # Convert to int and add extra fees if any

    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        amount = int(float(request.POST.get("amount")))  # Convert to int

        # Generate a temporary receipt number
        temp_receipt_number = f"TMP-{uuid4().hex[:10]}"

        # Trigger STK Push request
        response = stk_push_request(amount, phone_number, temp_receipt_number)

        # Store the transaction in the database
        MpesaTransaction.objects.create(
            phone_number=phone_number,
            amount=amount,
            mpesa_receipt_number=temp_receipt_number,  # Store temporary receipt number
            status="Pending"
        )

        messages.success(request, "Payment Processing...")

        return redirect("orders")  # Ensure "orders" is a valid URL name

    return render(request, "mpesa/stk_push_form.html", {"total_amount": total_amount})


@csrf_exempt
def mpesa_callback(request):
    """Handles the STK push callback from Safaricom."""
    try:
        data = json.loads(request.body)
        result_code = data.get("Body", {}).get("stkCallback", {}).get("ResultCode")
        receipt_number = data.get("Body", {}).get("stkCallback", {}).get("CallbackMetadata", {}).get("Item", [])[1].get("Value", "")

        # Get the pending transaction
        transaction = MpesaTransaction.objects.filter(mpesa_receipt_number__startswith="TMP-").first()

        if transaction:
            if result_code == 0:
                transaction.status = "Completed"
                transaction.mpesa_receipt_number = receipt_number  # Update with real receipt number
                transaction.save()

                # ✅ Ensure the user exists in the transaction (modify if necessary)
                user = transaction.user if hasattr(transaction, 'user') else None
                if user is None:
                    return JsonResponse({"error": "User not found for transaction"}, status=400)

                # ✅ Fetch cart items for the user
                cart_items = Cart.objects.filter(user=user)

                if not cart_items:
                    return JsonResponse({"error": "No items in cart"}, status=400)

                # ✅ Create orders for each cart item
                for cart_item in cart_items:
                    Order.objects.create(
                        user=user,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        amount=cart_item.quantity * cart_item.product.discounted_price,
                        status="Pending",
                        shipped=False
                    )

                # ✅ Clear the cart after successful payment
                cart_items.delete()

            else:
                transaction.status = "Failed"
                transaction.save()

        return JsonResponse({"status": "success"}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
def transaction_history(request):
    """ View for displaying transaction history """
    transactions = MpesaTransaction.objects.all().order_by('-transaction_date')
    return render(request, 'mpesa/transaction_history.html', {'transactions': transactions})
