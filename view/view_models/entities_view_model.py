from kivymd.toast import toast

from data.model.model import Entity
from data.repository.result import Result
from view.common_confirmation import ConfirmDialog


class EntitiesViewModel:
    def __init__(self, repository, refresh_view_callback, name):
        self.repo = repository
        self.refresh_view = refresh_view_callback
        self.name = name
        self.dialog = None
        self.edited_item = None
        self.filter_class = None
        self.filter_text = None

    def on_edit_enter(self, item):
        pass

    def on_delete_enter(self, item: Entity):
        ConfirmDialog(f'Удалить запись о лице {item.get_fullname()}?', self.delete_item, item)

    def delete_item(self, item):
        result, result_text = self.repo.delete_entity(item)
        if result == Result.SUCCESS:
            self.refresh_view(self.name)
        toast(result_text)
