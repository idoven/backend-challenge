class NotUniqueUserError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class UserAccessDeniedError(Exception):
    pass


class UserSelfDeletionError(Exception):
    pass
