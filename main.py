from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import Response
from gemini_service import GeminiService
import typing

app = FastAPI(title="Avatar Generator AI")
gemini = GeminiService()

@app.post("/crear-avatar")
async def crear_avatar(
    foto_rostro: UploadFile = File(...),
    genero: str = Form(...) # "hombre" o "mujer"
):
    try:
        content = await foto_rostro.read()
        avatar_bytes = await gemini.generate_initial_avatar(content, genero)
        
        return Response(content=avatar_bytes, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agregar-accesorios")
async def agregar_accesorios(
    avatar_base: UploadFile = File(...),
    accesorio1: UploadFile = File(...),
    accesorio2: typing.Optional[UploadFile] = File(None),
    accesorio3: typing.Optional[UploadFile] = File(None)
):
    try:
        # Leer avatar base
        base_content = await avatar_base.read()
        
        # Leer accesorios presentes
        acc_list = []
        for acc in [accesorio1, accesorio2, accesorio3]:
            if acc:
                content = await acc.read()
                acc_list.append(content)
        
        result_avatar = await gemini.modify_avatar_with_accessories(base_content, acc_list)
        
        return Response(content=result_avatar, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)