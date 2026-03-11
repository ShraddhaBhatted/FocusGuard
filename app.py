from flask import Flask, render_template
import pandas as pd
import pickle
import matplotlib.pyplot as plt

app = Flask(__name__)

# Load model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

@app.route("/")
def index():
    df = pd.read_csv("TestingHistory.csv")

    sites = df.iloc[:, 0]
    time_spent = df.iloc[:, -1]

    X_vec = vectorizer.transform(sites)
    predictions = model.predict(X_vec)

    df["label"] = predictions
    df["time_spent"] = time_spent

    distracted_time = df[df["label"] == "distracting"]["time_spent"].sum()
    productive_time = df[df["label"] == "productive"]["time_spent"].sum()

    # Plot
    plt.figure(figsize=(6,4))
    plt.bar(["Productive", "Distracting"], [productive_time, distracted_time])
    plt.ylabel("Time Spent")
    plt.title("Focus Analysis")
    plt.savefig("static/plot.png")
    plt.close()

    score = round((distracted_time / (distracted_time + productive_time)) * 100, 2)

    return render_template(
        "index.html",
        score=score,
        productive=productive_time,
        distracted=distracted_time
    )

if __name__ == "__main__":
    app.run(debug=True)
