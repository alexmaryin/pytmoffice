from data.repository.intel_repo import EntityCategory


class LegalViewModel:
    def __init__(self, repository, refresh_view_callback):
        self.repo = repository
        self.refresh_view = refresh_view_callback
        self.dialog = None
        self.edited_item = None
        self.filter_class = None
        self.filter_text = None
        self.view_class = None

    def show_items(self) -> list[dict]:
        legals_data = self.repo.get_entities(category=EntityCategory.Legals)
        data_dict = []
        for item in legals_data:
            data_dict.append({
                'main_text': f'{item.get_fullname()}',
                'second_text': f'{item.get_simple_line()}',
                'selected': item,
                'rv_key': item.id,
                'edit_callback': self.on_edit_enter,
                'delete_callback': self.on_delete_enter
            })
        return data_dict

    def on_edit_enter(self, instance):
        pass

    def on_delete_enter(self, instance):
        pass

    def show_managed_legals(self):
        pass
