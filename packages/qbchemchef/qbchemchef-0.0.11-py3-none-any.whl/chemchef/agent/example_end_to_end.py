import logging

from chemchef.agent import Agent, STANDARD_TOOLS, STANDARD_EXAMPLES

logging.basicConfig(level=logging.INFO)


def run(question: str) -> str:
    agent = Agent(tools=STANDARD_TOOLS, assistant_message_examples=STANDARD_EXAMPLES)
    return agent.run(question)


def main() -> None:
    run("What is Carlos Alcaraz's current ranking in the ATP rankings?")
    run("What are the top news headlines in the UK today?")
    run("What is the magnetic susceptibility of sodium chloride?")
    run("What are some cheaper alternatives to Alpro soy milk?")
    run("Is alcohol an approved ingredient in skincare products in the US?")


if __name__ == '__main__':
    main()
