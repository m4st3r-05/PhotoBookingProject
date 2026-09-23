from flask import Flask, request, render_template_string
import matplotlib
matplotlib.use("Agg")  # vẽ không cần màn hình
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Thống kê sinh viên nam/nữ</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; padding: 0 16px; }
        h1 { font-size: 22px; }
        label { display: block; margin-top: 12px; font-weight: bold; }
        input { width: 100%; padding: 8px; margin-top: 4px; box-sizing: border-box; }
        button { margin-top: 16px; padding: 10px 20px; cursor: pointer; }
        .error { color: #c00; margin-top: 12px; }
        img { max-width: 100%; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>Nhập số sinh viên nam/nữ trong một lớp</h1>
    <form method="post">
        <label>Số sinh viên nam</label>
        <input type="number" name="nam" min="0" value="{{ nam }}" required>
        <label>Số sinh viên nữ</label>
        <input type="number" name="nu" min="0" value="{{ nu }}" required>
        <button type="submit">Hiển thị biểu đồ</button>
    </form>
    {% if error %}<p class="error">{{ error }}</p>{% endif %}
    {% if chart %}
        <p>Tổng số sinh viên: <b>{{ tong }}</b></p>
        <img src="data:image/png;base64,{{ chart }}" alt="Biểu đồ cột">
    {% endif %}
</body>
</html>
"""


def ve_bieu_do(nam, nu):
    fig, ax = plt.subplots(figsize=(5, 4))
    cot = ax.bar(["Nam", "Nữ"], [nam, nu], color=["#3b82f6", "orange"])
    ax.bar_label(cot)
    ax.set_ylabel("Số sinh viên")
    ax.set_title("Số sinh viên nam / nữ trong lớp")
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()


@app.route("/", methods=["GET", "POST"])
def index():
    nam, nu, chart, tong, error = "", "", None, 0, None
    if request.method == "POST":
        nam = request.form.get("nam", "").strip()
        nu = request.form.get("nu", "").strip()
        try:
            n, f = int(nam), int(nu)
            if n < 0 or f < 0:
                raise ValueError
            chart = ve_bieu_do(n, f)
            tong = n + f
        except ValueError:
            error = "Vui lòng nhập số nguyên không âm."
    return render_template_string(HTML, nam=nam, nu=nu, chart=chart, tong=tong, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5175)