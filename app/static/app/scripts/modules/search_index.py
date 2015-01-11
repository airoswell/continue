import datetime
from app.models import Item
from haystack import indexes


class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, user_template=True)
    title = indexes.CharField(model_attr='title')
    time_created = indexes.DateTimeField(model_attr='time_created')

    def get_model(self):
        return Item

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            time_created__lte=datetime.datetime.now()
        )
