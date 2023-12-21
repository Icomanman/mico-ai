
import random
import gradio as gr


def random_response(message, history):
    return random.choice(["Yes", "No"])


def main():
    print("> This is Gradio.")
    demo = gr.ChatInterface(random_response)
    demo.launch()
    return


if __name__ == '__main__':
    main()