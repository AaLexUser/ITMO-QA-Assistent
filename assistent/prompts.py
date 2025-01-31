CHOOSE_ANSWER = """
Return the number corresponding to the correct answer based on the query and the information provided.

User query.
<query>
{query}
</query>

<information>
{information}
</information>
"""

IS_OPTIONS = """
Are there answer options in the query?
<query>
{query}
</query>
Examples:
Q: В каком году Университет ИТМО был включён в число Национальных исследовательских университетов России?\n1. 2007\n2. 2009\n3. 2011\n4. 2015
A: yes

Q: В каком рейтинге (по состоянию на 2021 год) ИТМО впервые вошёл в топ-400 мировых университетов?\n1. ARWU (Shanghai Ranking)\n2. Times Higher Education (THE) World University Rankings\n3. QS World University Rankings\n4. U.S. News & World Report Best Global Universities
A: yes

Q: В каком городе находится главный кампус Университета ИТМО?
A: no

Q: Существует ли образовательная программа Искусственный интеллект в ИТМО?
A: no
"""