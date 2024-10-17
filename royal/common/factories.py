import factory

from royal.common.models import RandomModel, SimpleModel

from utils.tests.base import faker


class RandomModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RandomModel
    
    end_date = factory.LazyAttribute(lambda self: faker.date_object())
    start_date = factory.LazyAttribute(lambda self: faker.date_object(end_datetime=self.end_date))


class SimpleModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RandomModel

    name = factory.LazyAttribute(lambda self:faker.word() )