from flask import Blueprint, render_template

import alert.lib.script as graph_script

import random

from alert.forms import EditGrammarForm

application = Blueprint("user", __name__)


@application.route("/", methods=["GET", "POST"])
def home():
    form = EditGrammarForm()
    if form.validate_on_submit():
        filename = random.randint(1, 10000000)
        graph_script.graph_of_grammar(form.grammar_editor.data, filename=str(filename))
        return render_template(
            "application/home.html", form=form, filename=str(filename)
        )

    return render_template("application/home.html", form=form, filename='frog')


# @application.route("/gen_graph", methods=['POST'])
# def gen_graph():
#     graph_script.graph_of_grammar(request.form)


@application.route("/health")
def health():
    return {"status": "healthy"}, 200
