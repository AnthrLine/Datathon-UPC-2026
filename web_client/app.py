from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

INT32_MIN = -2_147_483_648
INT32_MAX = 2_147_483_647

LANGUAGES = [
    ("en", "English"), ("es", "Español"), ("ca", "Català"), ("fr", "Français"),
    ("de", "Deutsch"), ("it", "Italiano"), ("pt", "Português"), ("nl", "Nederlands"),
    ("pl", "Polski"), ("sv", "Svenska"), ("no", "Norsk"), ("da", "Dansk"),
    ("fi", "Suomi"), ("el", "Ελληνικά"), ("cs", "Čeština"), ("ro", "Română"),
    ("hu", "Magyar"), ("uk", "Українська"), ("ru", "Русский"), ("tr", "Türkçe"),
    ("ar", "العربية"), ("he", "עברית"), ("hi", "हिन्दी"), ("bn", "বাংলা"),
    ("zh", "中文"), ("ja", "日本語"), ("ko", "한국어"), ("vi", "Tiếng Việt"),
    ("th", "ไทย"), ("id", "Bahasa Indonesia"), ("sw", "Kiswahili"),
]


def parse_int32(raw_value, default=1):
    try:
        val = int(raw_value)
        return max(INT32_MIN, min(INT32_MAX, val))
    except (TypeError, ValueError):
        return default


def get_problem(lang, complexity):
    return {
        "id": 42,
        "image_url": "/static/sample_problem.png",
        "correct_option": "C",
    }


@app.route("/", methods=["GET"])
def index():
    lang = request.args.get("lang", "en")
    complexity = parse_int32(request.args.get("complexity"), default=1)
    problem = get_problem(lang, complexity)

    return render_template(
        "index.html",
        languages=LANGUAGES,
        selected_language=lang,
        complexity=complexity,
        problem=problem,
        selected_choice=None,
        feedback=None,
    )


@app.route("/submit", methods=["POST"])
def submit_answer():
    lang = request.form.get("lang", "en")
    complexity = parse_int32(request.form.get("complexity"), default=1)
    choice = request.form.get("choice")
    problem = get_problem(lang, complexity)

    is_correct = choice == problem["correct_option"]
    feedback = {
        "correct": is_correct,
        "message": "Correct." if is_correct else f"Option {choice} is incorrect. Try again or ask for help.",
    }

    return render_template(
        "index.html",
        languages=LANGUAGES,
        selected_language=lang,
        complexity=complexity,
        problem=problem,
        selected_choice=choice,
        feedback=feedback,
    )


@app.route("/help", methods=["GET"])
def progressive_help():
    level = parse_int32(request.args.get("level"), default=1)
    # Replace with your model/database lookup keyed by problem_id and lang
    responses = {
        1: "Try solving a smaller version first: find x when 2x + 4 = 10.",
        2: "Linear equations and isolating variables.",
        3: "Subtract the constant term from both sides before dividing by the coefficient.",
        4: "Step 1: 3x + 6 = 21 → 3x = 15. Step 2: x = 5, which matches Option C.",
    }
    return jsonify({"level": level, "content": responses.get(level, "")})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)