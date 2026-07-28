import sys

from core.agent import Agent

agent = Agent()


def main():

    if len(sys.argv) < 2:
        print("Usage:")
        print("  ai <command>")
        print("Examples:")
        print("  ai hi")
        print("  ai scan my network")
        print("  ai check my ip")
        print("  ai create flask app")
        return

    prompt = " ".join(sys.argv[1:])

    result = agent.chat(prompt)

    if result:
        print(result)


if __name__ == "__main__":
    main()
