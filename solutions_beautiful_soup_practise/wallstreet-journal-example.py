from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)
app.debug = True



@app.route('/')
def hello_world():
    return '<h1>Hello World!</h1>'


# This route is a good example
@app.route('/user/<name>')
def hello_user(name):
   return '<h1>Hello {0}</h1>'.format(name)



@app.route('/form',methods= ['POST','GET'])
def enter_data():
    s = """<!DOCTYPE html>
<html>
<body>



<form action="http://localhost:5000/result" method="GET">
  URL:<br>
  <input type="text" name="url" value="https://www.wsj.com/">
  <br>
  <input type="submit" value="Submit">
</form> 



</body>
</html>""" 
# Note that by default https://www.wsj.com/ would be entered in the input field
    return s



@app.route('/result',methods = ['POST', 'GET'])
def res():
    if request.method == 'GET':
        result = request.args
        url = result.get('url')
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        headline_dict =[]
        for headline in soup.find_all("a", {'class':'wsj-headline-link'})[0:4]:
            headline_dict.append(headline.string)
        return render_template("wallstreet-journal-headlines.html",headlines=headline_dict)


if __name__ == '__main__':
    app.run()


