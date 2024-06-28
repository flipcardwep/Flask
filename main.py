import sqlite3
from sqlite3 import Error
from werkzeug.utils import secure_filename
import json,os
from passlib.hash import pbkdf2_sha256
from flask import  *
from flask_session import Session
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False  # True to make sessions persistent
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "./tmp" 
Session(app)
app.secret_key = 'BAD_SECRET_KEY'
print("running...")
j=json.load(open('product/product.json'))

def dbsine(email,username,password,location,product):
    path='user/sine.db'
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
        connection.execute("INSERT INTO products (email,username,password,location,product) VALUES ('"+email+"', '"+username+"','"+password+"', '"+location+"','"+product+"');")
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")
        return "false"
    connection.close()
def dbset(path,obj):
    connection = None
    f=""
    v=""
    for a,b in obj.items():
        if v=="":
            f=a
            v="'"+str(b)+"'"
        else: 
            try:
                b=int(b)
                v=v+"," +str(b)
                f=f+ "," +a
            except:                             
                v=v+",'" +str(b)+"'"
                f=f+ "," +a
                                         

    print(v)        
    print(f)
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful "+ path)
        connection.execute("INSERT INTO products ("+f+") VALUES ("+v+");")
        
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")
        return False
    connection.close()
def dbsearch(path,search,colume):  
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful"+path)
        aa=connection.execute("SELECT "+colume+" FROM products "+search+";")
        b=aa.fetchall()
        return b
    except Error as e:
        print(f"The error '{e}' occurred")
def dbproduct(name,fullprice,sellprice,noimg,imgname):
    path='Audiobooks/flipcard/static/productimg/txt.db'
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
        connection.execute("INSERT INTO products (name,fullprice,sellprice,noimg,imgname) VALUES ('"+name+"', '"+fullprice+"','"+sellprice+"', '"+noimg+"'"+imgname+"');")
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")
        return "false"
    connection.close()
     
@app.post('/login')
def home():    
    print(request.json)
    passw=pbkdf2_sha256.hash(request.json['password'])
    u=request.json['username']
    e=request.json['email']
    l=request.json['location']
    if (u =="" or e =="" or passw ==""):
        return {"error": "Please fill all the fields"}
    a=dbsine(e,u,passw,l,"")
    if (a == "false"):
        return jsonify({"error": "email already found"})
    session["name"] =str(u)
    print(" 1")
    return  jsonify({"url": "/"}) 

@app.post('/sell')  
def sell():   
    c={}
    #if not session.get("name"):
    #    return jsonify({"url": "/login"})
    #user = session.get('name')
    try: 
       req=json.loads(request.form.get('formdata'))
       print(req)
    except Error as e:
        print(e)
        return jsonify({"error": "please fill all input"}),400
    detail = {}
    a=["id","name","type","price","title","discription"]
    for b in a:
        try:
           c[b]=req[b]
        except:
            return jsonify({"error": "please fill "+ b}),400
    try:   
       detail= req["o_detail"]
       for d in j["detail"][req["url"]]:        
            try:
                c[d]=detail[d]
                detail.pop(d)
            except Error as e:
                print(e)
                return jsonify({"error": "please fill "+ d + " of details"}),400
    except Error as e:
        print(e)
        return jsonify({"error": "please select  product"}) ,400
    try: 
        c["o_detail"]=json.dumps(detail)
        c["n_sell"]=0
        c["reviews"]=0

        try: 
           file = request.files
           if not file:
              return jsonify({'error': 'No file URL provided'}), 400
           if "a" not in file:
               return jsonify({"error": "please select first image"}),400
           c["image"]=str(file.keys()).replace("[","").replace("]","").replace("dict_keys(","").replace(")","").replace("'","")
        except Error:
            print(Error)
            return jsonify({"error": "plese fill image"}),400
        g=dbset("product/"+str(j["product"][req["url"]])+"/product.db",c)
        if g==False:
            return jsonify({"erroe": "id already found"}),400

        for i,v in file.items():
           print(v)
           response = v
           try:
               name = secure_filename(v.filename)
               typ= name.split(".")[-1]
               fn="static/"+ str(j["product"][req["url"]])
               if not os.path.exists(fn):
                   os.makedirs(fn)
               response.save(fn + "/" +str(req["id"]) + i + "."+typ)
           except Error as e:
               print(e)
               return jsonify({"error": "anything  wrong"}) ,400
    except Error as e:
        print(e)
        return jsonify({"error": "anything  wrong"}),400
    return jsonify({"url": "/"})

@app.post('/check')
def file_check():
    #if not session.get("name"):
    #    return jsonify({"url": "/login"})
    returndata = {}
    a=request.json["product"]
    print(a)
    if a in j["detail"]:
        for b in j["detail"][a]:
            returndata[b] = j["de_obj"][b]
        return returndata    
    return "unvaled action"
@app.route("/search")
def search(search): 
    #search=request.json["search"]
    s=search.split("+")
    From=j["product"]
    t=0
    se=""
    result="not fond"
    for k,v in j["product"].items():
        n=0
        m=""
        for a in k.split(" "):
            if a in s:
                n=n+1
                m=a
        if t<n:
            t=n
            se=m     
    if t != 0:
        for a in se.split(" "):
            s.remove(a)
            From=[se]
        result=dbsearch("product/"+j["product"][se]+"/product.db","","id,image,title,price,reviews")
    if s==[]:
        return result
    id=False
    print(From)
    for d in From:
        for i in s:
            id=dbsearch("product/"+j["product"][d]+"/product.db","WHERE id = '"+i+"'","id,image,title,price,reviews")           
            if id!=[]:
               return id 
        print(" ".join(s))    
    
    return result
print(search("laptop+Ashish-shree1")) 
@app.post('/sineup')
def sineup():    
    re=request.json['email']
    rtit=request.json['password']
    if(re =="" or rtit ==""):
        return jsonify({"error": "Please fill all the fields"})
    a=dbsearch("user/sine.db","where email = '"+re+"'","*")
    print(a)
    if (a == []):
        return jsonify({"error": "email not found"})
    print(a[0][2])    
    if(pbkdf2_sha256.verify(rtit,a[0][2])):
        session['name']=str(a[0][1])
        return jsonify({"url": "/"})

    return jsonify({"error": "password not match"})
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')