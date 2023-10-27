import pprint
import sys
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5 import uic
# to draw picture using qtgui;
from PyQt5.QtGui import *
import pandas as pd
# to draw figure using matplotlib;
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
# to connect mysql;
# have to do install using 'pip install mysql.connector'
# import mysql.connector
import pymysql
from datetime import datetime

# 한글 폰트 사용을 위해서 세팅
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)


from sklearn.model_selection import train_test_split




# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# step 1; to connect ui files;
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
form_class = uic.loadUiType("dron1.ui")[0]





class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)


        # to set limits on lineedit widget;
        self.edt_presimul.setMaxLength(10)




        # //////////////////////////////////////////////////////////////////////////////////////////////////////////////
        # step 2; to make figure canvas to draw graphs;
        # //////////////////////////////////////////////////////////////////////////////////////////////////////////////

        # to make 1st canvas;
        #
        self.fig_1 = plt.Figure()
        self.canvas_1 = FigureCanvas(self.fig_1)
        self.ax_1 = self.canvas_1.figure.subplots()
        # self.layout is defined at ui;
        self.layout_1.addWidget(self.canvas_1)



        #
        # to make 2nd canvas;
        #
        self.fig_2 = plt.Figure()
        self.canvas_2 = FigureCanvas(self.fig_2)
        self.ax_2 = self.canvas_2.figure.subplots()
        self.layout_2.addWidget(self.canvas_2)




        #
        # to make 3rd canvas;
        #
        # self.canvas_3 = FigureCanvas(self.fig)
        # self.layout_3.addWidget(self.canvas_3)




        # /////////////////////////////////////////////////////////////////////////////////////////////////////////////
        # step 3; to connect widgets with functions;
        # /////////////////////////////////////////////////////////////////////////////////////////////////////////////

        # -------------------------------------------------------------------------------------------------------------
        # step 3-1; to use toolbars to connect functions;
        # -------------------------------------------------------------------------------------------------------------
        # to load excel data file;
        # self.btn_fopen.clicked.connect(self.open_from_file)

        # to open image files;
        self.actionOpen.triggered.connect(self.open_from_file)









        # to make any table and test it;
        self.btn_go.clicked.connect(self.make_some_table)
        # self.btn_go.clicked.connect(self.connect_k3i_api)



        self.btn_draw.clicked.connect(self.draw_graph)

        # to connect mysql database;
        self.btn_conn_db.clicked.connect(self.connect_essetel_mysql)

        # to load mysql database;
        self.btn_load_db.clicked.connect(self.load_file_downloaded_from_essetelMysql)

        # to simulate prelimilary received power;
        self.btn_presimul.clicked.connect(self.presimulate_recvPwr)

        # to draw data above heights;
        self.btn_data_aboveHeight.clicked.connect(self.data_aboveHeight)

        # to clear graph;
        self.btn_ax_clear.clicked.connect(self.clear_ax)






    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # step 4; to make functions;
    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////


    # -----------------------------------------------------------------------------------------------------------------
    # step 4-1; to clear axes;
    # -----------------------------------------------------------------------------------------------------------------
    def clear_ax(self):
        print('clear button pressed;')

        self.ax_1.clear()
        self.ax_2.clear()

        self.canvas_1.draw()
        self.canvas_2.draw()



    # -----------------------------------------------------------------------------------------------------------------
    # step 4-2; to sort table by options;
    # -----------------------------------------------------------------------------------------------------------------
    def sort_tbl_byOptions(self):
        self.edt_presimul.setText('hello,kitty')



    # -----------------------------------------------------------------------------------------------------------------
    # step 4-3; to presimulate received power;
    # -----------------------------------------------------------------------------------------------------------------
    def presimulate_recvPwr(self):
        self.edt_presimul.setText('hello,kitty')

        try:
            # to calculate eirp;
            if self.rbtn_eirp.isChecked():
                self.edt_presimul.setText('hi,kitty')
                eirp = float(self.edt_txpwr.text()) + float(self.edt_txantgain.text()) + float(self.edt_rxantgain.text())
                print(eirp)
                eirp = str(eirp)
                self.edt_presimul.setText(eirp)


            # to calculate passloss;
            elif self.rbtn_passloss.isChecked():

                if self.cmb_freq.currentText() == 'ps-lte':
                    # passloss = 10*float(self.edt_txpwr.text()) + float(self.edt_txantgain.text())
                    freq = 778*float(np.power(10,6))
                    print('freq;', freq)

                    dist = float(self.edt_distance.text())
                    passloss = - ( 20*np.log10(freq) + 20*np.log10(dist) - 147.55 )
                    print(passloss)
                    passloss = str(passloss)
                    self.edt_presimul.setText(passloss)

                elif self.cmb_freq.currentText() == 'wifi-2.4':
                    freq = 2400*float(np.power(10,6))
                    print('freq;', freq)
                    dist = float(self.edt_distance.text())
                    passloss = - ( 20*np.log10(freq) + 20*np.log10(dist) - 147.55 )
                    print(passloss)
                    passloss = str(passloss)
                    self.edt_presimul.setText(passloss)

                elif self.cmb_freq.currentText() == 'wifi-5.7':
                    freq = 5700 * float(np.power(10, 6))
                    print('freq;', freq)
                    dist = float(self.edt_distance.text())
                    passloss = - (20 * np.log10(freq) + 20 * np.log10(dist) - 147.55 )
                    print(passloss)
                    passloss = str(passloss)
                    self.edt_presimul.setText(passloss)

            # to calculate received power;
            elif self.rbtn_recvpwr.isChecked():
                if self.cmb_freq.currentText() == 'ps-lte':
                    # to calculate ant gains;
                    eirp = float(self.edt_txpwr.text()) + float(self.edt_txantgain.text()) + float(
                        self.edt_rxantgain.text())

                    # to calculate passloss;
                    # passloss = 10*float(self.edt_txpwr.text()) + float(self.edt_txantgain.text())
                    freq = 778*float(np.power(10,6))
                    print('freq;', freq)
                    dist = float(self.edt_distance.text())
                    passloss = - ( 20*np.log10(freq) + 20*np.log10(dist) - 147.55 )
                    print(passloss)

                    recvpwr = eirp + passloss
                    recvpwr = str(recvpwr)
                    self.edt_presimul.setText(recvpwr)

                elif self.cmb_freq.currentText() == 'wifi-2.4':
                    # to calculate ant gains;
                    eirp = float(self.edt_txpwr.text()) + float(self.edt_txantgain.text()) + float(
                        self.edt_rxantgain.text())

                    # to calculate passloss;
                    # passloss = 10*float(self.edt_txpwr.text()) + float(self.edt_txantgain.text())
                    freq = 2400*float(np.power(10,6))
                    print('freq;', freq)
                    dist = float(self.edt_distance.text())
                    passloss = - (20*np.log10(freq) + 20*np.log10(dist) - 147.55)
                    print(passloss)

                    recvpwr = eirp + passloss
                    recvpwr = str(recvpwr)
                    self.edt_presimul.setText(recvpwr)

                elif self.cmb_freq.currentText() == 'wifi-5.7':
                    # to calculate ant gains;
                    eirp = float(self.edt_txpwr.text()) + float(self.edt_txantgain.text()) + float(
                        self.edt_rxantgain.text())

                    # to calculate passloss;
                    # passloss = 10*float(self.edt_txpwr.text()) + float(self.edt_txantgain.text())
                    freq = 5700*float(np.power(10,6))
                    print('freq;', freq)
                    dist = float(self.edt_distance.text())
                    passloss = - (20*np.log10(freq) + 20*np.log10(dist) - 147.55)
                    print(passloss)

                    recvpwr = eirp + passloss
                    recvpwr = str(recvpwr)
                    self.edt_presimul.setText(recvpwr)


        except:
            pass
        finally:
            pass



    # -----------------------------------------------------------------------------------------------------------------
    # step 4-4; to connect mysql;
    # -----------------------------------------------------------------------------------------------------------------
    def connect_essetel_mysql(self):
        hostIp = '175.203.23.10'
        # hostIp = '175.203.23.4'
        portNumber = 13321
        userId = 'k3i'
        pw = 'k3i@@4321'
        dbName = 'drone'
        tblName = 'electric_wave_info'


        #
        # to connect mysql;
        #
        conn = pymysql.connect(host=hostIp, port=portNumber, user=userId, password=pw,
                       db=dbName, charset='utf8') # 한글처리 (charset = 'utf8')
        print('mysql db; connected')
        # connDb = pymysql.connect(server='pc-server', database='mydb')
        # conn = pymysql.connect(host='localhost', port=3306, user='root', password='1121',
        #                db='pm_mes_db', charset='utf8') # 한글처리 (charset = 'utf8')





        #
        # to save csv file using pandas;
        #
        sql = 'select * from '
        sql2 = sql + tblName
        df2 = pd.read_sql_query(sql2, conn)


        # sql = 'select * from electric_wave_info'
        # df2 = pd.read_sql_query(sql, conn)


        df2.to_csv(r'essetel_dron_db.csv', index=False)
        print('end time;', str(datetime.now())[10:19])


        #
        # to make wind message;
        #
        replyMesage = QMessageBox.question(self, 'Message', 'Mysql database is connected!',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if replyMesage == QMessageBox.Yes:
            conn.close()
        # else:
        #     conn.close()


        # STEP 5: DB 연결 종료
        # conn.close()





    # -----------------------------------------------------------------------------------------------------------------
    ## step 4-5; to draw graph from mysql;
    # -----------------------------------------------------------------------------------------------------------------
    def load_file_downloaded_from_essetelMysql(self):



        self.df_db = pd.read_csv('./essetel_dron_db.csv')
        print('df-db columns;', self.df_db.columns)
        print('df-db index;', self.df_db.index)



        #
        # to count rows and columns;
        #
        self.tbl_two.setRowCount(len(self.df_db.index))
        print('index count;', len(self.df_db.index))
        self.tbl_two.setColumnCount(len(self.df_db.columns))
        print('column count;', len(self.df_db.columns))



        #
        # # to make columns header label;
        #
        self.tbl_two.setHorizontalHeaderLabels(self.df_db.columns)
        # # self.tbl_two.setHorizontalHeaderLabels(('id','longitude','altitude','value'))


        #
        # to load data to a table;
        #
        for row_index, row in enumerate(self.df_db.index):
            for col_index, column in enumerate(self.df_db.columns):

                value = self.df_db.loc[row][column]
                item = QTableWidgetItem(str(value))

                # item = QTableWidgetItem(value)
                self.tbl_two.setItem(row_index,col_index, item)



        #################################################
        ## to load x,y variables to combobox;
        #################################################
        # to load x-variables to combobox from dataframes;
        self.cmb_x_axis.clear()
        self.cmb_x_axis.addItem('choose a field')
        for field in self.df_db.columns:
            self.cmb_x_axis.addItem(str(field))

        # to load y-variables to combobox from dataframes;
        self.cmb_y_axis.clear()
        self.cmb_y_axis.addItem('choose a field')
        self.cmb_add_y_axis.clear()
        self.cmb_add_y_axis.addItem('choose a field')
        for field in self.df_db.columns:
            self.cmb_y_axis.addItem(str(field))
            self.cmb_add_y_axis.addItem(str(field))




    # -----------------------------------------------------------------------------------------------------------------
    # step 4-6; to draw graph from tables;
    # -----------------------------------------------------------------------------------------------------------------
    def draw_graph(self):

        try:

            if self.rbtnDb_datatype.isChecked():
                print('hello,kitty')



                # to test graph;
                # x = np.arange(0, 10, 0.1)
                # y = np.sin(x)
                # self.ax.plot(x, y)

                self.ax.clear()
                x = self.cmb_x_axis.currentText()
                y = self.cmb_y_axis.currentText()
                print('x;', x)
                print('y;', y)
                # to load x, and y-variables from combo;
                xx = self.df_db[x]
                yy = self.df_db[y]

                self.ax.plot(xx, yy)
                self.canvas.draw()




            elif self.rbtnFile_datatype.isChecked():
                # self.ax_1.clear()
                # self.ax_2.clear()


                x = self.cmb_x_axis.currentText()
                y = self.cmb_y_axis.currentText()
                print('x;', x)
                print('y;', y)



                # to load x, and y-variables from combo;
                print('edt col begin;', self.edt_col_begin.text())
                print('edt col end;', self.edt_col_end.text())


                xxx = self.df.loc[:20, x]
                # yy = self.df.iloc[y]
                print('xxx;', xxx)
                #
                #
                # to load x, and y-variables from combo;
                xx = self.df[x]
                yy = self.df[y]
                print('xx;', xx)
                print('yy;', yy)
                #
                #


                if self.cmb_canvas.currentText() == 'canvas_1':
                    self.ax_1.clear()
                    # self.ax_2.clear()
                    self.ax_1.scatter(xx, yy)
                    # self.ax.plot(xx, yy)
                    xlbl = self.cmb_x_axis.currentText()
                    ylbl = self.cmb_y_axis.currentText()

                    self.ax_1.set_xlabel(xlbl)
                    self.ax_1.set_ylabel(ylbl)


                    self.ax_2.clear()



                elif self.cmb_canvas.currentText() == 'canvas_2':

                    # #
                    # # to select data according to x- and y-range;
                    # #
                    # fromSelectedRows = self.edt_col_begin.text()
                    # toSelectedRows = self.edt_col_end.text()
                    #
                    # x2 = self.df.loc[fromSelectedRows:toSelectedRows, x]
                    # y2 = self.df.loc[fromSelectedRows:toSelectedRows, y]
                    # # xx = self.df.loc[1000:2000, x]
                    # # yy = self.df.loc[1000:2000, y]
                    # print('x2;', x2)
                    # print('y2;', y2)
                    # #
                    # #
                    #





                    X_ = self.df[[x]]
                    y_ = self.df[y]
                    print('dfx2;', X_)
                    print('dfy2;', y_)




                    # # self.ax_1.clear()
                    # self.ax_2.clear()
                    # self.ax_2.scatter(X_, y_)
                    # # self.ax.plot(xx, yy)
                    #
                    #
                    # xlbl = self.cmb_x_axis.currentText()
                    # ylbl = self.cmb_y_axis.currentText()
                    #
                    # self.ax_2.set_xlabel(xlbl)
                    # self.ax_2.set_ylabel(ylbl)




                    # from sklearn.model_selection import train_test_split

                    # 랜덤 시드 고정
                    SEED = 12
                    # random.seed(SEED)
                    # np.random.seed(SEED)
                    print("시드 고정: ", SEED)

                    X_train, X_test, y_train, y_test = train_test_split(X_, y_, test_size=0.3, shuffle=True, random_state=SEED)
                    # X_train
                    # x_train.shape
                    print('number of train data;', len(X_train))
                    print('number of test data;', len(X_test))



                    # to make polynomial functions;
                    from sklearn import linear_model
                    from sklearn import preprocessing

                    # to make 2nd order polynomial function;
                    poly = preprocessing.PolynomialFeatures(degree=1)
                    X_train_polyed = poly.fit_transform(X_train)
                    print('original train data;', X_train.shape)
                    print('polyed train data;', X_train_polyed.shape)







                    from sklearn import linear_model
                    model = linear_model.LinearRegression()
                    model.fit(X_train_polyed, y_train)

                    # from sklearn import linear_model
                    # model = linear_model.LinearRegression()
                    # model.fit(X_train, y_train)
                    # model.fit(X_, y_)









                    X_test_polyed = poly.fit_transform(X_test)
                    r_square = model.score(X_test_polyed, y_test)
                    print('r2;', r_square)

                    # r_square = model.score(X_test, y_test)
                    # # r_square = model.score(X_, y_)
                    # print('r2;', r_square)







                    print('coefficient;', model.coef_)
                    print('intercept;', model.intercept_)









                    # y_pred = model.predict(X_)
                    # self.ax_2.scatter(X_, y_pred, color='r')
                    y_pred = model.predict(X_test_polyed)

                    # y_pred = model.predict(X_test)
                    self.ax_2.scatter(X_test, y_pred, color='r')
                    self.ax_1.scatter(X_test, y_pred, color='r')





                    if self.ckbx_add_graph.isChecked():
                        y_add = self.cmb_add_y_axis.currentText()

                        # X_ = self.df[[x]]
                        y_add_ = self.df[y_add]
                        # print('dfx2;', X_)
                        # print('dfy2;', y_)
                        self.ax_2.scatter(X_, y_add_)


                    # #
                    # #
                    # # to call calculated data;
                    # #
                    # #
                    # xlbl = self.cmb_x_axis.currentText()
                    # ylbl = self.cmb_y_axis.currentText()
                    #
                    # X_ = self.df[[x]]
                    # y_ = self.df[y]
                    # print('dfx2;', X_)
                    # print('dfy2;', y_)
                    #
                    #
                    #
                    #
                    # # # self.ax_1.clear()
                    # # self.ax_2.clear()
                    # self.ax_2.scatter(X_, y_)
                    # # # self.ax.plot(xx, yy)
                    # #











        except:
            pass

        finally:

            self.canvas_1.draw()
            self.canvas_2.draw()
            pass






    # -----------------------------------------------------------------------------------------------------------------
    # step 4-7; to open file and load data to tables;
    # -----------------------------------------------------------------------------------------------------------------
    def open_from_file(self):


        #
        # to open file;
        #
        filename = QFileDialog.getOpenFileName(self, 'Open File', './', '*csv *xlsx')
        # self.df = pd.read_csv(filename[0], index_col=0)




        # to go if fileopen succeed;
        if filename[0]:


            #
            # to load a csv file or an excel file;
            #
            if filename[0].endswith('.csv'):
                self.df = pd.read_csv(filename[0])
                # self.df = pd.read_csv(filename[0], index_col = 0)
            elif filename[0].endswith(".xlsx"):
                print("Selected file is an excel file")
                # df = pd.read_excel(filename[0], dtype={'Column1': str}, index_col = 0)
                self.df = pd.read_excel(filename[0], dtype={'Column1': str})
            else:
                print("Selected file is neither an Excel nor a CSV file")
            print('index;', self.df.index)



            #
            # to count rows and columns;
            #
            self.tbl_two.setRowCount(len(self.df.index))
            print('index count;', len(self.df.index))
            self.tbl_two.setColumnCount(len(self.df.columns))
            print('column count;', len(self.df.columns))


            #
            # to make columns header label;
            #
            self.tbl_two.setHorizontalHeaderLabels(self.df.columns)
            # self.tbl_two.setHorizontalHeaderLabels(('id','longitude','altitude','value'))


            for row_index, row in enumerate(self.df.index):
                for col_index, column in enumerate(self.df.columns):

                    value = self.df.loc[row][column]
                    item = QTableWidgetItem(str(value))

                    # item = QTableWidgetItem(value)
                    self.tbl_two.setItem(row_index,col_index, item)







    # -----------------------------------------------------------------------------------------------------------------
    # step 4-8; to open file and load data to tables;
    # -----------------------------------------------------------------------------------------------------------------
    def data_aboveHeight(self):

        self.edt_presimul.setText('Button_aboveHeight pressed; ')


        # to get data from edit;
        # aboveAltitude = self.edt_altitude.toPlainText()
        aboveAltitude = float(self.edt_altitude.text())


        # to select the level of height;
        # self.dfhigh = self.df[self.df['Alt']>= 140]
        self.dfhigh = self.df[self.df['Alt']>= aboveAltitude]
        print(len(self.dfhigh))



        #
        # to count rows and columns;
        #
        self.tbl_height.setRowCount(len(self.dfhigh.index))
        print('index count;', len(self.dfhigh.index))
        self.tbl_height.setColumnCount(len(self.dfhigh.columns))
        print('column count;', len(self.dfhigh.columns))

        #
        # to make columns header label;
        #
        self.tbl_height.setHorizontalHeaderLabels(self.dfhigh.columns)
        # self.tbl_two.setHorizontalHeaderLabels(('id','longitude','altitude','value'))

        for row_index, row in enumerate(self.dfhigh.index):
            for col_index, column in enumerate(self.dfhigh.columns):
                value = self.dfhigh.loc[row][column]
                item = QTableWidgetItem(str(value))

                # item = QTableWidgetItem(value)
                self.tbl_height.setItem(row_index, col_index, item)







        #################################################
        ## to load x,y variables to combobox;
        #################################################
        #
        # to load x-variables to combobox from dataframes;
        #
        self.cmb_x_axis.clear()
        self.cmb_x_axis.addItem('choose a field')
        for field in self.df.columns:
            self.cmb_x_axis.addItem(str(field))


        #
        # to load y-variables to combobox from dataframes;
        #
        self.cmb_y_axis.clear()
        self.cmb_y_axis.addItem('choose a field')
        self.cmb_add_y_axis.clear()
        self.cmb_add_y_axis.addItem('choose a field')
        for field in self.df.columns:
            self.cmb_y_axis.addItem(str(field))
            self.cmb_add_y_axis.addItem(str(field))
















    # -----------------------------------------------------------------------------------------------------------------
    # step 4-8; to connect k3i api;
    # -----------------------------------------------------------------------------------------------------------------
    def connect_k3i_api(self):
        import requests
        import pprint
        import json

        url = 'http://211.194.140.86:28000/?year=2022&month=10&day=20'
        # url = 'http://211.194.140.86:28000'


        response = requests.get(url)
        contents = response.text
        print(contents)
        pp = pprint.PrettyPrinter(indent=4)
        print(pp.pprint(contents))

        json_db = json.loads(contents)
        print(json_db)




        # # URL
        # # 127.0.0.1은 localhost로 대체 가능
        # url = 'http://211.194.140.86:28000/?year=2022&month=10&day=25'
        #
        # # headers
        # headers = {
        #     "Content-Type": "application/json"
        # }
        #
        # # data
        # temp = {
        #     "color": "black",
        #     "size": 200
        # }
        # # 딕셔너리를 JSON으로 변환
        # data = json.dumps(temp)
        #
        # # response = requests.post(url, headers=headers, data=data)
        # response = requests.post(url, headers=headers)
        # print("response: ", response)
        # print("response.text: ", response.text)



    # -----------------------------------------------------------------------------------------------------------------
    # step 4-9; to make tables;
    # -----------------------------------------------------------------------------------------------------------------

    def make_some_table(self):
        print('hello,kitty')
        self.tbl_one.setRowCount(3)
        self.tbl_one.setColumnCount(2)

        self.tbl_one.setHorizontalHeaderLabels(('brand','price'))

        self.tbl_one.setColumnWidth(0,120)
        self.tbl_one.setColumnWidth(1,50)

        self.tbl_one.setItem(0, 0, QTableWidgetItem('phone1'))
        self.tbl_one.setItem(0, 1, QTableWidgetItem('1000'))
        self.tbl_one.setItem(1, 0, QTableWidgetItem('phone1'))
        self.tbl_one.setItem(1, 1, QTableWidgetItem('1000'))
        self.tbl_one.setItem(2, 0, QTableWidgetItem('phone1'))
        self.tbl_one.setItem(2, 1, QTableWidgetItem('1000'))


        products = [
            {'name': '1', 'price': 1000},
            {'name': '2', 'price': 2000},
            {'name': '3', 'price': 3000},
        ]

        row_index = 0
        for product in products:
            self.tbl_one.setItem(row_index, 0, QTableWidgetItem(str(product['name'])))
            self.tbl_one.setItem(row_index, 1, QTableWidgetItem(str(product['price'])))
            row_index += 1





if __name__ == "__main__" :
    app = QApplication(sys.argv)

    mainWindow = WindowClass()
    mainWindow.show()

    app.exec_()