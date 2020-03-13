from bottle import route
from bottle import run
from bottle import request
from bottle import HTTPError

import my_06

@route("/albums/<artist>")
def albums(artist):
    i=0
    albums_list = my_06.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        
        album_names = [album.album for album in albums_list]
        result = "СПИСОК АЛЬБОМОВ ИСПОЛНИТЕЛЯ: {}:<br>&#10004".format(artist)
        result += "<br>&#10004".join(album_names)
        print(i)
    return result


@route("/albums", method="POST")
def create_album():

    try:
        year = request.forms.get("year")
    except ValueError:
        return HTTPError(400, "Указан некорректный год альбома")
    finally:
         print("год не указана или указан некорректно")

    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album_name = request.forms.get("album")

    try:
        year = int(year)
    except ValueError:
        return HTTPError(400, "Указан некорректный год альбома")
    finally:
         print("год не указана или указан некорректно")
    

    try:
        new_album = my_06.save(year, artist, genre, album_name)
    except AssertionError as err:
        result = HTTPError(400, str(err))
    except my_06.AlreadyExists as err:
        result = HTTPError(409, str(err))
    else:    
        print("New #{} album successfully saved".format(new_album.id))
        result = "Альбом #{} успешно сохранен".format(new_album.id)
    return result
    

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
