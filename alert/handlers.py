from flask import flash, render_template, session
import pyparsing

import alert.lib.script as graph_script

from alert.forms import EditGrammarForm


def home():
    session.pop("_flashes", None)
    form = EditGrammarForm()
    labelled_nodes = []
    numbered_edges = []

    if form.validate_on_submit():
        try:
            nodes, edges = graph_script.generate_graph(form.grammar_editor.data)
            numbered_nodes = {item: index for index, item in enumerate(nodes)}
            numbered_edges = [(numbered_nodes[s], numbered_nodes[v]) for s, v in edges]
            labelled_nodes = [(node, label) for label, node in numbered_nodes.items()]
        except pyparsing.exceptions.ParseException as e:
            flash(["Input error:", e.msg])
        except Exception as e:
            flash(["Unknown error", str(e)])

    return render_template(
        "pages/home.html", form=form, nodes=labelled_nodes, edges=numbered_edges
    )


def health():
    return {"status": "healthy"}, 200
