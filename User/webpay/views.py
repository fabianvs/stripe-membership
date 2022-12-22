
# from braces.views import LoginRequiredMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse
from .actions import initTransaction


class TbkInit(TemplateView):
    def get(self, request, *args, **kwargs):
        amount           = 2000
        buy_order        = "1"
        session_id       = "1"
        return_url       = "http://localhost:8000/cart/return/"
        final_url        = "http://localhost:8000/cart/final/"

        # transaction      = initTransaction(amount, buy_order, return_url, final_url)
        transaction      = initTransaction(buy_order, session_id, amount, return_url)

        context          = {
            'subscription': {
                'name': 'Suscripción Profesor',
                'value': 2000,
            },
            'transaction' : transaction,
        }

        return render(request, "webpay/init.html", context)