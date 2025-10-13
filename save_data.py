from app.npl_utils import analyze_sentiment
from pymongo import MongoClient, InsertOne
import csv
from itertools import islice
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGO_URI)
db = client["restaurant_reviews"]

restaurants_collection = db["restaurants"]
reviews_collection = db["reviews"]

csv_path = "reviews.csv"
restaurant_ids = {}
review_operations = []
batch_size = 100
errores = []

positive_count = reviews_collection.count_documents({"sentiment": "positive"})
negative_count = reviews_collection.count_documents({"sentiment": "negative"})

print(f"Positive reviews: {positive_count}")
print(f"Negative reviews: {negative_count}")

# with open(csv_path, mode="r", encoding="utf-8") as file:
#     reader = csv.DictReader(file)
#     for idx, row in enumerate(reader, start=1):
#         try:
#             name = row["business_name"].strip()
#             text = row["text"].strip()
#             author = row.get("author_name", "").strip()
#             rating = row.get("rating", "").strip()

#             # Insertar restaurante si es nuevo
#             if name not in restaurant_ids:
#                 rest_doc = {
#                     "name": name,
#                     "description": "Imported from reviews CSV."
#                 }
#                 result = restaurants_collection.insert_one(rest_doc)
#                 restaurant_ids[name] = result.inserted_id

#             # Crear documento de review
#             review_doc = {
#                 "restaurant_id": restaurant_ids[name],
#                 "business_name": name,
#                 "author_name": author,
#                 "text": text,
#                 "rating": float(rating) if rating else None,
#                 "sentiment": analyze_sentiment(text),
#                 "timestamp": datetime.utcnow()
#             }

#             review_operations.append(InsertOne(review_doc))

#             # Insertar en lote cada `batch_size` reviews
#             if len(review_operations) >= batch_size:
#                 reviews_collection.bulk_write(review_operations)
#                 review_operations.clear()

#         except Exception as e:
#             errores.append((idx, row.get("business_name", "N/A"), str(e)))

# # Insertar cualquier remanente
# if review_operations:
#     try:
#         reviews_collection.bulk_write(review_operations)
#     except Exception as e:
#         errores.append(("final_batch", "N/A", str(e)))

# # --- Resumen ---
# print(f"✔️ Restaurantes insertados: {len(restaurant_ids)}")
# print(f"📝 Reviews insertadas: ~{len(reader) - len(errores)}")
# print(f"⚠️ Reviews con error: {len(errores)}")

# # Mostrar errores (si hay)
# for i, name, err in errores[:5]:  # solo los 5 primeros
#     print(f"[Error línea {i}] Restaurante: {name} → {err}")