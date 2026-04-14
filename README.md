# 🚀 SeekSite: Local AI Website Builder

**Small Models, Big Designs.** 
SeekSite, küçük dil modellerini (4b, 8b, 12b, 20b) profesyonel birer web tasarımcısına dönüştüren, tamamen yerel (local) çalışan bir yapay zeka asistanıdır.

---

## 🌟 Neden SeekSite?

Geleneksel küçük modeller (SLM) genellikle tasarım yeteneğinden yoksundur; renkleri karıştırır, düzeni bozarlar. SeekSite, geliştirdiğimiz **"Design DNA Injection"** mimarisi ile bu sorunu kökten çözer.

### 🧬 Design DNA Engine
Modellere "hayal kurma" yükü bindirmek yerine, onlara önceden optimize edilmiş, modern ve responsive CSS bileşenleri (DNA) enjekte ediyoruz. Model sadece bu bileşenleri mantıklı bir sırayla birleştirir ve içeriği doldurur. Sonuç: **Gemini 1.5 Flash kalitesinde tasarımlar, yerel modellerle!**

---

## ✨ Temel Özellikler

- **🏠 %100 Yerel ve Gizli:** Ollama entegrasyonu sayesinde verileriniz asla bilgisayarınızdan çıkmaz. İnternet bağlantısı gerekmez.
- **⚡ Küçük Model Optimizasyonu:** Llama 3, Mistral, Gemma veya Phi-3 gibi 4b-12b arası modellerle profesyonel sonuçlar.
- **🔄 Auto-Continuation:** Kod üretimi yarıda kesilirse, sistem otomatik olarak fark eder ve kaldığı yerden devam eder.
- **🎨 Dinamik Tasarım:** Kullanıcının isteğine göre otomatik renk paleti ve tasarım dili seçimi.
- **🛠️ Canlı Önizleme Desteği:** Üretilen kodları anında tarayıcıda görüntüleme ve düzenleme.

---

## 🛠️ Kurulum

### 1. Gereksinimler
- Python 3.10+
- [Ollama](https://ollama.com/) (Yerel modelleri çalıştırmak için)

### 2. Adımlar
```bash
# Depoyu klonlayın
git clone https://github.com/kullaniciadi/seeksite.git
cd seeksite

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Ollama'da bir model indirin (Örn: Llama 3)
ollama run llama3

# Uygulamayı başlatın
python app.py
```

Uygulama başlatıldıktan sonra tarayıcınızda `http://localhost:5000` adresine giderek kendi web sitelerinizi üretmeye başlayabilirsiniz!

---


## 🤝 Katkıda Bulunun

SeekSite açık kaynaklı bir projedir. Her türlü katkı, hata bildirimi ve özellik önerisi için Pull Request göndermekten çekinmeyin!

---

**Geliştiren:** [Emir Özcan/Gazi-AI]
*Powered by Ollama & Design DNA Architecture*
