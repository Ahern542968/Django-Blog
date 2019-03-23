from haystack import indexes
from .models import Blog


class BlogIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Blog

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(status=self.get_model().STATUS_NORMAL)

    class Meta:
        fields = ['title', 'content']
