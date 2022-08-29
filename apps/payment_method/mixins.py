from apps.payment_method import usecases

class ProviderMixins:
    def get_provider(self):
        return usecases.GetProviderUseCase(
            provider_payment_id = self.kwargs.get('provider_payment_id')
        ).execute()

class VoucherMixins:
    def get_voucher(self):
        return  usecases.GetVoucherUseCase(
            voucher_id=self.kwargs.get('voucher_id')
        ).execute()