
from pymongo.mongo_client import MongoClient
from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index2.html")


uri = "mongodb+srv://hackuta:rpe5xx3YOUWLXFOc@cluster-01.65uvf4f.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


if __name__ == "__main__":
    app.run()
