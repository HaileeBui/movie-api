from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class WatchlistPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 10
    last_page_strings = 'end'

#more control in data range returned, more flexible
class WatchlistLOPagination(LimitOffsetPagination):
    default_limit = 1
    max_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'start'
 
#have to go through each page to last page
class WatchlistCPagination(CursorPagination):
    page_size = 2
    ordering = 'created'
    cursor_query_param = 'record'