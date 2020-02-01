from flask import Flask, jsonify, request
from random import randint

import pathlib

app = Flask(__name__)


_extensions_icons=['.pdf','.as','.c','.iso','.htm','.html','.xml','.xsl','.cf','.cpp','.cs','.sql','.xls','.xlsx','.h','.crt','.pem','.cer','.php','.jpg','.jpeg','.png','.gif','.bmp','.ppt','.pptx','.rb','.text','.txt','.md','.log','.htaccess','.doc','.docx','.zip','.gz','.tar','.rar','.js','.css','.fla']


def list_directory(directory): 
    children = []
    for p in pathlib.Path(directory).glob('*'):
        if p.is_dir():
            icon = "folder"
        else:
            if p.suffix in _extensions_icons:
                icon = "file file-{}".format(p.suffix.replace('.', ''))
            else:
                icon = "file"
        children.append({
            "children": p.is_dir(),
            "icon": icon,
            "id": str(p.absolute()),
            "text": str(p.name)
        })
    return children


@app.route('/get')
def get():
    if request.args and request.args.get('id') != '#':
        return jsonify(list_directory(request.args.get('id')))

    return jsonify([{
        "icon": "folder",
        "id": "/",
        "state": {
            "disabled": True,
            "opened": True
        },
        "text": "root",
        "children": list_directory('/')
    }])


@app.route('/info')
def info():
    _id = request.args.get('id')

    if not _id:
        return jsonify({"error": True, "message": "Could not load information of given path."})
    
    _file = pathlib.Path(_id)

    if not _file.exists():
        return jsonify({"error": True, "message": "Given directory does not exists."})
    
    _file_stats = _file.stat()

    return jsonify({
        "st_mode": _file_stats.st_mode,
        "st_ino": _file_stats.st_ino,
        "st_dev": _file_stats.st_dev,
        "st_nlink": _file_stats.st_nlink,
        "st_uid": _file_stats.st_uid,
        "st_gid": _file_stats.st_gid,
        "st_size": _file_stats.st_size,
        "st_atime": _file_stats.st_atime,
        "st_mtime": _file_stats.st_mtime,
        "st_ctime": _file_stats.st_ctime,
    })


# disable CORS :-D
@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = '*'
    return response


app.run(debug=True)
