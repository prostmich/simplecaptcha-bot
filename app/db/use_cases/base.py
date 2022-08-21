from app.db.storages.factory import StorageFactory


class BaseUseCase:
    def __init__(self, storage_factory: StorageFactory):
        self.storage_factory = storage_factory
