from jinja2 import Template

#Шаблон спецификации страницы
spec_page = Template("""
<h2>Спецификация таблицы - {{ table_schema }}.{{ table_name }}</h2>
<table>
<tr><th><b>Наименование поля</b></th><th><b>Тип данных</b></th><th><b>Nullable</b></th><th><b>Default</b></th><th><b>Описание поля</b></th></tr>
{% for col in columns %}
<tr><td>{{ col[0] }}</td><td>{{ col[1] }}({{ col[2] }})</td><td>{{ col[3] }}</td><td>{{ col[4] }}</td><td>{{ col[6] if col[6] is not none else col[7]}} {{ col[5] }}</td></tr>
{% endfor %}
</table>
<h2><b>Индексы</b></h2>
<table>
<tr><th><b>Наименование индекса</b></th><th><b>Состав полей</b></th></tr>
{% for index in indexes %}
<tr><td>{{ index[0] }}</td><td>{{ index[1] }}</td></tr>
{% endfor %}
</table>
""")


#Шаблон спецификации страницы для удаленных таблиц
spec_page_del = Template("""
<h2><b>ТАБЛИЦА УДАЛЕНА</b> - Спецификация таблицы - {{ table_schema }}.{{ table_name }} - <b>ТАБЛИЦА УДАЛЕНА</b></h2>
<table>
<tr><th><b>Наименование поля</b></th><th><b>Тип данных</b></th><th><b>Nullable</b></th><th><b>Default</b></th><th><b>Описание поля</b></th></tr>
{% for col in columns %}
<tr><td>{{ col[0] }}</td><td>{{ col[1] }}({{ col[2] }})</td><td>{{ col[3] }}</td><td>{{ col[4] }}</td><td>{{ col[6] if col[6] is not none else col[7]}} {{ col[5] }}</td></tr>
{% endfor %}
</table>
<h2><b>Индексы</b></h2>
<table>
<tr><th><b>Наименование индекса</b></th><th><b>Состав полей</b></th></tr>
{% for index in indexes %}
<tr><td>{{ index[0] }}</td><td>{{ index[1] }}</td></tr>
{% endfor %}
</table>
""")


#Шаблон страницы для схемы
schema_page = Template("""
<h2>Перечень таблиц схемы - {{ table_schema }}</h2>
<ac:structured-macro ac:name="children" ac:schema-version="2" ac:macro-id="случайный-uuid">
  <ac:parameter ac:name="sort">title</ac:parameter>
  <ac:parameter ac:name="reverse">false</ac:parameter>
</ac:structured-macro>
""")

