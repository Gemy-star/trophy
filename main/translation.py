from modeltranslation.translator import translator, TranslationOptions
from .models import Category

class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

translator.register(Category, CategoryTranslationOptions)
