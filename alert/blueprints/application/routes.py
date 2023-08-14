from flask import Blueprint, render_template

import alert.lib.script as graph_script

import uuid

from alert.forms import EditGrammarForm

application = Blueprint("user", __name__)


@application.route("/", methods=["GET", "POST"])
def home():
    form = EditGrammarForm()
    if form.validate_on_submit():
        filename = uuid.uuid4()
        graph_script.graph_of_grammar(form.grammar_editor.data, filename=str(filename))
        return render_template(
            "application/home.html", form=form, filename=str(filename)
        )

    return render_template("application/home.html", form=form, filename="frog")


@application.route("/health")
def health():
    return {"status": "healthy"}, 200
