import mysql.connector

# Veritabanı bağlantısı 
def veritabani_baglantisi():
    conn = mysql.connector.connect(
        host="localhost",  
        user="root",  
        port=3306,
        password="fdm3535",  
        database="yemek_tarifi"  
    )
    return conn


# Kullanıcı girişi fonksiyonu
def giris_yap(kullanici_adi, e_mail, sifre):
    conn = veritabani_baglantisi()
    cursor = conn.cursor()

    query = "SELECT kullanici_id FROM kullanici_bilgileri WHERE kullanici_adi = %s AND e_mail = %s AND sifre = %s"
    cursor.execute(query, (kullanici_adi, e_mail, sifre))
    
    kullanici = cursor.fetchone()
    conn.close()

   
    if kullanici:
        return kullanici[0]  
    else:
        return None


# Kullanıcı kaydı fonksiyonu
def kullanici_kayit(e_mail, sifre, kullanici_adi):
    conn = veritabani_baglantisi()
    cursor =conn.cursor()

    query = "SELECT * FROM kullanici_bilgileri WHERE e_mail = %s"
    cursor.execute(query, (e_mail,))
    
    if cursor.fetchone():
        conn.close()
        return False  

    # Kullanıcı bilgilerini veritabanına ekleyen sorgu
    query = "INSERT INTO kullanici_bilgileri (e_mail, sifre, kullanici_adi) VALUES (%s, %s, %s)"
    cursor.execute(query, (e_mail, sifre, kullanici_adi))
    conn.commit() 
    conn.close()
    
    return True 


# Kategori listeleme fonksiyonu
def kategori_sec():  
    try:             
        conn = veritabani_baglantisi()
        cursor = conn.cursor()

        query = "SELECT kategori_id, kategori_adi FROM kategoriler ORDER BY kategori_adi ASC"
        cursor.execute(query)
        kategoriler = cursor.fetchall()

        return [{"id": kategori[0], "adi": kategori[1]} for kategori in kategoriler if kategori]
     
    except Exception as e:
        print(f"Kategoriler alınırken hata oluştu: {e}")
        return []
    finally:
        conn.close()


# Kullanıcıya özel tarifleri listeleme
def tarifleri_getir(kullanici_id, kategori_id=None):
    try:
        conn = veritabani_baglantisi()
        cursor = conn.cursor()

        if kategori_id: 
            query = """
                SELECT tarif_id, tarif_adi, hazirlanis, kisi_sayisi, gorsel
                FROM tarifler
                WHERE kategori_id = %s AND kullanici_id = %s
            """
            cursor.execute(query, (kategori_id, kullanici_id))
        else:  
            query = """
                SELECT tarif_id, tarif_adi, hazirlanis, kisi_sayisi, gorsel
                FROM tarifler
                WHERE kullanici_id = %s
            """
            cursor.execute(query, (kullanici_id,))
        tarifler = cursor.fetchall()


        return [
            {
                "tarif_id": tarif[0],
                "tarif_adi": tarif[1],
                "hazirlanis": tarif[2],
                "kisi_sayisi": tarif[3],
                "gorsel": tarif[4],
            }
            for tarif in tarifler
        ]
    except Exception as e:
        print(f"Tarifler alınırken hata oluştu: {e}")
        return []
    finally:
        conn.close()



# Kullanıcıya özel tarif ekleme
def tarif_ekle(kategori_adi, tarif_adi, hazirlanis, kisi_sayisi, gorsel, kullanici_id):
    conn = veritabani_baglantisi()
    cursor = conn.cursor()
    
    query_kategori = "SELECT kategori_id FROM kategoriler WHERE kategori_adi = %s"
    cursor.execute(query_kategori, (kategori_adi,))
    kategori_id = cursor.fetchone()
    
    if kategori_id:
        kategori_id = kategori_id[0]
    else:
        raise ValueError("Geçersiz kategori adı!")
    
    query_tarif = """
        INSERT INTO tarifler (tarif_adi, hazirlanis, kisi_sayisi, gorsel, kategori_id, kullanici_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query_tarif, (tarif_adi, hazirlanis, kisi_sayisi, gorsel, kategori_id, kullanici_id))
    conn.commit()
    conn.close()




def tarif_guncelleme(tarif_adi, kullanici_id, yeni_tarif_adi=None, yeni_hazirlanis=None, yeni_kisi_sayisi=None, yeni_gorsel=None):
    # Mevcut tarifi getir
    conn = veritabani_baglantisi()
    cursor = conn.cursor()
    sorgu_getir = "SELECT tarif_adi, hazirlanis, kisi_sayisi, gorsel FROM tarifler WHERE tarif_adi = %s AND kullanici_id = %s"
    cursor.execute(sorgu_getir, (tarif_adi, kullanici_id))
    mevcut_tarif = cursor.fetchone()

    if mevcut_tarif is None:
        print("Tarif bulunamadı! Lütfen doğru bir tarif adı girin.")
        conn.close()
        return


    print("Mevcut Tarif Bilgileri:")
    print(f"Tarif Adı: {mevcut_tarif[0]}")
    print(f"Hazırlanış: {mevcut_tarif[1]}")
    print(f"Kişi Sayısı: {mevcut_tarif[2]}")
    print(f"Görsel: {mevcut_tarif[3]}")

    sorgu_guncelle = "UPDATE tarifler SET "
    degerler = []

    if yeni_tarif_adi:
        sorgu_guncelle += "tarif_adi = %s, "
        degerler.append(yeni_tarif_adi)
    else:
        yeni_tarif_adi = mevcut_tarif[0]  

    if yeni_hazirlanis:
        sorgu_guncelle += "hazirlanis = %s, "
        degerler.append(yeni_hazirlanis)
    else:
        yeni_hazirlanis = mevcut_tarif[1] 

    if yeni_kisi_sayisi:
        sorgu_guncelle += "kisi_sayisi = %s, "
        degerler.append(yeni_kisi_sayisi)
    else:
        yeni_kisi_sayisi = mevcut_tarif[2] 

    if yeni_gorsel:
        sorgu_guncelle += "gorsel = %s, "
        degerler.append(yeni_gorsel)
    else:
        yeni_gorsel = mevcut_tarif[3]  

    
    sorgu_guncelle = sorgu_guncelle.rstrip(", ")
    sorgu_guncelle += " WHERE tarif_adi = %s AND kullanici_id = %s"

    
    degerler.extend([tarif_adi, kullanici_id])

    cursor.execute(sorgu_guncelle, tuple(degerler))
    conn.commit()
    conn.close()

    print("Tarif başarıyla güncellendi!")

# Tarif silme fonksiyonu
def tarif_sil(tarif_adi, kullanici_id):
    conn = veritabani_baglantisi()
    cursor = conn.cursor()

    sorgu = "DELETE FROM tarifler WHERE tarif_adi = %s AND kullanici_id = %s"
    cursor.execute(sorgu, (tarif_adi, kullanici_id))
    conn.commit()
    conn.close()



# Tüm tarifleri getirme fonksiyonu
def tum_tarifleri_getir():
    try:
        conn = veritabani_baglantisi()
        cursor = conn.cursor()

        
        query = """
        SELECT 
        tarifler.tarif_id, 
        tarifler.tarif_adi, 
        tarifler.hazirlanis, 
        tarifler.kisi_sayisi, 
        tarifler.gorsel, 
        kategoriler.kategori_adi, 
        kullanici_bilgileri.kullanici_adi
        FROM tarifler
        JOIN kategoriler ON tarifler.kategori_id = kategoriler.kategori_id
        JOIN kullanici_bilgileri ON tarifler.kullanici_id = kullanici_bilgileri.kullanici_id;

        """
        cursor.execute(query)
        tarifler = cursor.fetchall()

        return [
            {
                "tarif_id": tarif[0],
                "tarif_adi": tarif[1],
                "hazirlanis": tarif[2],
                "kisi_sayisi": tarif[3],
                "gorsel": tarif[4],
                "kategori_adi": tarif[5],
                "kullanici_adi": tarif[6]
            }
            for tarif in tarifler
        ]
    except Exception as e:
        print(f"Tarifler alınırken hata oluştu: {e}")
        return []
    finally:
        conn.close()
