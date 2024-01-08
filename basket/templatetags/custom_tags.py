from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def paginated_url(context, page_number):
    request = context['request']
    category_id = request.GET.get('category', '')

    # Remove the 'page' parameter if it's already in the URL
    params = request.GET.copy()
    if 'page' in params:
        params.pop('page')

    # Add 'category' and 'page' parameters to the URL if category_id is present
    if category_id:
        params['category'] = category_id
    params['page'] = page_number

    return f"?{params.urlencode()}"
