import logging
import json

try:
    import requests
except ImportError as ex:
    print("Please Install requests")
    raise ImportError(ex)


class DiscordHandler(logging.Handler):
    """
    A handler class which writes logging records, appropriately formatted,
    to a Discord Server using webhooks.
    """

    def __init__(self, webhook_url, agent):
        logging.Handler.__init__(self)

        if webhook_url is None:
            raise ValueError("webhook_url parameter must be given!")

        if agent is None:
            raise ValueError("agent parameter must be given!")

        self._url = webhook_url
        self._agent = agent
        self._header = self.create_header()
        self._name = ""

    def create_header(self):
        return {
            'User-Agent': self._agent,
            "Content-Type": "application/json"
        }

    def write_to_discord(self, message):
        content = json.dumps({"content": message})
        request = requests.post(self._url,
                                headers=self._header,
                                data=content)

        if request.ok == False:
            raise request.Exception("Request not successful")

    def emit(self, record):
        try:
            print(record)
            msg = self.format(record)
            self.write_to_discord("```%s```" % msg)
        except Exception:
            self.handleError(record)


def test():
    url = ""
    agent = ""

    level = logging.DEBUG
    log_format = logging.Formatter(
        "[%(filename)s]{%(funcName)s L %(lineno)d} --- %(message)s"
    )

    logger = logging.getLogger('spam_application')
    logger.setLevel(level)
    file_handler = DiscordHandler(url, agent)
    file_handler.setFormatter(log_format)
    file_handler.set_name("file")
    file_handler.setLevel(level)
    logger.addHandler(file_handler)

    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(log_format)
    streamHandler.set_name("strema")
    streamHandler.setLevel(level)
    logger.addHandler(streamHandler)

    logger.info("testing info")


if __name__ == "__main__":
    test()
