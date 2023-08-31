from .base import DynamicListInit, DynamicTable, DynamicGrid


class BaseListingFactory:
    def __init__(self, model, dynamic_list, filterset_class=None, listing_type=None,
                 listing_actions=None, actions_template_name=None, header_template_name=None, bulk_actions=False,
                 extra_context=None, media=None, header=None):
        self.factory = True
        self.model = model
        self.dynamic_list = dynamic_list
        self.filterset_class = filterset_class
        self.listing_type = listing_type
        self.bulk_actions = bulk_actions
        self.listing_actions = listing_actions
        self.actions_template_name = actions_template_name
        self.header_template_name = header_template_name
        self.extra_context = extra_context or {}
        self.header = header
        self.factory_media = media or {}
        self.create_dynamic_listing(dynamic_list)

    def create_dynamic_listing(self, dynamic_list):
        class Media:
            js = getattr(self.dynamic_list, 'Media', {}).js + getattr(self, 'factory_media', {}).get('js', tuple())
            css = getattr(self.dynamic_list, 'Media', {}).css
            for medium, styles in getattr(self, 'factory_media', {}).get('css', {}).items():
                css.setdefault(medium, []).extend(styles)

        self.Listing = type(
            self.model.__name__ + 'DynamicListing',
            (dynamic_list, DynamicListInit),
            {'Media': Media, **self.__dict__}
        )

    def __call__(self, *args, **kwargs):
        return self.Listing(*args, **kwargs)


class DynamicTableFactory(BaseListingFactory):
    def __init__(self, model, dynamic_list=DynamicTable,
                 table_columns=None, load_rows_from_template=False,

                 row_template_name=None, **kwargs):
        self.table_columns = table_columns
        self.load_rows_from_template = load_rows_from_template
        self.row_template_name = row_template_name
        super().__init__(model, dynamic_list, listing_type='table', **kwargs)


class DynamicGridFactory(BaseListingFactory):
    def __init__(self, model, dynamic_list=DynamicGrid, item_template_name=None, **kwargs):
        self.item_template_name = item_template_name
        super().__init__(model, dynamic_list, listing_type='grid', **kwargs)


class DynamicListFactory(BaseListingFactory):
    def __init__(self, model, dynamic_list=DynamicGrid, item_template_name=None, **kwargs):
        self.item_template_name = item_template_name
        super().__init__(model, dynamic_list, listing_type='list', **kwargs)
