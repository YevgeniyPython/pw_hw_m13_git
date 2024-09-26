class UserRouter:
    """
    Маршрутизатор базы данных для приложения 'quotes'.
    """
    route_app_labels = {'user'}

    def db_for_read(self, model, **hints):
        """
        Указывает базу данных для операций чтения.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'db_users'
        return None

    def db_for_write(self, model, **hints):
        """
        Указывает базу данных для операций записи.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'db_users'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Указывает, разрешены ли отношения между объектами.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Указывает, может ли приложение мигрировать в указанную базу данных.
        """
        if app_label in self.route_app_labels:
            return db == 'db_users'
        return None
