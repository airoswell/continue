from django.template import Library

register = Library()


@register.filter_function
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)


@register.filter(name='find_requester_in_post')
def find_requester_in_post(item, post):
    q = item.status_in_post.filter(post=post)
    if q:
        status = q[0]
    return status.item_requesters.all()


@register.filter(name='truncate')
def truncate(string, limit):
    if len(string) <= limit:
        return string
    else:
        return string[0:limit] + " ..."


@register.filter(name='unread_count')
def unread_count(queryset):
    return queryset.filter(read_at=None).count()


@register.filter(name='model_name')
def model_name(record):
    return record.__class__.__name__


@register.filter(name='split')
def filter(string, delimiter):
    if not string:
        return []
    return string.split(delimiter)
