from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .request_local import get_current_request
import json
@receiver(pre_save)
def pre_save_handler(sender, instance, **kwargs):
    # Ignore UserActivityLog model itself
    if sender.__name__ == 'UserActivityLog':
        return
    
    request = get_current_request()
    user = request.user if request and request.user.is_authenticated else None

    if not instance.pk:  # Creating
        if hasattr(instance, 'created_by') and not instance.created_by:
            instance.created_by = user
    else:  # Updating
        if hasattr(instance, 'updated_by'):
            instance.updated_by = user
        
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            instance._old_instance = old_instance
        except sender.DoesNotExist:
            pass

@receiver(post_save)
def post_save_handler(sender, instance, created, **kwargs):
    if sender.__name__ in ['UserActivityLog', 'Migration'] or not hasattr(instance, '_meta'):
        return
    request = get_current_request()
    user = request.user if request and request.user.is_authenticated else None
    
    old_instance = getattr(instance, '_old_instance', None)

    if created:
        action = 'CREATE'
        changes = f'{sender.__name__} created a new record.'
    else:
        if old_instance and old_instance.deleted_at is None and instance.deleted_at is not None:
            action = 'DELETE'
            changes = f'{sender.__name__} record soft-deleted.'
        else:
            action = 'UPDATE'
            changes = f'{sender.__name__} record updated.'

        if old_instance:
            changed_fields = {}
            for field in instance._meta.fields:
                if field.name in ['updated_at', 'updated_by']:
                    continue
                old_val = getattr(old_instance, field.name)
                new_val = getattr(instance, field.name)
                if old_val != new_val:
                    changed_fields[field.name] = {'old': str(old_val), 'new': str(new_val)}
            changes = changed_fields if changed_fields else None

    def sanitize_data(data):
        if not data:
            return None
        # Create a copy and remove non-serializable Django internal state
        clean_dict = {k: v for k, v in data.items() if k != '_state'}
        # Convert non-serializable objects to string
        for k, v in clean_dict.items():
            try:
                if hasattr(v, 'isoformat'):
                    clean_dict[k] = v.isoformat()
                elif hasattr(v, 'name') and hasattr(type(v), 'url') and isinstance(type(v).url, property):
                    # Check if it's a file field without triggering its properties if possible
                    # or just use the fact that bool(v) is False for empty file fields
                    clean_dict[k] = str(v.name) if v else None
                elif not isinstance(v, (str, int, float, bool, type(None), dict, list)):
                    clean_dict[k] = str(v)
            except Exception:
                try:
                    clean_dict[k] = str(v)
                except Exception:
                    clean_dict[k] = "<Unserializable>"
        return clean_dict

    # Lazy import to avoid early loading
    from core.models import UserActivityLog
    from django.db import connection
    
    # Safety check for migrations or missing table
    if 'user_activity_logs' not in connection.introspection.table_names():
        return

    UserActivityLog.objects.create(
        user=user,
        action_name=action,
        model_name=sender.__name__,
        object_id=instance.pk,
        before_input=sanitize_data(old_instance.__dict__) if old_instance else None,
        after_input=sanitize_data(instance.__dict__),
        description=changes if changes else None,
        ip_address=request.META.get('REMOTE_ADDR') if request else None,
        user_agent=request.META.get('HTTP_USER_AGENT') if request else None,
    )