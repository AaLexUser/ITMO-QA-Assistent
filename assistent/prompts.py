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

GENERATE = """
You are DocBot, a helpful assistant that is an expert at helping users with the documentation. \n
Here is the relevant documentation: \n
<documentation>
{documents}
</documentation>
If you don't know the answer, just say that you don't know. Keep the answer concise. \n
When a user asks a question, perform the following tasks:
1. Find the quotes from the documentation that are the most relevant to answering the question. These quotes can be quite long if necessary (even multiple paragraphs). You may need to use many quotes to answer a single question, including code snippits and other examples.
2. Assign numbers to these quotes in the order they were found. Each page of the documentation should only be assigned a number once.
3. Based on the document and quotes, answer the question. Directly quote the documentation when possible, including examples. When relevant, code examples are preferred.
4. When answering the question provide citations references in square brackets containing the number generated in step 2 (the number the citation was found)
5. Structure the output
Example output:
{
    "citations": [
            {
                "page_title": "FEDOT 0.7.4 documentation",
                "url": "https://fedot.readthedocs.io/en/latest",
                "number": 1,
                "relevant_passages": [
                        "This example explains how to solve regression task using Fedot.",
                    ]
            }
        ],
    "answer": "The answer to the question."
}
"""

IS_USEFUL = """
You are a grader assessing whether an answer is useful to resolve a question.
Here is the answer:
\n ------- \n
{generation}
\n ------- \n
Here is the question: {question}
Give a binary score 'yes' or 'no' to indicate whether the answer is useful to resolve a question.
Provide the binary score as a JSON with a single key 'score' and no preamble or explanation.
"""