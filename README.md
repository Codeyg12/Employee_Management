## Todo
- Remove the `<a class="link-secondary text-decoration-none link-opacity-50-hover" href="{% url 'department' department.id %}">{{department.department_name}}</a>` from the clickable tables, are we comfortable with the style changes? Regardless its redundant to double up on the links
- Maybe do this for the go backs (<a href="javascript:history.go(-1)" class="btn btn-outline-light mb-3"><i class="fa-solid fa-arrow-left"></i></a>)
- When selecting role for new employee it auto adds department
- https://code.djangoproject.com/ticket/27562  https://stackoverflow.com/questions/16925129/generate-unique-id-in-django-from-a-model-field
- Change error page for user attemps I.E. user types in '/budget/112', custom 404 page (https://www.makeuseof.com/create-custom-404-error-page-django/)
- font awesome icons, do I keep the 'fa-sm' or do I want to make it large?
- set up database for live page, both in employee_manag - settings.py and mydb
- DRY OUT THIS CODE
- check for all unused vars
- Actual README