"""Simple helper to paginate query
"""
import math
from urllib import response
from flask import url_for, request
import itertools

DEFAULT_PAGE_SIZE = 50
DEFAULT_PAGE_NUMBER = 1


def extract_pagination(page=None, per_page=None, **request_args):
    page = int(page) if page is not None else DEFAULT_PAGE_NUMBER
    per_page = int(per_page) if per_page is not None else DEFAULT_PAGE_SIZE
    return page, per_page, request_args


def paginate(query, schema, sub_schema=None):
    page, per_page, other_request_args = extract_pagination(**request.args)
    page_obj = query.paginate(page=page, per_page=per_page)

    next_ = url_for(
        request.endpoint,
        page=page_obj.next_num if page_obj.has_next else page_obj.page,
        per_page=per_page,
        **other_request_args,
        **request.view_args
    )
    prev = url_for(
        request.endpoint,
        page=page_obj.prev_num if page_obj.has_prev else page_obj.page,
        per_page=per_page,
        **other_request_args,
        **request.view_args
    )
    return {
        "total": page_obj.total,
        "pages": page_obj.pages,
        "next": next_,
        "prev": prev,
        "results": schema.dump(page_obj.items),
    }


def paginate_list(list, sub_schema=None):
    page, per_page, other_request_args = extract_pagination(**request.args)

    list_size = len(list)
    available_number_of_page = math.ceil(list_size/per_page)
    next_ = url_for(
        request.endpoint,
        page=page + 1 if page < available_number_of_page else page,
        per_page=per_page,
        **other_request_args,
        **request.view_args
    )
    prev = url_for(
        request.endpoint,
        page=page - 1 if (page < available_number_of_page and page > 1) else page,
        per_page=per_page,
        **other_request_args,
        **request.view_args
    )
    return {
        "total": list_size,
        "pages": available_number_of_page,
        "next": next_,
        "prev": prev,
        "results": list
    }