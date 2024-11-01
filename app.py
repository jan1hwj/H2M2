from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import os
from model import runModels_langChain

load_dotenv()

app =Flask(__name__, template_folder = 'templates', static_folder='static',static_url_path='/')

@app.route('/')
def index():
    return render_template('about.html', active='index')

# @app.route('/milestone1')
# def interaction_1():
#     return redirect("https://github.com/jan1hwj/H2M1")
@app.route('/milestone1')
def interaction_1():
    return render_template('milestone1.html', active='interaction_1')

@app.route('/milestone2', methods=['GET','POST'])
def interaction_2():

    if request.method == 'POST':
        
        f = request.files["imgFile"]
        file_name = secure_filename(f.filename)
        cwd = os.getcwd()
        upld_path = cwd+'/static/imgs/'+file_name
        f.save(upld_path)
        img_path = 'imgs/'+file_name
        # generated_img_path = 'imgs/' + os.path.basename(generated_img_path)

        selected_style = request.form.get('style')
        (caption, story, generated_img_path) = runModels_langChain(upld_path, selected_style)

        return render_template('milestone2.html', active='interaction_2', 
                               imgPath=img_path, story=story, caption=caption, generated_img_path=generated_img_path)  

    else:
        return render_template('milestone2.html', active='interaction_2')


if __name__ == '__main__':
    app.run(host='0.0.0.0')