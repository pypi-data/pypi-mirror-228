import random


class question_asker:
    questions = []
    answers = []

    def __init__(self, *args):
        """
        The function takes in a list of questions and appends them to the questions list
        """
        for questionn in args:
            self.questions.append(questionn)

    def ask(self, index: int = 0, keep: bool = False):
        """
        The function asks a question, and then appends the answer to the answers list

        :param index: The index of the question you want to ask, defaults to 0
        :type index: int (optional)
        :param keep: If you want to keep the question in the list of questions, set this to True, defaults to False
        :type keep: bool (optional)
        :return: A dictionary with the answer and the question.
        """
        answer = input(self.questions[index])
        self.answers.append({"answer": answer, "question": self.questions[index]})
        if not keep:
            self.questions.pop(index)
        return {"answer": answer, "question": self.questions[index]}

    def append(self, *args):
        """
        It takes a list of questions and appends them to the end of the list of questions
        """
        for questionn in args:
            self.questions.append(questionn)

    def remove(self, item: str):
        """
        It removes the item from the list.

        :param item: str
        :type item: str
        """
        self.questions.remove(item)

    def ask_all(self):
        """
        It takes a list of questions, asks them one by one, and returns a list of answers
        :return: A list of dictionaries.
        """
        answers = []
        for questionn in self.questions:
            answer = input(questionn)
            answers.append({"question": questionn, "answer": answer})
            self.answers.append({"question": questionn, "answer": answer})
        return answers

    def get_answer(self, index: int):
        """
        It returns the answer at the given index

        :param index: The index of the answer you want to get
        :type index: int
        :return: The answer to the question at the given index.
        """
        return self.answers[index]

    def get_all_answers(self):
        """
        It returns all the answers for a question.
        :return: The answers to the question.
        """
        return self.answers

    def ask_random(self, append: bool = False):
        """
        It takes a boolean argument, and if it's True, it appends the user's answer to the answers list

        :param append: If True, the answer will be appended to the answers list, defaults to False
        :type append: bool (optional)
        :return: A dictionary with the question and answer.
        """
        question = random.choice(self.questions)
        answer = input(question)
        if append:
            self.answers.append(answer)
        return {"question": question, "answer": answer}
