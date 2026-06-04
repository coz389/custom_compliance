from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList

class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context['response'] if renderer_context else None
        status_code = response.status_code if response else 200

        # if response data is already wrapped with 'success', return as is
        if isinstance(data, dict) and 'success' in data:
            return super().render(data, accepted_media_type, renderer_context)

        # Standard success response wrap
        view = renderer_context.get('view') if renderer_context else None
        
        # Determine the message
        message = self._get_message(view, status_code)
        
        # If data is a dict and already has a 'message', use it
        if isinstance(data, dict) and 'message' in data:
            message = data.pop('message')

        wrapped_data = {
            'success': True if status_code < 400 else False,
            'message': message,
            'data': data
        }

        # if error response with 'detail', wrap it without nesting under 'data'
        if status_code >= 400 and isinstance(data, dict) and 'detail' in data:
            wrapped_data['data'] = data 

        return super().render(wrapped_data, accepted_media_type, renderer_context)
    

    def _get_message(self, view, status_code):
        """
        Get message from view based on:
        1. view.response_message attribute (set in view methods)
        2. view.get_response_message() method
        3. Default messages based on HTTP method and status code
        """
        # 1. Check if view has custom message set directly
        if hasattr(view, 'response_message'):
            return view.response_message

        # 2. Check if view has get_response_message method
        if hasattr(view, 'get_response_message'):
            return view.get_response_message(status_code)

        # 3. Try to build a model-specific message if possible
        model_name = None
        if view and hasattr(view, 'queryset') and view.queryset is not None:
            model_name = view.queryset.model._meta.verbose_name.title()
        elif view and hasattr(view, 'serializer_class') and view.serializer_class is not None:
            if hasattr(view.serializer_class.Meta, 'model'):
                model_name = view.serializer_class.Meta.model._meta.verbose_name.title()

        # Default messages based on status code
        if status_code == 201:
            return f"{model_name} created successfully." if model_name else "Created successfully."
        elif status_code == 204:
            return f"{model_name} deleted successfully." if model_name else "Deleted successfully."

        default_messages = {
            200: 'Request successful.',
            201: 'Request creates successful.',
            400: 'Bad request.',
            401: 'Authentication required.',
            403: 'Permission denied.',
            404: 'Not found.',
            500: 'Server error.',
        }

        return default_messages.get(status_code, 'Request processed.')