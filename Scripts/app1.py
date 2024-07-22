from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB connection
mongo_client = MongoClient('mongodb://127.0.0.1:27017')
db = mongo_client.bookstore
books_collection = db.books

# Helper function to convert MongoDB document to JSON
def book_to_json(book):
    book["_id"] = str(book["_id"])
    return book

# Add new book
@app.route('/book', methods=['POST'])
def add_book():
    data = request.json
    try:
        result = books_collection.insert_one(data)
        data["_id"] = result.inserted_id
        return jsonify(book_to_json(data)), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400

# Get all books
@app.route('/book', methods=['GET'])
def get_all_books():
    books = books_collection.find()
    result = [book_to_json(book) for book in books]
    return jsonify(result)

# Get book by ID
@app.route('/book/<id>', methods=['GET'])
def get_book_by_id(id):
    try:
        book = books_collection.find_one({"_id": ObjectId(id)})
        if book:
            return jsonify(book_to_json(book))
        else:
            return jsonify({"message": "Book not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 400

# Update book by ID
@app.route('/book/<id>', methods=['PUT'])
def update_book(id):
    data = request.json
    try:
        result = books_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if result.matched_count > 0:
            return jsonify({"message": "Book updated successfully"})
        else:
            return jsonify({"message": "Book not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 400

# Delete book by ID
@app.route('/book/<id>', methods=['DELETE'])
def delete_book_by_id(id):
    try:
        result = books_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count > 0:
            return jsonify({"message": "Book deleted successfully"})
        else:
            return jsonify({"message": "Book not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
