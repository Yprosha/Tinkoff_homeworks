from flask import Flask, render_template, request
from search import score, retrieve, build_index, something
from time import time

app = Flask(__name__, template_folder='.')
build_index()


@app.route('/', methods=['GET'])
def index():
    start_time = time()
    query = request.args.get('query')
    if query is None:
        query = ''
    documents = retrieve(query)
    wv = something(documents)
    documents = sorted(documents, key=lambda doc: -score(query, doc, wv))
    results = [doc.format(query)+['%.2f' % score(query, doc)] for doc in documents] 
    return render_template(
        'index.html',
        time="%.2f" % (time()-start_time),
        query=query,
        search_engine_name='Yandex',
        results=results
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
