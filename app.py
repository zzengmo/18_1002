from flask import Flask, render_template, request, send_file
from scrapper import search_incruit, search_gamejob
from file import save_to_csv

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search")
def search():
    keyword = request.args.get("keyword")

    incruit_jobs = search_incruit(keyword)
    gamejob_jobs = search_gamejob(keyword)

    jobs = incruit_jobs + gamejob_jobs

    return render_template(
        "search.html",
        keyword=keyword,
        jobs=enumerate(jobs)
    )


@app.route("/file")
def file():
    keyword = request.args.get("keyword")

    incruit_jobs = search_incruit(keyword)
    gamejob_jobs = search_gamejob(keyword)

    jobs = incruit_jobs + gamejob_jobs

    save_to_csv(jobs)

    return send_file("downloads.csv", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)