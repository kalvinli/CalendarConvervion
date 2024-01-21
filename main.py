from flask import Flask, request, render_template, url_for, redirect
from base_class.base_func import batch_convert_date_func

app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config['JSON_AS_ASCII'] = False


## 前端用户界面，通过前端SDK操作
@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

# @app.route('/setup.png')
# def favicon():
#     return redirect(url_for('static', filename='img/setup.png'))

## 自动化流程接口，通过后端SDK操作
@app.route('/batch_convert_date', methods=['POST'])
def batch_convert_date():

  data = request.get_data().decode()
  # print(data)

  try:
    result = batch_convert_date_func(data)
    code = 200

  except Exception as e:
    result = '日期转换失败，请检查后重试'
    code = -1

  return {"code": code, "msg": result}


app.run(host='0.0.0.0', port=3300, debug=True, use_reloader=True)
