from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB connection
mongo_url = 'mongodb://127.0.0.1:27017/'  # Update to your MongoDB URL if needed
client = MongoClient(mongo_url)
db = client['bookstore']
books_collection = db['books']

# Convert MongoDB documents to JSON
def book_to_json(book):
    book['_id'] = str(book['_id'])
    return book

@app.route('/book', methods=['POST'])
def add_book():
    data = request.json
    try:
        result = books_collection.insert_one(data)
        data["_id"] = str(result.inserted_id)
        return jsonify(book_to_json(data)), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@app.route('/books', methods=['GET'])
def get_books():
    try:
        books = list(books_collection.find())
        books = [book_to_json(book) for book in books]
        return jsonify(books), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/book/<id>', methods=['PUT'])
def update_book(id):
    data = request.json
    try:
        if not ObjectId.is_valid(id):
            return jsonify({"message": "Invalid ID format"}), 400
        result = books_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": data}
        )
        if result.matched_count == 0:
            return jsonify({"message": "Book not found"}), 404
        updated_book = books_collection.find_one({"_id": ObjectId(id)})
        return jsonify(book_to_json(updated_book)), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@app.route('/book/<id>', methods=['DELETE'])
def delete_book(id):
    try:
        if not ObjectId.is_valid(id):
            return jsonify({"message": "Invalid ID format"}), 400
        result = books_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            return jsonify({"message": "Book not found"}), 404
        return jsonify({"message": "Book deleted"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
