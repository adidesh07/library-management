from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def paginate_query(querylist: list, items_per_page: int = 20, page_num: int = 1) -> list:
    query_paginator = Paginator(querylist, items_per_page)

    try:
        paginated_querylist = query_paginator.page(page_num)
    except PageNotAnInteger:
        paginated_querylist = query_paginator.page(items_per_page)
    except EmptyPage:
        paginated_querylist = query_paginator.page(query_paginator.num_pages)

    return paginated_querylist
