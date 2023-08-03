from flask import Blueprint, request, send_from_directory, jsonify
from os import getcwd, path, remove, makedirs

files = Blueprint("files", __name__)

PATH_FILES = getcwd() + "\\planificacion\\"


def create_folder_if_not_exists(folder_path):
    if not path.exists(folder_path):
        makedirs(folder_path)


@files.post("/upload")
def upload_file():
    try:
        file = request.files['file']
        ciclo = request.form.get('ciclo', '')
        folder = request.form.get('folder', '')

        ciclo_path = path.join(PATH_FILES, ciclo)
        create_folder_if_not_exists(ciclo_path)

        folder_path = path.join(ciclo_path, folder)
        create_folder_if_not_exists(folder_path)

        file.save(path.join(folder_path, file.filename))

        return jsonify({"ok": True, "status": 200, "data": None})
    except FileNotFoundError:
        return jsonify({"ok": False, "status": 500, "data": {"message" "Folder not foun"}}), 500


@files.get("/file/<string:name_file>")
def get_file(name_file):
    folder = request.args.get("folder", "")
    ciclo = request.args.get("ciclo", "")

    file_path = path.join(PATH_FILES + ciclo, folder, name_file)

    if not path.isfile(file_path):
        return jsonify({"ok": False, "status": 500, "data": {"message": "Archivo no encontrado"}}), 404

    try:
        return send_from_directory(path.join(PATH_FILES, ciclo, folder), path=name_file, as_attachment=False)
    except FileNotFoundError:
        raise FileNotFoundError


@files.get("/download/<string:name_file>")
def download_file(name_file):
    folder = request.args.get("folder", "")
    ciclo = request.args.get("ciclo", "")
    file_path = path.join(PATH_FILES + ciclo, folder, name_file)

    if not path.isfile(file_path):
        return jsonify({"ok": False, "status": 500, "data": {"message": "Archivo no encontrado"}}), 404
    return send_from_directory(path.join(PATH_FILES, ciclo, folder), path=name_file, as_attachment=True)


@files.delete('/delete')
def delete_file():
    filename = request.json.get('filename', '')
    folder = request.json.get('folder', '')
    ciclo = request.json.get('ciclo', '')

    file_path = path.join(PATH_FILES + ciclo, folder, filename)

    if not path.isfile(file_path):
        print(file_path)
        return jsonify({"ok": False, "status": 500, "data": {"message": "Archivo no encontrado"}}), 500
    else:
        try:
            remove(file_path)
            return jsonify({"ok": True, "status": 200, "data": None})
        except Exception as ex:
            return jsonify({"ok": False, "status": 500, "data": {"message": str(ex)}}), 500
