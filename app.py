from flask import Flask, request, jsonify

app = Flask(__name__)

notes = []


@app.route("/")
def index():
    return jsonify({"message": "Notes API is running", "version": "1.0.0"})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/notes", methods=["GET"])
def get_notes():
    return jsonify({"notes": notes, "count": len(notes)})


@app.route("/notes", methods=["POST"])
def create_note():
    data = request.get_json()

    if not data or "content" not in data:
        return jsonify({"error": "Field 'content' is required"}), 400

    content = data["content"].strip()
    if not content:
        return jsonify({"error": "Content cannot be empty"}), 400

    note = {"id": len(notes) + 1, "content": content}
    notes.append(note)
    return jsonify(note), 201


@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    global notes
    original_count = len(notes)
    notes = [n for n in notes if n["id"] != note_id]

    if len(notes) == original_count:
        return jsonify({"error": "Note not found"}), 404

    return jsonify({"message": f"Note {note_id} deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
