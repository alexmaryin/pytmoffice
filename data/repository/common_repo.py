from sqlalchemy.exc import DBAPIError
from .result import Result


class CommonRepository:
    def __init__(self, database):
        self.source = database.session

    def common_add_item(self, item, override_success=None, override_error=None) -> (Result, str):
        try:
            self.source.add(item)
            self.source.commit()
            return Result.SUCCESS, override_success or 'Новая запись внесена в базу'
        except DBAPIError as e:
            print(e)
            self.source.rollback()
            return Result.ERROR, override_error or 'Ошибка при записи нового элемента в базу'

    def common_edit_item(self, item, override_success=None, override_error=None) -> (Result, str):
        try:
            if item in self.source.dirty:
                self.source.flush()
                return Result.SUCCESS, override_success or 'Изменения сохранены'
            else:
                return Result.EMPTY, 'Никаких изменений'
        except DBAPIError as e:
            print(e)
            self.source.rollback()
            return Result.ERROR, override_error or 'Ошибка при сохранении изменений'

    def common_delete_item(self, item, override_success=None, override_error=None) -> (Result, str):
        try:
            self.source.delete(item)
            self.source.commit()
            return Result.SUCCESS, override_success or 'Запись удалена из базы'
        except DBAPIError as e:
            print(e)
            self.source.rollback()
            return Result.ERROR, override_error or 'Удаление невозможно (скорее всего из-за нарушения целостности данных)'
