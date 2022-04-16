from invoke import task
from dotenv import load_dotenv

load_dotenv()

@task
def debug(ctx):
    from liveline.app import app
    
    app.run('0.0.0.0', 8000, debug=True)

@task
def sass(ctx):
    ctx.run(
        "sass ./liveline/static/styles/style.scss ./liveline/static/styles/style.css --watch"
    )
