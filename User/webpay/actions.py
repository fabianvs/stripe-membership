# from back.certificates import cert_normal
# from tbk.services import WebpayService
# from tbk.commerce import Commerce
# from .utils import _read_file
from transbank.error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_api_keys import IntegrationApiKeys
from transbank.common.integration_type import IntegrationType
# def init():
# 	certificate   = cert_normal.certDictionary.dictionaryCert();
# 	enviromet     = certificate['environment']
# 	commerce_code = certificate['commerce_code'];
# 	key_data      = _read_file(certificate['private_key']);
# 	cert_data     = _read_file(certificate['public_cert']);
# 	tbk_cert_data = _read_file(certificate['webpay_cert']);
# 	commerce      = Commerce(commerce_code, key_data, cert_data, tbk_cert_data, enviromet)
# 	webpay        = WebpayService(commerce)

# 	return webpay

def initTransaction(buy_order, session_id, amount, return_url):
    tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))

    # tx.create(buy_order, session_id, amount, return_url)
    response = tx.create(buy_order, session_id, amount, return_url)
    return response
