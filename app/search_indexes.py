from app.models import Post
from haystack import indexes


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    detail = indexes.CharField(model_attr='detail')
    zip_code = indexes.CharField(model_attr='zip_code')
    time_posted = indexes.DateTimeField(model_attr="time_posted")

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
