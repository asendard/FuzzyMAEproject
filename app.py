import streamlit as st

# Fungsi Keanggotaan Segitiga
def triangular_membership(x, a, b, c):
    if x <= a or x >= c:
        return 0
    elif a < x < b:
        return (x - a) / (b - a)
    elif b <= x < c:
        return (c - x) / (c - b)
    else:
        return 0

# Fungsi Fuzzification
def fuzzification(request_count, security_level, anomalous_volume):
    # Request Count
    rc_low = triangular_membership(request_count, 0, 0, 500)
    rc_med = triangular_membership(request_count, 250, 500, 750)
    rc_high = triangular_membership(request_count, 500, 1000, 1000)
    
    # System Security Level
    sl_low = triangular_membership(security_level, 0, 0, 5)
    sl_med = triangular_membership(security_level, 2, 5, 8)
    sl_high = triangular_membership(security_level, 5, 10, 10)
    
    # Anomalous Data Volume
    av_low = triangular_membership(anomalous_volume, 0, 0, 250)
    av_med = triangular_membership(anomalous_volume, 100, 250, 400)
    av_high = triangular_membership(anomalous_volume, 250, 500, 500)
    
    return {
        "rc_low": rc_low, "rc_med": rc_med, "rc_high": rc_high,
        "sl_low": sl_low, "sl_med": sl_med, "sl_high": sl_high,
        "av_low": av_low, "av_med": av_med, "av_high": av_high
    }

# Fungsi Evaluasi Aturan Fuzzy (Sugeno)
def evaluate_rules(fuzzy_values):
    rule_outputs = []
    
    # Rule 1
    degree = min(fuzzy_values["rc_low"], fuzzy_values["sl_low"], fuzzy_values["av_low"])
    rule_outputs.append(("Aturan 1", degree, 30))
    
    # Rule 2
    degree = min(fuzzy_values["rc_med"], fuzzy_values["sl_low"], fuzzy_values["av_med"])
    rule_outputs.append(("Aturan 2", degree, 60))
    
    # Rule 3
    degree = min(fuzzy_values["rc_low"], fuzzy_values["sl_high"], fuzzy_values["av_low"])
    rule_outputs.append(("Aturan 3", degree, 20))
    
    # Rule 4
    degree = min(fuzzy_values["rc_high"], fuzzy_values["sl_low"], fuzzy_values["av_high"])
    rule_outputs.append(("Aturan 4", degree, 95))
    
    # Rule 5
    degree = min(fuzzy_values["rc_med"], fuzzy_values["sl_med"], fuzzy_values["av_low"])
    rule_outputs.append(("Aturan 5", degree, 40))
    
    # Rule 6
    degree = min(fuzzy_values["rc_high"], fuzzy_values["sl_low"], fuzzy_values["av_high"])
    rule_outputs.append(("Aturan 6", degree, 85))
    
    # Rule 7
    degree = min(fuzzy_values["rc_low"], fuzzy_values["sl_high"], fuzzy_values["av_low"])
    rule_outputs.append(("Aturan 7", degree, 10))
    
    # Rule 8
    degree = min(fuzzy_values["rc_med"], fuzzy_values["sl_high"], fuzzy_values["av_low"])
    rule_outputs.append(("Aturan 8", degree, 50))
    
    # Rule 9
    degree = min(fuzzy_values["rc_high"], fuzzy_values["sl_med"], fuzzy_values["av_high"])
    rule_outputs.append(("Aturan 9", degree, 90))
    
    # Rule 10
    degree = min(fuzzy_values["rc_med"], fuzzy_values["sl_med"], fuzzy_values["av_low"])
    rule_outputs.append(("Aturan 10", degree, 35))
    
    # Filter rules with non-zero membership degree
    active_rules = [(rule, degree, output) for rule, degree, output in rule_outputs if degree > 0]
    return active_rules

# Fungsi Utama untuk FIS
def fis_system(request_count, security_level, anomalous_volume):
    fuzzy_values = fuzzification(request_count, security_level, anomalous_volume)
    active_rules = evaluate_rules(fuzzy_values)
    
    # Periksa apakah ada aturan aktif
    if not active_rules:
        # Jika tidak ada aturan aktif, kembalikan nilai default, misalnya 0
        return 0
    
    # Pilih aturan dengan derajat keanggotaan tertinggi
    selected_rule = max(active_rules, key=lambda x: x[1])
    rule_name, degree, output = selected_rule
    
    return output

# Fungsi Menghitung MAE
def calculate_mae(predicted, actual):
    errors = [abs(p - a) for p, a in zip(predicted, actual)]
    mae = sum(errors) / len(errors)
    return mae

# Dataset dengan Nilai Aktual (Contoh)
data = [
    {"request_count": 200, "security_level": 3, "anomalous_volume": 50, "actual": 30},
    {"request_count": 400, "security_level": 2, "anomalous_volume": 150, "actual": 60},
    {"request_count": 150, "security_level": 8, "anomalous_volume": 30, "actual": 20},
    {"request_count": 900, "security_level": 1, "anomalous_volume": 400, "actual": 95},
    {"request_count": 250, "security_level": 5, "anomalous_volume": 80, "actual": 40},
    {"request_count": 700, "security_level": 3, "anomalous_volume": 300, "actual": 85},
    {"request_count": 100, "security_level": 9, "anomalous_volume": 20, "actual": 10},
    {"request_count": 500, "security_level": 7, "anomalous_volume": 100, "actual": 50},
    {"request_count": 800, "security_level": 4, "anomalous_volume": 350, "actual": 90},
    {"request_count": 300, "security_level": 6, "anomalous_volume": 60, "actual": 35}
]

# Menghitung Prediksi dan MAE
def main():
    st.title("Cyber Attack Risk Level Prediction and MAE Calculation")
    
    predicted_values = []
    actual_values = []
    results = []
    
    # Menghitung prediksi berdasarkan input data
    for entry in data:
        predicted = fis_system(entry["request_count"], entry["security_level"], entry["anomalous_volume"])
        predicted_values.append(predicted)
        actual_values.append(entry["actual"])
        results.append({
            "Request Count": entry["request_count"],
            "System Security Level": entry["security_level"],
            "Anomalous Data Volume": entry["anomalous_volume"],
            "Predicted Risk Level": predicted,
            "Actual Risk Level": entry["actual"]
        })
    
    # Hitung MAE
    mae = calculate_mae(predicted_values, actual_values)
    
    # Tampilkan tabel hasil prediksi dan nilai aktual
    st.write("## Prediksi dan Nilai Aktual")
    st.table(results)
    
    # Tampilkan MAE
    st.write(f"## Mean Absolute Error (MAE): {mae:.2f}")
    
    # Interpretasi hasil MAE
    if mae < 10:
        st.write("Model FIS memiliki performa yang baik dalam memprediksi risiko serangan siber.")
    elif mae < 20:
        st.write("Model FIS memiliki performa yang cukup baik dalam memprediksi risiko serangan siber.")
    else:
        st.write("Model FIS memiliki performa yang kurang baik dan mungkin perlu disempurnakan.")

if __name__ == "__main__":
    main()
