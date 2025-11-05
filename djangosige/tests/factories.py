import factory
from django.contrib.auth import get_user_model
from factory import fuzzy


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = fuzzy.FuzzyText()
    password = fuzzy.FuzzyText()
