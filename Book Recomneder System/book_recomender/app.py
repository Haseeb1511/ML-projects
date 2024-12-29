
from flask import Flask,render_template,request
import pickle
import pandas as pd
import numpy as np
final_rating=pickle.load(open("final_rating.pkl","rb"))
book=pickle.load(open("book.pkl","rb"))
pt=pickle.load(open("pt.pkl","rb"))
similarity_score=pickle.load(open("similarity_score.pkl","rb"))


app=Flask(__name__)



@app.route("/")
def main():
    return render_template('index.html',
                           images=list(final_rating["Image-URL-M"].values),
                           book_title=list(final_rating["Book-Title"].values),
                           book_aurthor=list(final_rating["Book-Author"].values),
                           num_rating=list(final_rating["Num_Rating"].values),
                           avg_rating=np.round(list(final_rating["Avg_Rating"].values),1)
                           )


@app.route("/recomend")
def book_recomend():
    book_name=sorted(final_rating["Book-Title"].unique())
    return render_template('recomend.html',
                           book_name=book_name)


@app.route("/recomend_books" ,methods=["POST"])
def recomend():
    user_input=request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_item = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]
    data = []
    for i in similar_item:
        l = []
        temp = book[book["Book-Title"] == pt.index[i[0]]]
        l.extend(list(temp.drop_duplicates("Book-Title")["Book-Title"].values))
        l.extend(list(temp.drop_duplicates("Book-Title")["Book-Author"].values))
        l.extend(list(temp.drop_duplicates("Book-Title")["Image-URL-M"].values))
        data.append(l)
    print(data)

    return render_template('recomend.html',data=data)

if __name__=="__main__":
    app.run(debug=True)