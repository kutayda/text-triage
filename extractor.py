from pydantic import BaseModel
from main import get_client
import csv
import time
import argparse

  
class JobPosting(BaseModel):
    title: str
    location: str
    abilities: list[str]
    salary: str | None = None
    
def extract(text,provider):
    client, model = get_client(provider)
    completion = client.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": "Verilen iş ilanı metnindeki bilgileri çıkar."},
            {"role":"user", "content": text}
        ],
        response_format =JobPosting,
    )
    return completion.choices[0].message.parsed

results = []
with open("jobs.csv",encoding="utf-8",newline="") as f:
    reader= csv.DictReader(f)
    for row in reader:
        text = row["raw_text"]
        sonuc = extract(text, "groq")
        results.append(sonuc)
        time.sleep(5)
for r in results:
    print(r)
        


cv = JobPosting(title= "Software Developer", location= "Ankara", abilities= ["Python", "Java", "Flutter"], salary= '45.000-55.000 TL')

bad_cv = JobPosting(title= "Software Developer", location= "Ankara", abilities= ["Python", "Java", "Flutter"]) 

sonuc = extract("Aranıyor: Junior Frontend Developer. React ve TypeScript bilen, İstanbul ofisimizde tam zamanlı çalışacak. Maaş 45.000-55.000 TL. En az 1 yıl deneyim.", "groq")
print(sonuc)