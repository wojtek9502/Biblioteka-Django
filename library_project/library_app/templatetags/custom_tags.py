from django import template

register = template.Library()


@register.simple_tag(name='free_bookcopies_counter_tag')
def free_bookcopies_counter(bookcopies_obj):
    return bookcopies_obj.filter(is_borrowed=False).count()


    
