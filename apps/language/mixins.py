from apps.language.usecases import GetLanguageUseCase
class LanguageMixins:
    def get_language(self):
        return GetLanguageUseCase(
            language_id=self.kwargs.get('language_id')
        ).execute()