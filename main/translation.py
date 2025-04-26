from modeltranslation.translator import translator, TranslationOptions
from .models import HomeSlider , Announcement

class HomeSliderTranslationOptions(TranslationOptions):
    fields = ('heading', 'subheading', 'button_text')

class AnnouncementTranslationOptions(TranslationOptions):
    fields = ('title',)

translator.register(HomeSlider, HomeSliderTranslationOptions)
translator.register(Announcement, AnnouncementTranslationOptions)