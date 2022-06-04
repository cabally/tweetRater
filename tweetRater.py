import tweepy,csv
from textblob import TextBlob
from urlextract import URLExtract
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import  sys

from PyQt5 import QtCore, QtGui, QtWidgets

#this was ui code but I don't really know how would I connect it to backend.
#class Ui_Dialog(object):
#    def setupUi(self, Dialog):
#        Dialog.setObjectName("Dialog")
#        Dialog.resize(400, 300)
#        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
#        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
#        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
#        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
#        self.buttonBox.setObjectName("buttonBox")
#        self.label1 = QtWidgets.QLabel(Dialog)
#        self.label1.setGeometry(QtCore.QRect(40, 20, 51, 16))
#        self.label1.setObjectName("label1")
#        self.label_2 = QtWidgets.QLabel(Dialog)
#        self.label_2.setGeometry(QtCore.QRect(40, 70, 61, 16))
#        self.label_2.setObjectName("label_2")
#        self.lineEdit = QtWidgets.QLineEdit(Dialog)
#        self.lineEdit.setGeometry(QtCore.QRect(40, 40, 251, 20))
#        self.lineEdit.setObjectName("lineEdit")
 #       self.label_3 = QtWidgets.QLabel(Dialog)
  #      self.label_3.setGeometry(QtCore.QRect(300, 40, 47, 14))
   #     self.label_3.setObjectName("label_3")
    #    self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
     #   self.lineEdit_2.setGeometry(QtCore.QRect(40, 100, 251, 20))
      #  self.lineEdit_2.setObjectName("lineEdit_2")
       # self.progressBar = QtWidgets.QProgressBar(Dialog)
        #self.progressBar.setGeometry(QtCore.QRect(40, 210, 291, 23))
#        self.progressBar.setProperty("value", 24)
#        self.progressBar.setObjectName("progressBar")
#        self.label_4 = QtWidgets.QLabel(Dialog)
#        self.label_4.setGeometry(QtCore.QRect(40, 140, 121, 16))
#        self.label_4.setObjectName("label_4")
#        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
#        self.lineEdit_3.setGeometry(QtCore.QRect(40, 170, 81, 20))
#        self.lineEdit_3.setObjectName("lineEdit_3")

#        self.retranslateUi(Dialog)
#        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
#        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
#        QtCore.QMetaObject.connectSlotsByName(Dialog)

#    def retranslateUi(self, Dialog):
#        _translate = QtCore.QCoreApplication.translate
#        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
#        self.label1.setText(_translate("Dialog", "file name:"))
#        self.label_2.setText(_translate("Dialog", "search term:"))
#        self.label_3.setText(_translate("Dialog", ".csv"))
#        self.label_4.setText(_translate("Dialog", "tweet amount to harvest"))#


#if __name__ == "__main__":
#    import sys
#    app = QtWidgets.QApplication(sys.argv)
#    Dialog = QtWidgets.QDialog()
#    ui = Ui_Dialog()
#    ui.setupUi(Dialog)
#    Dialog.show()
#    sys.exit(app.exec_())

#these are keys to interface with twitter API
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''


auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

csvFileName = 'twitter_polarity_anal.csv' #what to save file name as
query = 'reddit' #search query
amount = 10 #the amount of results to save


public_tweets = api.search_tweets(q=query,count = amount,lang = 'en',result_type = 'popular')#this is where we place our search term and the amount to search

with open(csvFileName,'w',encoding="utf-8",newline='') as output:
    fileout =csv.writer(output)
    data = [['Tweet','polarity','subjectivity','URL','Polarity','Subjectivity']]

    fileout.writerow(data)

    for tweet in public_tweets:

        analysis = TextBlob(tweet.text)
        polar = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity

        print(analysis.sentiment)

        words = tweet.text.split()
        link = URLExtract()
        urls = link.find_urls(tweet.text)

        for word in words:
            if 'http' or 'https' in word:
                url = word


        print(tweet.text)
        print('Polarity',polar)
        print('Subjectivity:',subjectivity)


        #this decides what kind of category it fits into.
        if polar > 0:
            polarRating="the sentiment is positive"
        if polar == 0:
            polarRating="sentiment is neutral"
        if polar < 0:
            polarRating="the sentiment is negative"
        if subjectivity > 0.5:
            subjectivityRating="this is more of a personal opinion"
        if subjectivity < 0.5:
            subjectivityRating="this is less of a personal opinion and more factual"

        fileout.writerow([tweet.text, polar, subjectivity, url,polarRating,subjectivityRating])