from app.models import Post, Item
from haystack import indexes


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    # these fields are used to narrow down data
    title = indexes.CharField(model_attr='title')
    detail = indexes.CharField(model_attr='detail')
    area = indexes.CharField(model_attr='area')
    tags = indexes.CharField(model_attr="tags")
    visibility = indexes.CharField(model_attr="visibility")
    secret_key = indexes.CharField(model_attr="secret_key")
    time_created = indexes.DateTimeField(model_attr="time_created")

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class ItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    # these fields are used to narrow down data
    owner = indexes.CharField(model_attr='owner')
    tags = indexes.CharField(model_attr="tags")
    tags_private = indexes.CharField(model_attr="tags_private")

    def get_model(self):
        return Item

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
