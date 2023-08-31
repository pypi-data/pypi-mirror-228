from django.views.generic import ListView
from django_filters.views import FilterView

from .base import DynamicTable, DynamicGrid, DynamicList


class BaseDynamicListingView(ListView, FilterView):
    title = None
    template_name = 'dynamic_listing/index.html'

    def __init__(self, request=None, queryset=None, *args, **kwargs):
        self.request = self.request
        super(BaseDynamicListingView, self).__init__(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(BaseDynamicListingView, self).get_context_data(**kwargs)
        context["breadcrumb"] = self.get_breadcrumb()
        context['title'] = self.get_title()
        return context

    def get_breadcrumb(self):
        return []

    def get_title(self):
        return self.title


class DynamicTableView(BaseDynamicListingView, DynamicTable):
    pass


class DynamicGridView(BaseDynamicListingView, DynamicGrid):
    pass


class DynamicListView(BaseDynamicListingView, DynamicList):
    pass
