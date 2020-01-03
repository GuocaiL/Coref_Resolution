# _*_coding:utf-8_*_
# from __future__ import absolute_import
from flask import request, Flask
from word_check import *
app = Flask(__name__)
@app.route("/",methods=['GET', 'POST'])
def coref_resolution():
    if request.method == 'POST':
        text = request.form.get('text')
        zero_coref = bool(request.form.get('zero_coref'))

        try:
            result, _, _= coref_no_zero(text)
            if zero_coref:
                result = coref_only_zero(result)
            return {
                'code': 0,
                'text': result
                # 'keywords': textrank.textrank(text)
            }
        except:
            return {'code':-1}

if __name__ == "__main__":
    app.run(host='172.27.128.90', port=9098)
