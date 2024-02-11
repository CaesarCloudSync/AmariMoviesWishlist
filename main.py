import os
import io
import json
import base64
import hashlib
import asyncio 
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Header,Request,File, UploadFile,status,Form
from fastapi.responses import StreamingResponse,FileResponse,Response
from typing import Dict,List,Any,Union
from CaesarSQLDB.caesarcrud import CaesarCRUD
from CaesarSQLDB.caesarhash import CaesarHash
from fastapi.responses import StreamingResponse
from fastapi import WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from CaesarJWT.caesarjwt import CaesarJWT
from CaesarSQLDB.caesar_create_tables import CaesarCreateTables
import requests
load_dotenv(".env")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


caesarcrud = CaesarCRUD()
maturityjwt = CaesarJWT(caesarcrud)
caesarcreatetables = CaesarCreateTables()
caesarcreatetables.create(caesarcrud)
JSONObject = Dict[Any, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]

def stream_subtitle(url):
    for chunk in requests.get(url,stream=True):
        yield chunk


@app.get('/')# GET # allow all origins all methods.
async def index():
    return "Welcome to CaesarAIWorld!"
@app.post('/addwishlist')# GET # allow all origins all methods.
async def addwishlist(data: JSONStructure = None):
    try:
        data = dict(data)
        movie = data["movie"]
        themoviedbid = data["themoviedbid"]
        broadcasttype = data["type"]
        movie_exists = caesarcrud.check_exists(("*"),"amarimovieswishlist",f"themoviedbid = {themoviedbid}")
        if movie_exists:
            return {"error":"already exists"}
        else:
            res = caesarcrud.post_data(("movie","themoviedbid","broadcasttype"),(movie,themoviedbid,broadcasttype),"amarimovieswishlist")
            return {"message":"added to wishlist."}
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}
@app.get('/getsubtitles')# GET # allow all origins all methods.
async def getsubtitles(url:str):
    try:
       return StreamingResponse(stream_subtitle(url),status_code=status.HTTP_200_OK,
                                media_type="text/vtt") #Response(buffer.getvalue(), headers=headers, media_type='video/mp4')
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}

@app.get('/checkwishlist')# GET # allow all origins all methods.
async def checkwishlist(themoviedbid:str):
    try:
        movie_exists = caesarcrud.check_exists(("*"),"amarimovieswishlist",f"themoviedbid = {themoviedbid}")
        if movie_exists:
            return {"result":"true"}
        else:
            return {"result":"false"}
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}

@app.get('/getallwishlist')# GET # allow all origins all methods.
async def getallwishlist():
    try:
        movie_exists = caesarcrud.check_exists(("*"),"amarimovieswishlist")
        if movie_exists:
            res = caesarcrud.get_data(("movie","themoviedbid","broadcasttype"),"amarimovieswishlist")
            return {"message":res}
        else:
            return {"error":"does not exist."}
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}

@app.delete('/deletefromwishlist')# GET # allow all origins all methods.
async def deletefromwishlist(themoviedbid:str):
    try:
        movie_exists = caesarcrud.check_exists(("*"),"amarimovieswishlist",f"themoviedbid = {themoviedbid}")
        if movie_exists:
            res = caesarcrud.delete_data("amarimovieswishlist",f"themoviedbid = {themoviedbid}")
            return {"message":"removed from the wish list"}
        else:
            return {"error":"does not exist."}
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}



if __name__ == "__main__":
    uvicorn.run("main:app",port=8090,log_level="info")
    #uvicorn.run()
    #asyncio.run(main())