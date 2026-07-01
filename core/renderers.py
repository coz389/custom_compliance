from rest_framework.renderers import JSONRenderer

class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context['response'] if renderer_context else None
        status_code = response.status_code if response else 200

        # Bypass — already wrapped (login jaise endpoints)
        if isinstance(data, dict) and 'status' in data and 'results' in data:
            return super().render(data, accepted_media_type, renderer_context)

        view = renderer_context.get('view') if renderer_context else None
        message = self._get_message(view, status_code)

        if isinstance(data, dict) and 'message' in data:
            message = data.pop('message')

        # ── Paginated response — flat structure ──────────────────
        if isinstance(data, dict) and data.get('__paginated'):
            data.pop('__paginated')
            wrapped_data = {
                'status': status_code,
                'message': message,
                **data          # count, total_pages, page, page_size, results
            }
            return super().render(wrapped_data, accepted_media_type, renderer_context)
        # ─────────────────────────────────────────────────────────

        # Standard response
        wrapped_data = {
            'status': status_code,
            'message': message,
            'results': data
        }

        if status_code >= 400 and isinstance(data, dict) and 'detail' in data:
            wrapped_data['results'] = data

        return super().render(wrapped_data, accepted_media_type, renderer_context)

    def _get_message(self, view, status_code):
        if hasattr(view, 'response_message'):
            return view.response_message
        if hasattr(view, 'get_response_message'):
            return view.get_response_message(status_code)

        model_name = None
        if view and hasattr(view, 'queryset') and view.queryset is not None:
            model_name = view.queryset.model._meta.verbose_name.title()
        elif view and hasattr(view, 'serializer_class') and view.serializer_class is not None:
            if hasattr(view.serializer_class, 'Meta') and hasattr(view.serializer_class.Meta, 'model'):
                model_name = view.serializer_class.Meta.model._meta.verbose_name.title()

        if status_code == 201:
            return f"{model_name} created successfully." if model_name else "Created successfully."
        if status_code == 204:
            return f"{model_name} deleted successfully." if model_name else "Deleted successfully."

        return {
            200: 'Request successful.',
            400: 'Bad request.',
            401: 'Authentication required.',
            403: 'Permission denied.',
            404: 'Not found.',
            500: 'Server error.',
        }.get(status_code, 'Request processed.')