from flask import Flask, render_template, request, flash
import requests

app = Flask(__name__)
app.secret_key = "supersecretkey" # Required for flashing error messages

# API Configurations (Replace with your actual keys)
WEATHER_API_KEY = "your_openweathermap_api_key"
NEWS_API_KEY = "your_newsapi_key"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    news_articles = []
    city = request.form.get("city")
    topic = request.form.get("topic", "Technology") # Default topic

    if request.method == "POST":
        # --- Part A: Weather Logic ---
        if city:
            w_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
            w_response = requests.get(w_url).json()
            
            if w_response.get("cod") == 200:
                weather_data = {
                    "temp": w_response["main"]["temp"],
                    "desc": w_response["weather"][0]["description"],
                    "country": w_response["sys"]["country"],
                    "city": city
                }
            else:
                flash(f"City '{city}' not found!", "danger") # Bonus: Error Handling

        # --- Part B: News Logic ---
        n_url = f"https://newsapi.org/v2/everything?q={topic}&pageSize=3&apiKey={NEWS_API_KEY}"
        n_response = requests.get(n_url).json()
        if n_response.get("status") == "ok":
            news_articles = n_response.get("articles", [])

    return render_template("index.html", weather=weather_data, news=news_articles, topic=topic)

if __name__ == "__main__":
    app.run(debug=True)