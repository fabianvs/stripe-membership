from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .actions import initTransaction, commitTransaction
from User.models import Order, PaymentHistory, OrderStatus, UserSubscription
from django.core.exceptions import ObjectDoesNotExist
from transbank.error.transaction_commit_error import TransactionCommitError

class TbkInit(TemplateView):
	def get(self, request, *args, **kwargs):
		order_pk=self.kwargs.get('pk')
		try:            
			order = Order.objects.get(pk=order_pk, user=request.user)
			amount = order.total
			buy_order = order.id
			session_id = request.session.session_key
			return_url = "http://localhost:8000/suscripcion/return/"

			transaction = initTransaction(str(buy_order), session_id, amount, return_url)

			context = {
				'order':{
					'id': order.id,
					'tax': f"{order.tax:,}",
					'total': f"{order.total:,}",
					'subscription': {
						'name': order.subscription.name,
						'value': f"{order.subscription.value:,}",
					},
				},
				'transaction' : transaction,
			}
			return render(request, "webpay/init.html", context)
		except ObjectDoesNotExist as e:
			return redirect('home')

class TbkReturn(TemplateView):

	def get(self, request, *args, **kwargs):
		if(request.GET.get("token_ws")):
			token = request.GET["token_ws"]
		else: 
			token = request.GET["TBK_TOKEN"]

		try:
			transaction = commitTransaction(token)

			if(transaction["vci"] == "TSY"):
				installments_amount = None
				installments_number = None

				if(transaction['payment_type_code'] != 'VD' and transaction['payment_type_code'] != 'VN'):
					installments_amount = transaction['installments_amount']
					installments_number = transaction['installments_number']

				order = Order.objects.get(pk=transaction['buy_order'])

				if(order.status.pk != 2):
					payment = PaymentHistory.objects.create(
						user = request.user,
						buy_order = transaction['buy_order'],
						session_id =transaction['session_id'],
						amount = transaction['amount'],
						vci = transaction['vci'],
						status = transaction['status'],
						card_number = transaction['card_detail']['card_number'],
						accounting_date = transaction['accounting_date'],
						transaction_date = transaction['transaction_date'],
						authorization_code = transaction['authorization_code'],
						payment_type_code = transaction['payment_type_code'],
						response_code= transaction['response_code'],
						installments_amount = installments_amount,
						installments_number = installments_number
						# balance = transaction['balance']
					)

					order_status = OrderStatus.objects.get(pk=2)
					order.status = order_status
					order.save()
					try:
						user_subscription = UserSubscription.objects.get(user=request.user, subscription=order.subscription)
						user_subscription.active=True
						# Acá se puede agregar el tiempo para finalizar la suscripción y pedir renovación
						# user_subscription.finish = transaction['transaction_date'] + 1 año
						user_subscription.save()
					except ObjectDoesNotExist:
						UserSubscription.objects.create(user=request.user, subscription=order.subscription, active=True)

				else:
					payment = PaymentHistory.objects.get(buy_order=transaction['buy_order'], status=transaction['status'])

				return render(request, "webpay/success.html", {
					'payment' : payment,
					'token' : token
				})
			else:
				return render(request, "webpay/failure.html", {
					'transaction' : transaction,
					'token' : token
				})
		except TransactionCommitError as error:
			print("error: ", error.code)
			return render(request, "webpay/failure.html", {
				'error_code' : error.code,
				'token' : token
			})


