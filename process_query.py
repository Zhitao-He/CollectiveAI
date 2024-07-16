import re

GUIDANCE = (
    'Here are some useful guidelines you need to follow:\n'
    'Action Related\n'
    '- Use the `open_app` action whenever you want to open an app'
    ' (nothing will happen if the app is not installed), do not use the'
    ' app drawer to open an app unless all other ways have failed.\n'
    '- Use the `input_text` action whenever you want to type'
    ' something (including password) instead of clicking characters on the'
    ' keyboard one by one. Sometimes there is some default text in the text'
    ' field you want to type in, remember to delete them before typing.\n'
    '- For `click`, `long_press` and `input_text`, the index parameter you'
    ' pick must be VISIBLE in the screenshot and also in the UI element'
    ' list given to you (some elements in the list may NOT be visible on'
    ' the screen so you can not interact with them).\n'
    '- Consider exploring the screen by using the `scroll`'
    ' action with different directions to reveal additional content.\n'
    '- The direction parameter for the `scroll` action can be confusing'
    " sometimes as it's opposite to swipe, for example, to view content at the"
    ' bottom, the `scroll` direction should be set to "down". It has been'
    ' observed that you have difficulties in choosing the correct direction, so'
    ' if one does not work, try the opposite as well.\n'
    '\n\nNow output an action from the above list in the correct JSON format,'
    ' following the reason why you do that. Your answer should look like:\n'
    'Reason: ...\nAction: {{"action_type":...}}\n\n'
    'Your Answer:\n'
)

text = '''
The current user goal/request is: Open the file task.html in Downloads in the file manager; when prompted open it with Chrome. Then navigate the X to the bottom-right cell, by using the direction buttons.

Here is a history of what you have done so far:
Step 1: Action selected: {"action_type": "navigate_home"}. Navigated to the home screen to access the app drawer for opening the file manager, as the file manager app was not directly visible on the initial screen.
Step 2: Action selected: {"action_type": "scroll", "direction": "down"}. Scrolled down on the home screen to reveal more apps in search of the file manager; the action was successful in showing additional apps, but the file manager is not yet visible. Need to continue searching or consider alternative methods to access the file manager....

Here is a list of descriptions for some UI elements on the current screen:

UI element 2: UIElement(text=None, content_description='Share', class_name='android.widget.TextView', bbox=None, bbox_pixels=BoundingBox(x_min=700, x_max=827, y_min=128, y_max=254), hint_text=None, is_checked=False, is_checkable=False, is_clickable=True, is_editable=False, is_enabled=True, is_focused=False, is_focusable=True, is_long_clickable=False, is_scrollable=False, is_selected=False, is_visible=True, package_name='com.google.android.documentsui', resource_name='com.google.android.documentsui:id/action_menu_share', tooltip=None, resource_id=None)
UI element 3: UIElement(text=None, content_description='Delete', class_name='android.widget.TextView', bbox=None, bbox_pixels=BoundingBox(x_min=827, x_max=954, y_min=128, y_max=254), hint_text=None, is_checked=False, is_checkable=False, is_clickable=True, is_editable=False, is_enabled=True, is_focused=False, is_focusable=True, is_long_clickable=False, is_scrollable=False, is_selected=False, is_visible=True, package_name='com.google.android.documentsui', resource_name='com.google.android.documentsui:id/action_menu_delete', tooltip=None, resource_id=None)...

Here are some useful guidelines you need to follow:
General
- Usually there will be multiple ways to complete a task, pick the easiest one. Also when something does not work as expected (due to various reasons), sometimes a simple retry can solve the problem, but if it doesn't (you can see that from the history), try to switch to other solutions.
- Sometimes you may need to navigate the phone to gather information needed to complete the task, for example if user asks "what is my schedule tomorrow", then you may want to open the calendar app (using the `open_app` action), look up information there, answer user's question (using the `answer` action) and finish (using the `status` action with complete as goal_status)....
'''
def remove_UI_property(text):
    # 定义要去除的字段
    fields_to_remove = ['class_name', 'hint_text', 'bbox', 'bbox_pixels', 'package_name', 'resource_name', 'tooltip', 'resource_id']

    # 构建正则表达式模式，包含特殊处理的bbox_pixels字段
    pattern = r',?\s*(%s)=(?:BoundingBox\([^)]*\)|[^,)]*)' % '|'.join(fields_to_remove)

    # 使用正则表达式去除匹配的字段
    cleaned_text = re.sub(pattern, '', text)

    return cleaned_text

def remove_guidelines(text):
    start_index = text.find("Here are some useful guidelines you need to follow:")

    # 保留目标字符串之前的所有内容
    if start_index != -1:
        text = text[:start_index]

    return text

print(text)

cleaned_text = remove_UI_property(text)

print('=========')
print('\n')
print(cleaned_text)

cleaned_text = remove_guidelines(cleaned_text)
print('=========')
print('\n')
print(cleaned_text)

cleaned_text = cleaned_text + GUIDANCE
print('=========')
print('\n')
print(cleaned_text)