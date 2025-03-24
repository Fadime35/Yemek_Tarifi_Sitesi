import streamlit as st
from yemekler import kategori_sec, giris_yap, kullanici_kayit, tarif_ekle, tarif_guncelleme, tarif_sil, tarifleri_getir, tum_tarifleri_getir



if "kullanici_id" not in st.session_state:
    st.session_state.kullanici_id = None 
if "kullanici_adi" not in st.session_state:
    st.session_state.kullanici_adi = None 

# Menü seçeneklerini tanımlama
menu = ["Giriş Yap", "Kayıt Ol", "Kategori Seç", "Tarif Ekle", "Tarif Güncelle", "Tarif Sil", "Tüm Tarifler"]
secim = st.sidebar.selectbox("Menü", menu) 

# Giriş Yap işlemi
if secim == "Giriş Yap":
    st.title("Giriş Yap")
    kullanici_adi = st.text_input("Kullanıcı Adı")
    e_mail = st.text_input("E-mail")
    sifre = st.text_input("Şifre", type="password")
    sifre2 = st.text_input("Şifre2", type="password")

    if st.button("Giriş Yap"):
        kullanici_id = giris_yap(kullanici_adi, e_mail, sifre) 
        if kullanici_id:
            st.session_state.kullanici_id = kullanici_id  
            st.session_state.kullanici_adi= kullanici_adi  
            st.success("Giriş Başarılı!")
            st.write(f"Hoşgeldin, {st.session_state.kullanici_adi}!") 
        else:
            st.error("Giriş Başarısız! Lütfen bilgilerinizi kontrol edin.")

# Kayıt Ol işlemi
elif secim == "Kayıt Ol":
    st.title("Kayıt Ol")  
    kullanici_adi = st.text_input("Kullanıcı Adı")
    e_mail = st.text_input("E-mail")
    sifre = st.text_input("Şifre", type="password")
    
    if st.button("Kayıt Ol"): 
        if kullanici_kayit(e_mail, sifre, kullanici_adi):
            st.success("Kayıt Başarılı! Artık giriş yapabilirsiniz.")
        else:
            st.error("Kayıt Başarısız! E-mail adresi zaten kullanımda olabilir.")



# Kategori seçme ve tarifleri listeleme
elif secim == "Kategori Seç":
    st.title("Yemek Tarifi Kategorileri")

    if st.session_state.kullanici_id is None:
        st.warning("Lütfen giriş yapın!")
    else:
        st.write(f"Hoşgeldin, {st.session_state.kullanici_adi}!")  
        kullanici_id = st.session_state.kullanici_id  

        # Kategorileri getir
        kategoriler = kategori_sec()  

        if kategoriler:
            
            kategori_secenekleri = {kategori["adi"]: kategori["id"] for kategori in kategoriler}
            secilen_kategori_adi = st.selectbox("Bir kategori seçin:", list(kategori_secenekleri.keys()))

            if secilen_kategori_adi:
                st.success(f"Seçilen Kategori: {secilen_kategori_adi}")
                kategori_id = kategori_secenekleri[secilen_kategori_adi]

                tarifler = tarifleri_getir(kullanici_id, kategori_id)

                if tarifler:
                    # Tarifleri listele
                    for tarif in tarifler:
                        st.subheader(f"{tarif['tarif_adi']}") # Tarifin adını büyük bir başlık olarak ekrana yazdırır.
                        st.write(f"Kişi Sayısı: {tarif['kisi_sayisi']}")
                        st.write(f"Tarif: {tarif['hazirlanis']}")
                        if tarif['gorsel']:
                            st.image(tarif['gorsel'], use_container_width=True)
                        st.markdown("---")
                else: 
                    st.warning(f"'{secilen_kategori_adi}' kategorisinde tarif bulunmamaktadır.")
        else:
            st.warning("Henüz kategori bulunmamaktadır. Veritabanını kontrol edin.")


# Tarif Ekle işlemi
elif secim == "Tarif Ekle":
    if st.session_state.kullanici_id:
        st.title("Yeni Tarif Ekle")
        kategoriler = kategori_sec()

        if kategoriler:
            kategori = st.selectbox("Bir kategori seçin:", [kategori['adi'] for kategori in kategoriler])
            tarif_adi = st.text_input("Tarif Adı")
            hazirlanis = st.text_area("Hazırlanış")
            kisi_sayisi = st.number_input("Kişi Sayısı", min_value=1, step=1)
            gorsel_url = st.text_input("Görsel URL'sini Girin")

            if gorsel_url:
                st.image(gorsel_url, use_container_width=True)

            if st.button("Tarifi Ekle"):
                try:
                    tarif_ekle(kategori, tarif_adi, hazirlanis, kisi_sayisi, gorsel_url, st.session_state.kullanici_id)
                    st.success(f"'{tarif_adi}' tarifi başarıyla eklendi!")
                except Exception as e:
                    st.error(f"Hata: {e}")
        else:
            st.warning("Tarif eklemek için önce kategori eklemelisiniz.")
    else:
        st.error("Tarif eklemek için giriş yapmalısınız!")

# Tarif Güncelle işlemi
elif secim == "Tarif Güncelle":
    if st.session_state.kullanici_id:
        st.title("Tarif Güncelle")
        tarif_adi = st.text_input("Güncellenecek Tarif Adı")
        yeni_tarif_adi = st.text_input("Yeni Tarif Adı (isteğe bağlı)")
        yeni_hazirlanis = st.text_area("Yeni Hazırlanış (isteğe bağlı)")
        yeni_kisi_sayisi = st.number_input("Yeni Kişi Sayısı (isteğe bağlı)", min_value=1, step=1)
        yeni_gorsel = st.text_input("Yeni Görsel URL (isteğe bağlı)")
        
        if st.button("Tarifi Güncelle"):
            try:
                # Tarif adını güncelleme
                tarif_guncelleme(tarif_adi, st.session_state.kullanici_id, yeni_tarif_adi, yeni_hazirlanis, yeni_kisi_sayisi, yeni_gorsel)
                st.success(f"'{tarif_adi}' başarıyla güncellendi!")
            except Exception as e:
                st.error(f"Hata: {e}")
    else:
        st.error("Tarif güncellemek için giriş yapmalısınız!")

# Tarif Sil işlemi
elif secim == "Tarif Sil":
    if st.session_state.kullanici_id:
        st.title("Tarif Sil")
        tarif_adi = st.text_input("Silmek İstediğiniz Tarif Adı")

        if st.button("Tarifi Sil"):
            try:
                tarif_sil(tarif_adi, st.session_state.kullanici_id)
                st.success(f"'{tarif_adi}' tarifi başarıyla silindi!")
            except Exception as e:
                st.error(f"Hata: {e}")
    else:
        st.error("Tarif silmek için giriş yapmalısınız!")


# Tüm Tarifler işlemi
elif secim == "Tüm Tarifler":
    st.title("Tüm Tarifler")   
    tarifler = tum_tarifleri_getir()

    if tarifler:
        for tarif in tarifler:
            st.subheader(f"{tarif['tarif_adi']}")
            st.write(f"Kategori: {tarif['kategori_adi']}")
            st.write(f"Kullanıcı: {tarif['kullanici_adi']}")
            st.write(f"Kişi Sayısı: {tarif['kisi_sayisi']}")
            st.write(f"Tarif: {tarif['hazirlanis']}")
            if tarif['gorsel']:
                st.image(tarif['gorsel'], use_container_width=True)
            st.markdown("---") 
    else:
        st.warning("Henüz hiç tarif eklenmemiş.")



