import re

def calculate_score(alternatives, user_input=None, preference_profile='basic'):
    if not alternatives:
        return {}

    # =========================
    # HELPER
    # =========================
    def to_float(val):
        try:
            return float(val)
        except:
            return 0.0

    def extract_first_number(val):
        nums = re.findall(r"\d+\.?\d*", str(val))
        if not nums:
            return 0.0
        return float(nums[0])

    def extract_max_number(val):
        nums = re.findall(r"\d+\.?\d*", str(val))
        if not nums:
            return 0.0
        return max([float(n) for n in nums])

    # Konversi ke skala 1-5
    def konversi_panjang(val):
        panjang = extract_first_number(val)
        if panjang >= 50:
            return 5
        elif panjang >= 45:
            return 4
        elif panjang >= 35:
            return 3
        elif panjang >= 30:
            return 2
        else:
            return 1

    def konversi_kedalaman(val):
        kedalaman = extract_max_number(val)
        if kedalaman >= 2.0:
            return 5
        elif kedalaman >= 1.8:
            return 4
        elif kedalaman >= 1.5:
            return 3
        elif kedalaman >= 1.2:
            return 2
        else:
            return 1

    def konversi_jalur(val):
        jalur = extract_first_number(val)
        if jalur >= 8:
            return 5
        elif jalur >= 6:
            return 4
        elif jalur >= 5:
            return 3
        elif jalur >= 4:
            return 2
        else:
            return 1

    def konversi_harga(val):
        harga = to_float(val)
        if harga < 15000:
            return 5
        elif harga < 30000:
            return 4
        elif harga < 45000:
            return 3
        elif harga < 60000:
            return 2
        else:
            return 1

    def konversi_kategori(val):
        if val is None:
            return 3
        val = str(val).lower().strip()
        mapping = {
            "sangat bersih": 5, "bersih": 4, "cukup": 3, "kurang": 2, "sangat kurang": 1,
            "sangat lengkap": 5, "lengkap": 4, "cukup": 3, "kurang": 2,
            "sangat mudah": 5, "mudah": 4, "cukup": 3, "sulit": 2, "sangat sulit": 1,
            "ada": 5, "ya": 5, "tidak": 1, "tidak ada": 1
        }
        return mapping.get(val, 3)

    def konversi_air_hangat(val):
        val = str(val).lower().strip()
        if val in ["ya", "ada", "hangat"]:
            return 1
        return 0

    scores = {}

    for alt in alternatives:
        name = alt.get("name")

        # Konversi ke skala 1-5
        skor_panjang = konversi_panjang(alt.get("panjang"))
        skor_kedalaman = konversi_kedalaman(alt.get("kedalaman"))
        skor_jalur = konversi_jalur(alt.get("jalur"))
        skor_harga = konversi_harga(alt.get("harga"))
        skor_rating = min(max(to_float(alt.get("rating")), 1), 5)
        
        papan_start = str(alt.get("papan_start", "")).lower()
        pace_clock = str(alt.get("pace_clock", "")).lower()
        skor_papan = 5 if papan_start in ["ada", "ya"] else 1
        skor_pace = 5 if pace_clock in ["ada", "ya"] else 1
        
        skor_kebersihan = konversi_kategori(alt.get("kebersihan"))
        skor_fasilitas = konversi_kategori(alt.get("fasilitas"))
        skor_lokasi = konversi_kategori(alt.get("lokasi"))
        skor_air = konversi_air_hangat(alt.get("air_hangat"))

        # Normalisasi ke 0-1
        norm_panjang = skor_panjang / 5
        norm_kedalaman = skor_kedalaman / 5
        norm_jalur = skor_jalur / 5
        norm_papan = skor_papan / 5
        norm_pace = skor_pace / 5
        norm_harga = skor_harga / 5
        norm_rating = skor_rating / 5
        norm_kebersihan = skor_kebersihan / 5
        norm_fasilitas = skor_fasilitas / 5
        norm_lokasi = skor_lokasi / 5
        norm_air = skor_air

        # =========================
        # PREFERENSI ATLET
        # =========================
        if preference_profile == "atlet":
            weights = {
                "panjang": 0.25,
                "kedalaman": 0.20,
                "jalur": 0.15,
                "papan_start": 0.10,
                "pace_clock": 0.10,
                "harga": 0.10,
                "rating": 0.10
            }

            score = (
                norm_panjang * weights["panjang"] +
                norm_kedalaman * weights["kedalaman"] +
                norm_jalur * weights["jalur"] +
                norm_papan * weights["papan_start"] +
                norm_pace * weights["pace_clock"] +
                norm_harga * weights["harga"] +
                norm_rating * weights["rating"]
            )

        # =========================
        # PREFERENSI BASIC
        # =========================
        else:
            weights = {
                "harga": 0.30,
                "kebersihan": 0.20,
                "fasilitas": 0.20,
                "air_hangat": 0.10,
                "rating": 0.20
            }

            score = (
                norm_harga * weights["harga"] +
                norm_kebersihan * weights["kebersihan"] +
                norm_fasilitas * weights["fasilitas"] +
                norm_air * weights["air_hangat"] +
                norm_rating * weights["rating"]
            )

        score = max(0, min(score, 1))
        scores[name] = round(score, 4)

    return scores