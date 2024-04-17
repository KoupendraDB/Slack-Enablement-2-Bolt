import os
from slack_bolt import App
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

from services.mongo.client import MongoManager
mongo_client = MongoManager().mongo_client

bot_info = app.client.auth_test()

from listeners import register_listeners
register_listeners(app)

if __name__ == "__main__":
    from slack_bolt.adapter.socket_mode import SocketModeHandler
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()