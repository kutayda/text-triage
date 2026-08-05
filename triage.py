from main import ask    
import csv
import time 
import argparse

def classify(text,provider):
    prompt = f"Aşağıda müşteri mesajını şu üç kategoriden birine ayır:şikayet, soru, övgü. Sadece kategori kelimesini yaz, başka hiçbir şey ekleme. Mesaj: {text}"
    result = ask(provider, prompt)   
    result = result.lower().strip()
    return result

def summarize(text,provider):
    prompt = f"Düşünme sürecini, açıklama veya 'THOUGHTS' gibi bir şey yazma. Doğrudan tek cümlelik özeti ver. Mesaj: {text}"
    result = ask(provider, prompt)   
    return result

parser = argparse.ArgumentParser(description="Müşteri mesajlarını sınıflandırır ve özetler.")
parser.add_argument("--input", default = "emails.csv", help = "Girdi CSV dosyası")
parser.add_argument("--output", default = "results.csv", help = "Çıktı CSV dosyası")
parser.add_argument("--provider", default = "groq", help = "LLM sağlayıcısı: gemini veya groq")

args = argparse.Namespace()
args = parser.parse_args()

results = []
with open(args.input, encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        text = row["text"]
        category = classify(text, args.provider)   
        summary = summarize(text, args.provider)
        results.append({
            "id": row["id"],
            "text": text,
            "category": category,
            "summary": summary
        })
        time.sleep(5)
for r in results:
    print(r["id"], "->", r["category"], "->", r["summary"])


with open(args.output, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "text", "category", "summary"])
    writer.writeheader()
    writer.writerows(results)
    
    
sikayet = 0
soru = 0
ovgu = 0

for r in results:
    if r["category"] == "şikayet":
        sikayet = sikayet + 1
    elif r["category"] == "soru":
        soru = soru + 1
    elif r["category"] == "övgü":
        ovgu = ovgu + 1
        
print(f"{len(results)} mesaj: {sikayet} şikayet, {soru} soru, {ovgu} övgü")



