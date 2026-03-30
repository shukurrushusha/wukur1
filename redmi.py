import datetime

def metro_kart_simulyatoru():
    # İlkin parametrlər
    pin = "1234"
    balans = 0.0
    borc = 0.0
    gedis_sayi = 0
    gunluk_artirma_cemi = 0.0
    
    # Parametrlər (Dəyişdirilə bilən)
    artirma_limiti = 100.0
    rejim = "Normal" # Normal, Telebe, Pensiyaci
    
    # Tarixçə (Əməliyyat siyahısı)
    emeliyyatlar = []

    # 1. PIN Girişi
    cehd = 3
    while cehd > 0:
        daxil_edilen_pin = input(f"Zəhmət olmasa 4 rəqəmli PIN daxil edin (Cəhd: {cehd}): ")
        if daxil_edilen_pin == pin:
            print("\nSistemə giriş uğurludur!")
            break
        else:
            cehd -= 1
            print("Yanlış PIN!")
            if cehd == 0:
                print("Kart bloklandı. Proqram dayanır.")
                return
    
    # 2. Əsas Menyu
    while True:
        print("\n" + "="*30)
        print(f" BALANS: {balans:.2f} AZN | BORC: {borc:.2f} AZN | REJİM: {rejim}")
        print("="*30)
        print("1) Balansı göstər")
        print("2) Balans artır")
        print("3) Gediş et (Turniket)")
        print("4) Son əməliyyatlara bax")
        print("5) Günlük statistika")
        print("6) Parametrlər")
        print("0) Çıxış")
        
        secim = input("\nSeçiminizi edin: ")

        if secim == "1":
            print(f"\nCari balansınız: {balans:.2f} AZN")
            if borc > 0: print(f"Ödəniləcək borc: {borc:.2f} AZN")

        elif secim == "2":
            try:
                mebleg = float(input("Artırılacaq məbləği daxil edin: "))
                if mebleg <= 0:
                    print("Xəta: Məbləğ müsbət olmalıdır!")
                elif gunluk_artirma_cemi + mebleg > artirma_limiti:
                    print(f"Xəta: Günlük limiti ({artirma_limiti} AZN) keçirsiniz!")
                else:
                    ilk_mebleg = mebleg
                    # Borc ödəmə məntiqi
                    if borc > 0:
                        if mebleg >= borc:
                            mebleg -= borc
                            borc = 0
                            print("Borcunuz tam ödənildi.")
                        else:
                            borc -= mebleg
                            mebleg = 0
                            print(f"Borcun bir hissəsi ödənildi. Qalan borc: {borc:.2f}")
                    
                    balans += mebleg
                    gunluk_artirma_cemi += ilk_mebleg
                    emeliyyatlar.append({
                        "tip": "Balans Artırma", 
                        "mebleg": ilk_mebleg, 
                        "balans": balans, 
                        "endirim": 0.0
                    })
                    print(f"Balans artırıldı! Yeni balans: {balans:.2f} AZN")
            except ValueError:
                print("Xəta: Düzgün rəqəm daxil edin!")

        elif secim == "3":
            # Qiymət təyini
            qiymet = 0.40
            endirim = 0.0
            
            if rejim == "Telebe":
                qiymet = 0.20
            elif rejim == "Pensiyaci":
                qiymet = 0.15
            else: # Normal rejim endirimləri
                if 1 <= gedis_sayi < 4: # 2, 3, 4-cü gedişlər
                    endirim = 0.40 * 0.10
                    qiymet = 0.40 - endirim
                elif gedis_sayi >= 4: # 5 və daha çox
                    endirim = 0.40 * 0.25
                    qiymet = 0.40 - endirim

            # Keçid yoxlanışı
            if balans >= qiymet:
                balans -= qiymet
                gedis_sayi += 1
                print(f"Keçid uğurludur! Ödəniş: {qiymet:.2f} AZN. Xoş gedişlər!")
                emeliyyatlar.append({
                    "tip": "Gediş", 
                    "mebleg": qiymet, 
                    "balans": balans, 
                    "endirim": endirim
                })
            elif 0.30 <= balans < qiymet and rejim == "Normal":
                print(f"Balans kifayət deyil ({balans:.2f} AZN).")
                cavab = input("Təcili keçid istifadə edilsin? (0.10 AZN borc yazılacaq) [h/y]: ")
                if cavab.lower() == 'h':
                    balans = 0 # Balans sıfırlanır
                    borc += 0.10
                    gedis_sayi += 1
                    print("Təcili keçid aktiv edildi. Xoş gedişlər!")
                    emeliyyatlar.append({
                        "tip": "Təcili Gediş", 
                        "mebleg": 0.30, 
                        "balans": 0.0, 
                        "endirim": 0.0
                    })
            else:
                print("Balans yetərsizdir. Zəhmət olmasa artırın.")

        elif secim == "4":
            try:
                n = int(input("Son neçə əməliyyatı görmək istəyirsiniz? "))
                son_emeliyyatlar = emeliyyatlar[-n:]
                print("\n--- SON ƏMƏLİYYATLAR ---")
                for e in reversed(son_emeliyyatlar):
                    print(f"Tip: {e['tip']} | Məbləğ: {e['mebleg']:.2f} | Endirim: {e['endirim']:.2f} | Balans: {e['balans']:.2f}")
            except ValueError:
                print("Xəta: Düzgün say daxil edin!")

        elif secim == "5":
            umi_odenis = sum(e['mebleg'] for e in emeliyyatlar if "Gediş" in e['tip'])
            umi_endirim = sum(e['endirim'] for e in emeliyyatlar)
            print("\n--- GÜNLÜK STATİSTİKA ---")
            print(f"Ümumi gediş sayı: {gedis_sayi}")
            print(f"Ümumi ödənilən məbləğ: {umi_odenis:.2f} AZN")
            print(f"Qazanılan cəmi endirim: {umi_endirim:.2f} AZN")
            print(f"Günlük artırılan cəmi məbləğ: {gunluk_artirma_cemi:.2f} AZN")

        elif secim == "6":
            print("\n1) Günlük artırma limitini dəyiş")
            print("2) Endirim rejimini dəyiş")
            p_secim = input("Seçiminiz: ")
            if p_secim == "1":
                new_limit = float(input("Yeni limit daxil edin: "))
                artirma_limiti = new_limit
                print(f"Limit dəyişdirildi: {artirma_limiti} AZN")
            elif p_secim == "2":
                print("Rejimlər: 1) Normal, 2) Tələbə, 3) Pensiyaçı")
                r_secim = input("Seçiminiz: ")
                if r_secim == "1": rejim = "Normal"
                elif r_secim == "2": rejim = "Telebe"
                elif r_secim == "3": rejim = "Pensiyaci"
                print(f"Rejim dəyişdirildi: {rejim}")

        elif secim == "0":
            print("Sistemdən çıxılır. Sağ olun!")
            break
        else:
            print("Yanlış seçim! Yenidən yoxlayın.")

# Proqramı başlat
metro_kart_simulyatoru()