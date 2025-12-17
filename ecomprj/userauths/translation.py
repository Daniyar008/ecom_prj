from modeltranslation.translator import register, TranslationOptions
from .models import Profile, ContactUs


@register(Profile)
class ProfileTranslationOptions(TranslationOptions):
    fields = (
        "full_name",
        "bio",
        "address",
        "country",
    )


@register(ContactUs)
class ContactUsTranslationOptions(TranslationOptions):
    fields = (
        "full_name",
        "subject",
        "message",
    )
