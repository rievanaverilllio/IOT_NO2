from flask import Flask, jsonify, request, render_template
import datetime
import random

app = Flask(__name__)

data = {
    "suhumax": 0,
    "suhumin": 0,
    "suhurata": 0,
    "nilai_suhu_max_humid_max": [
        {
            "idx": 101,
            "suhu": 36,
            "humid": 36,
            "kecerahan": 25,
            "timestamp": "2010-09-18 07:23:48"
        },
        {
            "idx": 226,
            "suhu": 21,
            "humid": 36,
            "kecerahan": 27,
            "timestamp": "2011-05-02 12:29:34"
        }
    ],
    "month_year_max": [
        {"month_year": ""},
        {"month_year": ""}
    ]
}

def hitung_statistik():
    suhu_max = -float('inf')
    suhu_min = float('inf')
    suhu_total = 0
    count = 0
    timestamp_terlama = None
    timestamp_terbaru = None

    for entry in data["nilai_suhu_max_humid_max"]:
        suhu = entry["suhu"]
        timestamp = entry["timestamp"]

        if suhu > suhu_max:
            suhu_max = suhu
        if suhu < suhu_min:
            suhu_min = suhu

        suhu_total += suhu
        count += 1

        try:
            timestamp_obj = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            timestamp_obj = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M")

        if not timestamp_terlama or timestamp_obj < timestamp_terlama:
            timestamp_terlama = timestamp_obj
        if not timestamp_terbaru or timestamp_obj > timestamp_terbaru:
            timestamp_terbaru = timestamp_obj

    suhu_rata_rata = suhu_total / count if count > 0 else 0

    data["suhumax"] = suhu_max
    data["suhumin"] = suhu_min
    data["suhurata"] = suhu_rata_rata
    data["month_year_max"][0]["month_year"] = timestamp_terlama.strftime("%Y-%m")
    data["month_year_max"][1]["month_year"] = timestamp_terbaru.strftime("%Y-%m")

@app.route('/')
def tampilkan():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def ambil_data():
    hitung_statistik()
    return jsonify(data)

@app.route('/data', methods=['POST'])
def perbarui_data():
    data_baru = request.json
    if data_baru:
        if "nilai_suhu_max_humid_max" in data_baru:
            for entry in data_baru["nilai_suhu_max_humid_max"]:
                entry["idx"] = random.randint(200, 999)
        
        data["nilai_suhu_max_humid_max"].extend(data_baru["nilai_suhu_max_humid_max"])
        
        hitung_statistik()
        return jsonify({"message": "Data berhasil diperbarui", "data": data}), 200
    else:
        return jsonify({"message": "Data yang diberikan tidak valid"}), 400

if __name__ == '__main__':
    app.run(debug=True)
