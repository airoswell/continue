from haystack.forms import SearchForm


class ItemsSearchForm(SearchForm):

    def no_query_found(self):
        return self.searchqueryset.all()


# class PostsSearchForm(SearchForm):

#     def no_query_found(self):
#         return self.searchqueryset.all()
