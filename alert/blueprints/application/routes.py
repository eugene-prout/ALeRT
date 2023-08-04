from flask import Blueprint, render_template

import alert.lib.script as graph_script

from alert.forms import EditGrammarForm

application = Blueprint("user", __name__)


@application.route("/", methods=['GET','POST'])
def home():
    form = EditGrammarForm()
    if form.validate_on_submit():
        graph_script.graph_of_grammar(form.grammar_editor.data)

    return render_template("application/home.html",form=form)


@application.route("/health")
def health():
    return {"status": "healthy"}, 200

