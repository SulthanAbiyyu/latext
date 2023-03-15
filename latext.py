import os
import tiktoken
import openai
from dotenv import load_dotenv

load_dotenv(".env")
openai.api_key = os.getenv("OPENAI_KEY")


class Latext:
    def __init__(self, model: str = "gpt-3.5-turbo", currency: str = "idr"):
        self.model = model
        self.currency = currency
        self.response = None
        self.past_responses = []

    def __call__(self, text: str, verbose=True):
        if verbose:
            print(
                f"Estimated cost: {self.estimate_cost(text):.2f} {self.currency.upper()}")
            print(f"Estimated tokens: {self.estimated_tokens}")

        if self.response is not None:
            self.past_responses.append(self.response)
            self.response = None

        self.response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": self._latex_prompt(text)
                }
            ],
            temperature=0.2,
            max_tokens=100,
            top_p=1,
        )

        if verbose:
            print(
                f"Actual cost: {self.get_actual_cost():.2f} {self.currency.upper()}")
            print(f"Actual tokens: {self.get_actual_tokens()}")
        return self.response

    def _latex_prompt(self, text):
        QUESTION_TEMPLATE = f"convert the following text to latex: {text}"
        return PREFIX_TEMPLATE + "\n" + QUESTION_TEMPLATE

    def _num_tokens_from_string(self, string: str, encoding_name: str = "cl100k_base") -> int:
        """Returns the number of tokens in a text string."""
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def estimate_cost(self, text: str) -> int:
        self.estimated_tokens = self._num_tokens_from_string(
            self._latex_prompt(text))

        if self.model == "gpt-3.5-turbo":
            estimate_price = self.estimated_tokens / 1000 * 0.002
        else:
            raise NotImplementedError(
                "Only gpt-3.5-turbo is currently supported.")

        if self.currency == "idr":
            return estimate_price * 15490.10
        elif self.currency == "usd":
            return estimate_price
        else:
            raise NotImplementedError("Only USD and IDR are supported.")

    def get_answer(self):
        resp = self.response["choices"][0]["message"]["content"]
        try:
            resp = resp.replace("\n", "")
        except:
            pass
        try:
            resp = resp.replace("$", "")
        except:
            pass
        return resp

    def get_actual_tokens(self):
        return self.response["usage"]["total_tokens"]

    def get_actual_cost(self):
        if self.currency == "idr":
            return self.get_actual_tokens() / 1000 * 0.002 * 15490.10
        elif self.currency == "usd":
            return self.get_actual_tokens() / 1000 * 0.002
        else:
            raise NotImplementedError("Only USD and IDR are supported.")


PREFIX_TEMPLATE = r"""
You are a helpful assistant to a math teacher. You are given a math equation in text form and you need to convert it to latex. You don't need to calculate it. Here is an example:

Example 1:
text: square root of 2 + 5 ^ 2
latex: \sqrt(2) + 5^{2}

Example 2:
text: 1/2 + 1/3
latex: \frac{1}{2} + \frac{1}{3}

Example 3:
text: A dot B is equal to
30 36 42
66 81 96
102 126 150
latex: A \cdot B = \begin{bmatrix} 30 & 36 & 42 \\ 66 & 81 & 96 \\ 102 & 126 & 150 \end{bmatrix}

Example 4:
text: A is element of B
latex: A \in B

You only need to answer the latex code with given format:
insert latex code here
"""
