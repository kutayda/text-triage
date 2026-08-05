# text-triage

Ham müşteri mesajlarını otomatik olarak sınıflandırıp özetleyen bir komut satırı aracı. Bir CSV dosyası dolusu mesajı alır, her birini "şikayet / soru / övgü" olarak etiketler, tek cümlelik özetini çıkarır ve sonucu düzenli bir CSV'ye yazar.

## Ne işe yarar?

Gelen müşteri mesajlarını elle okuyup kategorilere ayırmak zaman alır. Bu araç o işi otomatikleştirir: dağınık, yapısız mesajlar girer; sınıflandırılmış, özetlenmiş, yapılandırılmış veri çıkar.

## Özellikler

- CSV'den toplu mesaj işleme
- LLM ile otomatik sınıflandırma ve özetleme
- Sağlayıcı seçilebilir (Gemini / Groq) — komut satırından değiştirilebilir
- Rate limit'e karşı otomatik retry / backoff
- Sonunda özet istatistik (kaç şikayet, kaç soru, kaç övgü)

## Kurulum

​```bash
uv sync
​```

`.env.example` dosyasını `.env` olarak kopyala ve kendi API key'lerini gir:

​```
GEMINI_API_KEY=...
GROQ_API_KEY=...
​```

## Kullanım

​```bash
# Varsayılan ayarlarla
uv run triage.py

# Sağlayıcı seçerek
uv run triage.py --provider groq

# Farklı girdi/çıktı dosyasıyla
uv run triage.py --input mesajlar.csv --output sonuc.csv
​```

## Tasarım kararları

### Sağlayıcı değiştirilebilir mimari

Bu proje kişisel bir öğrenme projesi olduğu için ücretli bir LLM kullanmak istemedim; Gemini ve Groq'un ücretsiz katmanlarını tercih ettim. Ancak ücretsiz katmanların kotası kısıtlı — tek bir sağlayıcıya bağlı kalsaydım, kota dolduğunda proje tamamen tıkanırdı. Bu yüzden kodu tek bir sağlayıcıya sabitlemek yerine sağlayıcı-değiştirilebilir tasarladım: sağlayıcı bilgisi tek yerde tanımlı ve `--provider` bayrağıyla dışarıdan seçiliyor. Böylece Gemini'nin günlük kotası dolduğunda, kodda hiçbir değişiklik yapmadan `--provider groq` ile Groq'a geçilebiliyor.

### Rate limit'e karşı retry/backoff

Model ücretsiz katmanda çalıştığından, çağrılar arka arkaya gidince rate limit'e (429) takıldım. Kod hemen çökmesin diye artan sürelerle (1sn, 2sn, 4sn) birkaç kez bekleyip tekrar deniyor. Denemeler tükenirse sessizce kapanmak yerine `Max retries exceeded` hatası verip duruyor. Böylece geçici bir tıkanma yüzünden bütün işin çökmesi engellenmiş oluyor.

### Çıktı normalleştirme

Model her zaman tutarlı bir çıktı vermiyordu — kategori bazen büyük harfle (`Şikayet`), bazen küçük harfle (`şikayet`), bazen de baştan/sondan boşluklu geliyordu. Bu tutarsızlığı `.lower().strip()` ile normalleştirdim. Bu önemliydi çünkü sonda kaç şikayet/soru/övgü olduğunu sayarken, tutarsız kategoriler aynı grubu farklı sayar ve istatistiği bozardı.

## Kullanılan teknolojiler

Python, OpenAI-uyumlu API (Gemini & Groq), csv, argparse