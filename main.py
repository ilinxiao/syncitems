from sanic import Sanic
from sanic.response import json
from tortoise import Tortoise, run_async

from models import JobStatus, Choice
from choices_view import bp

app = Sanic("sync_items")
app.blueprint(bp)


@app.route("/")
async def index(request):
    ch = Choice(
        name="linxiao",
        status=JobStatus.Leave
    )
    await ch.save()
    return json({"message": "前后端可选项同步测试。"})


async def init():
    # Here we connect to a SQLite DB file.
    # also specify the app name of "models"
    # which contain models from "app.models"
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()


if __name__ == "__main__":
    run_async(init())
    app.run(host="0.0.0.0", prot=8000, auto_reload=True)
