import logging

from chemchef.agent import Agent

logging.basicConfig(level=logging.INFO)


def run(question: str) -> str:
    agent = Agent.create_with_standard_tools()
    return agent.run(question)


def main() -> None:
    run("What is Carlos Alcaraz's current ranking in the ATP rankings?")
    run("What are the top news headlines in the UK today?")
    run("What is the magnetic susceptibility of sodium chloride?")
    run("What are some cheaper alternatives to Alpro soy milk?")
    run("Is alcohol an approved ingredient in skincare products in the US?")


if __name__ == '__main__':
    main()
