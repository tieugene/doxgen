from django.conf import settings


def support_email(_) -> dict:
    """
    Inject support email (for footer)
    :param _: ordinary must be request
    :return: 1st admin_name,admin_email
    """
    return {'support_email': settings.ADMINS[0] if settings.ADMINS else None}
