from flask import Flask, render_template, request, jsonify
from math import comb

app = Flask(__name__)

def calculate_binomial_probability(n, p, k):
    # Rumus binomial: P(X = k) = C(n, k) * (p^k) * ((1-p)^(n-k))
    coefficient = comb(n, k)  # Kombinasi C(n, k)
    success_prob = p**k  # Probabilitas sukses
    failure_prob = (1-p)**(n-k)  # Probabilitas gagal
    probability = coefficient * success_prob * failure_prob

    # Memformat agar angka nol di belakang koma hilang
    formatted_probability = f"{probability:.10f}".rstrip('0').rstrip('.')
    formatted_success_prob = f"{success_prob:.10f}".rstrip('0').rstrip('.')
    formatted_failure_prob = f"{failure_prob:.10f}".rstrip('0').rstrip('.')
    formatted_coefficient = f"{coefficient:.0f}"

    # Langkah-langkah
    steps = [
        f"Langkah 1: Identifikasi Nilai yang Diberikan<br>"
        f"<br>"
        f"- Jumlah Percobaan (n): {n}<br>"
        f"- Probabilitas Keberhasilan (p): {p}<br>"
        f"- Jumlah Keberhasilan (k): {k}<br>"
        f"<br>"
        "Langkah 2: Substitusikan Nilai ke dalam Rumus\n"
        f"$$P(X = k) = \\binom{{n}}{{k}} (p)^k (1-p)^{{n-k}}$$\n"
        f"$$P(X = {k}) = \\binom{{{n}}}{{{k}}} ({p})^{k} (1-{p})^{{{n-k}}}$$",
        "Langkah 3: Hitung Koefisien Binomial\n"
        f"$$\\binom{{{n}}}{{{k}}} = {formatted_coefficient}$$",
        "Langkah 4: Hitung Probabilitas\n"
        f"$$P(X = {k}) = {formatted_coefficient} \\times ({p})^{k} \\times (1-{p})^{{{n-k}}}$$\n"
        f"$$P(X = {k}) = {formatted_coefficient} \\times {formatted_success_prob} \\times {formatted_failure_prob}$$\n"
        f"$$P(X = {k}) = {formatted_probability}$$"
    ]
    
    # Langkah 5: Menghitung Probabilitas Kumulatif P(X ≤ k)
    cumulative_prob = sum(comb(n, i) * pow(p, i) * pow(1 - p, n - i) for i in range(k + 1))
    formatted_cumulative_prob = f"{cumulative_prob:.10f}".rstrip('0').rstrip('.')
    steps.insert(0, f"$$P(X \\leq {k}) = {formatted_cumulative_prob}$$")

    # Langkah-langkah CDF (Langkah 6-9)
    steps.append(f"Langkah 5: Memahami Fungsi Distribusi Kumulatif Binomial<br>"
                 "$$P(X \\leq {k}) = \\sum_{{i=0}}^{{{k}}} \\binom{{{n}}}{{i}} ({p})^{i} (1-{p})^{{n-i}}$$")
    steps.append(f"Langkah 6: Kembangkan Penjumlahan<br>"
                 f"$$P(X \\leq {k}) = \\sum_{{i=0}}^{{{k}}} \\binom{{{n}}}{{i}} (p)^i (1-p)^{{n-i}}$$") 
    # Hitung setiap term dalam penjumlahan
    cdf_terms = [
        f"$$\\binom{{{n}}}{{{i}}} ({p})^{i} (1-{p})^{{n-i}} = {comb(n, i) * pow(p, i) * pow(1 - p, n - i):.10f}".rstrip('0').rstrip('.') + "$$"
        for i in range(k + 1)
    ]
    steps.append(f"Langkah 7: Hitung Setiap Term dalam Penjumlahan<br>" + "<br>".join(cdf_terms))
    # Jumlahkan semua term untuk mendapatkan probabilitas kumulatif
    steps.append(f"Langkah 8: Jumlahkan Semua Term untuk Mendapatkan Probabilitas Kumulatif<br>"
                 f"$$P(X \\leq {k}) = {formatted_cumulative_prob}$$")
    return formatted_probability, steps


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        n = int(request.form['n'])
        p = float(request.form['p'])
        k = int(request.form['k'])
        result, steps = calculate_binomial_probability(n, p, k)
        return jsonify({'result': result, 'steps': steps})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)