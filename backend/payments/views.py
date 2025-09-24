import os
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
import razorpay
from subscriptions.models import Payment, UserPlan


def get_client():
	return razorpay.Client(auth=(os.getenv('RAZORPAY_KEY_ID',''), os.getenv('RAZORPAY_KEY_SECRET','')))


class CreateOrderView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request):
		amount = int(float(request.data.get('amount', 0)) * 100)
		receipt = request.data.get('receipt', f"rcpt_{request.user.id}_{int(datetime.utcnow().timestamp())}")
		client = get_client()
		order = client.order.create({"amount": amount, "currency": "INR", "receipt": receipt})
		payment = Payment.objects.create(user=request.user, amount=amount/100, order_id=order['id'], receipt=receipt)
		return Response({"order": order, "payment_id": payment.id})


class CapturePaymentView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request):
		order_id = request.data.get('order_id')
		payment_id = request.data.get('payment_id')
		amount = int(float(request.data.get('amount')) * 100)
		client = get_client()
		client.payment.capture(payment_id, amount)
		Payment.objects.filter(order_id=order_id).update(payment_id=payment_id, status='captured')
		return Response({"status": "captured"})


class RefundPaymentView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request):
		payment_id = request.data.get('payment_id')
		client = get_client()
		# enforce within 1 day
		p = Payment.objects.filter(payment_id=payment_id, user=request.user).first()
		if not p:
			return Response({"detail": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
		if (datetime.utcnow() - p.created_at.replace(tzinfo=None)) > timedelta(days=1):
			return Response({"detail": "Refund window expired"}, status=status.HTTP_400_BAD_REQUEST)
		ref = client.payment.refund(payment_id)
		p.refunded = True
		p.refund_id = ref.get('id')
		p.status = 'refunded'
		p.save()
		return Response({"status": "refunded", "refund": ref})
