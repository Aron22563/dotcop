from dotcop.app.app import App
import logging

logging.basicConfig(
    level=logging.INFO, 
    format="%(levelname)s: %(message)s"
)

def main():
    app = App()
    app.run()
