from flask import Flask ,request ,render_template ,url_for ,redirect 
from base_class .base_func import batch_split_rows_func 
app =Flask (__name__ ,static_folder ="static",static_url_path ="/static")
app .config ['JSON_AS_ASCII']=False 
@app .route ('/',methods =['GET'])
def index ():
  return render_template ('index.html')
@app .route ('/batch_split_rows',methods =['POST'])
def batch_split_rows ():
  O000OOO00OOOO0OO0 =request .get_data ().decode ()
  try :
    OOO0OO000O0O000O0 =batch_split_rows_func (O000OOO00OOOO0OO0 )
    OO000OOOOO0OOO0O0 =200 
  except Exception as OOOOO0O0O0O00O0O0 :
    OOO0OO000O0O000O0 ='拆分数据失败，请检查后重试'
    OO000OOOOO0OOO0O0 =-1 
  return {"code":OO000OOOOO0OOO0O0 ,"msg":OOO0OO000O0O000O0 }
app .run (host ='0.0.0.0',port =3300 ,debug =True ,use_reloader =True )
