from flask import Flask, abort, render_template, request, jsonify, session, redirect
from utils import authorized, not_authorized, authorize
#---------
import db
import xlrd
import pandas as pd
import numpy as np
import openpyxl
#---------
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import csv
#---------
from random import*


index_string  ='!'

app = Flask("SimpleTaskTracker")
template_dir = 'templates'


@app.route('/', methods=["GET"])
@not_authorized
def login():
    return render_template('login.html')
    
@app.route('/registration', methods=["GET"])
@not_authorized
def registration():
    return  render_template('reg.html')

@app.route('/add_books', methods=['GET'])
@authorized
def add():
    return render_template('add_books.html')

@app.route('/list_of_books', methods=['GET'])
@authorized
def list():
    return render_template('list_of_books.html')

@app.route('/extradite_books', methods=["GET"])
@authorized
def extradite_books():
    return render_template('extradite_books.html')

@app.route('/menu', methods=["GET"])
@authorized
def menu():
    return render_template('menu.html')

@app.route('/logout', methods=["GET"])
@authorized
def logout():
    session.clear()
    return redirect('/')

@app.route('/api/table_search', methods=["POST"])
@authorized
def api_table():
    df = pd.read_excel('table.xlsx')#чтение из файла
    df.loc[df['Характер док-та об образовании'] == 'Оригинал', 'Характер док-та об образовании'] = 1#Сравнение Оригинал или Копия
    df.loc[df['Характер док-та об образовании'] == 'Копия', 'Характер док-та об образовании'] = 0
    df.sort_values(['Характер док-та об образовании','Сумма баллов'], ascending = [False,False], inplace = True)
    ind = len(df.index)

    #df_2.insert('index', index=df_2.index)
    #df_2.reset_index(inplace=True)
    df.loc[df['Характер док-та об образовании'] == 1, 'Характер док-та об образовании'] = 'Оригинал'#Сравнение Оригинал или Копия
    df.loc[df['Характер док-та об образовании'] == 0, 'Характер док-та об образовании'] = 'Копия'
    writer = pd.ExcelWriter('output.xlsx', engine='openpyxl')#Создание новой таблицы
    df.index = range(1,ind+1)
    
    df.to_excel(writer, 'Results')#Запись в файл
    writer.save()#Сохранение


    name = request.form.get('name', None)
    second_name = request.form.get('second_name', None)
    third_name = request.form.get('third_name', None)
    col_vo = request.form.get('col_vo', None)
    all_summ = 0
    all_mat = 0
    all_inf = 0
    all_rus = 0
    for i in range(0,len(df)):
        new_mat = str(df.iloc[i,8])
        new_inf = str(df.iloc[i,7])
        new_rus = str(df.iloc[i,9])
        if new_mat[-1] == '*':
            df.iloc[i,8] = new_mat[:-1]
        elif new_inf[-1] == '*':
            df.iloc[i,7] = new_inf[:-1]
        elif new_rus[-1] == '*':
            df.iloc[i,9] = new_rus[:-1]

    for i in range(0,len(df)):
        all_summ = int(df.iloc[i,6]) + all_summ
        all_mat = int(df.iloc[i,8]) + all_mat
        all_inf = int(df.iloc[i,7]) + all_inf
        all_rus = int(df.iloc[i,9]) + all_rus
    sr_summ = all_summ/len(df) 
    sr_mat = all_mat/len(df) 
    sr_inf = all_inf/len(df) 
    sr_rus = all_rus/len(df) 

    df_4 = df.loc[df['ФИО'] == (name+' '+second_name+' '+third_name)]
    #вот здесь описание массива
    #summ = df_4[df_4['Сумма баллов']]
    #for row in df_4.rows:
    #    summ = row['Сумма баллов']
    print(df_4)
    summ = int(df_4.iloc[0,6])
    mat = int(df_4.iloc[0,8])
    rus = int(df_4.iloc[0,9])
    inf = int(df_4.iloc[0,7])
    print(summ, mat, inf, rus)
    df_4 = df_4.index
    
    #print(summ)
    df_4  = str(df_4)
    start = 0
    end = 0
    end_string = ''
    for i in range(0,len(df_4)):
        if df_4[i] == '[':
            start = i
        if df_4[i] == ']':
            end = i
    #df_4 =

    print(df_4)
    print(start, end)
    for j in range(start+1, end):
        end_string = end_string + df_4[j]
    #------elipse diagramm-----------
    end_index = int(end_string)
    col_vo = int(col_vo)
    count_org = 0
    count_cop = 0
    for j in range(0,end_index+1):
        org = str(df.iloc[j,3])
        if org == 'Оригинал':
            count_org += 1
    print('Оригиналов : ',count_org)
    for i in range(0,end_index+1):
        cop = str(df.iloc[i,3])
        if (cop == 'Копия') and (count_cop<(col_vo-count_org)):
            count_cop += 1
    print('Копий : ',count_cop)
    procent = 0
    good = 0
    prom_procent = 0 
    if end_index<=col_vo:
        procent = 100
    elif end_index>col_vo:
        for i in range(1,count_cop+1):
            prom = (i*100)/count_cop
            prom_procent = prom+prom_procent
            good +=1
        procent = prom_procent/good
    print(procent)
    data_names_pie = ['Вероятность попадания','Не попадание']
    data_values_pie = [int(procent), 100-int(procent)]

    dpi_pie = 80
    fig_pie = plt.figure(dpi = dpi_pie, figsize = (512 / dpi_pie, 384 / dpi_pie) )
    mpl.rcParams.update({'font.size': 9})

    plt.title('Распределение кафе по городам России (%)')

    xs_pie = range(len(data_names_pie))

    plt.pie( 
        data_values_pie, autopct='%.1f', radius = 1.1,
        explode = [0.15] + [0 for _ in range(len(data_names_pie) - 1)] )
    plt.legend(
        bbox_to_anchor = (-0.16, 0.45, 0.25, 0.25),
        loc = 'lower left', labels = data_names_pie )
    fig_pie.savefig('pie.png')
    #------diagramm------------------
    
    data_names = ['Summa Ballov', 'Math', 'Rus', 'Inf']
    data_values = [summ, mat, rus, inf]

    dpi = 80
    fig = plt.figure(dpi = dpi, figsize = (1024 / dpi, 384 / dpi) )
    mpl.rcParams.update({'font.size': 10})

    plt.title('Table')
    proxod_bal = 240
    ax = plt.axes()
    ax.yaxis.grid(True, zorder = 1)

    xs = range(len(data_names))

    plt.bar([x + 0.05 for x in xs], [sr_summ,sr_mat,sr_rus,sr_inf],
            width = 0.2, color = 'red', alpha = 0.7, label = 'srednee',
            zorder = 2)
    plt.bar([x + 0.3 for x in xs], data_values,
            width = 0.2, color = 'green', alpha = 0.7, label = 'yours',
            zorder = 2)
    plt.xticks(xs, data_names)

    fig.autofmt_xdate(rotation = 25)

    plt.legend(loc='upper right')
    plt.show()
    fig.savefig('bars.png')
    return jsonify({'status': 'error', 'message':'Ваше место в списке :'+end_string})    

@app.route('/api/login', methods=["POST"])
@not_authorized
def api_login():
    login = request.form.get('login', None)
    password = request.form.get('password', None)
    if login is None or password is None:
        return jsonify({'status': 'error', 'message': 'Неверные данные для входа'})
    user = authorize(login, password)
    if user.is_authorized():
        session['user_login'] = login
        return jsonify({'status': 'ok'})
    return jsonify({'status': 'error', 'message': 'Неверные данные для входа'})

@app.route('/api/add_user', methods=["POST"])
@not_authorized
def api_add_user():

    login = request.form.get('login', None)
    name = request.form.get('name', None)
    surname = request.form.get('surname', None)
    third_name = request.form.get('third_name', None)
    password = request.form.get('password', None)
    confirm_password = request.form.get('confirm_password', None)
    profile = request.form.get('profile', None)
    if password != confirm_password:
        return jsonify({'status': 'error', 'message': 'Пароли не совпадают'})
    if login is None or name is None or surname is None or third_name is None or password is None or confirm_password is None or profile is None:
        return jsonify({'status': 'error', 'message': 'Некорректный запрос'})
    user_id = db.add_user(login, name, surname, third_name, password, confirm_password, profile)
    return jsonify({'status': 'ok', 'user_id': user_id})

@app.route('/api/books', methods=["GET"])
@authorized
def api_books():
    login = session['user_login']
    return jsonify({"books": db.get_books(login)})

@app.route('/api/users', methods=["GET"])
@authorized
def api_users():
    login = request.form.get('login', None)
    name = request.form.get('name', None)
    surname = request.form.get('surname', None)
    third_name = request.form.get('third_name', None)
    password = request.form.get('password', None)
    confirm_password = request.form.get('confirm_password', None)
    profile = request.form.get('profile', None)
    return jsonify({"users": db.get_users(login, name, surname, third_name, password, confirm_password, profile)})

@app.route('/api/add_book', methods=["POST"])
@authorized
def api_add_book():
    chet=0
    login = session['user_login']
    name = request.form.get('name', None)
    author = request.form.get('author', None)
    clas = request.form.get('clas', None)
    numIzd = request.form.get('numIzd', None)
    nameIzd = request.form.get('nameIzd', None)
    if name is None or author is None or clas is None or numIzd is None or nameIzd is None :
        return jsonify({'status': 'error', 'message': 'Некорректный запрос'})
    # task_id = add_task(login, text)
    book_id = db.add_book(login, name, author, clas, numIzd, nameIzd)
    return jsonify({'status': 'ok', 'book_id': book_id})

@app.route('/table_tool', methods=['GET'])
@authorized
def table_tool():
    print("table_tool start ....")
    return render_template('table_tool.html')

@app.route('/table_results', methods=['GET'])
@authorized
def table_results():

    return render_template('table_results.html')


if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(port=randint(8001,8501))
