from volworld_common.test.behave.BehaveUtil import BehaveUtil
from behave import *
from api.A import A
from volworld_aws_api_common.test.behave.selenium_utils import w__get_element_by_shown_dom_id, w__click_element_by_dom_id, w__assert_element_existing, \
    w__key_in_element_by_dom_id


@when('{mentor} input {title} as title and {description} as description for new chapter')
def when__input_title_description(c, mentor: str, title: str, description: str):
    w__key_in_element_by_dom_id(c, [A.Chapter, A.Title], BehaveUtil.clear_string(title))
    w__key_in_element_by_dom_id(c, [A.Chapter, A.Description], BehaveUtil.clear_string(description))
