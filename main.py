from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fal_service import FalService
import typing

app = FastAPI(title="Avatar Fal.ai API")
fal_service = FalService()

@app.post("/crear-avatar")
async def crear_avatar(
    foto_rostro: UploadFile = File(...),
    genero: str = Form(...)
):
    try:
        content = await foto_rostro.read()
        url_generada = await fal_service.generate_initial_avatar(content, genero)
        return {"avatar_url": url_generada}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agregar-accesorios")
async def agregar_accesorios(
    avatar_url: str = Form(...), # Recibe la URL que devolvió el primer paso
    accesorio1: UploadFile = File(...),
    accesorio2: typing.Optional[UploadFile] = File(None),
    accesorio3: typing.Optional[UploadFile] = File(None)
):
    try:
        acc_list = []
        for acc in [accesorio1, accesorio2, accesorio3]:
            if acc:
                acc_list.append(await acc.read())
        
        # Nota: En una implementación real, procesaríamos las imágenes de accesorios 
        # para extraer sus características visuales.
        nueva_url = await fal_service.modify_avatar_with_accessories(avatar_url, acc_list)
        return {"avatar_modificado_url": nueva_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))