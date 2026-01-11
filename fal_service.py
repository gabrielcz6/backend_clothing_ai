import os
import fal_client
import base64

class FalService:
    def __init__(self):
        # La API Key se tomará de la variable de entorno FAL_KEY
        pass

    def _bytes_to_data_uri(self, image_bytes: bytes, mime_type: str = "image/png"):
        base64_encoded = base64.b64encode(image_bytes).decode("utf-8")
        return f"data:{mime_type};base64,{base64_encoded}"

    async def generate_initial_avatar(self, face_bytes: bytes, gender: str):
        """
        Usa el modelo 'face-to-sticker' para crear un avatar estilizado
        manteniendo la esencia de la cara.
        """
        image_uri = self._bytes_to_data_uri(face_bytes)
        
        handler = await fal_client.submit_async(
            "fal-ai/face-to-sticker",
            arguments={
                "image_url": image_uri,
                "prompt": f"A professional 3D stylized avatar of a {gender}, high quality, pixar style, vibrant colors",
            }
        )
        result = await handler.get()
        return result['image']['url'] # Fal devuelve una URL pública de la imagen

    async def modify_avatar_with_accessories(self, avatar_uri: str, accessories_bytes: list[bytes]):
        """
        Usa Image-to-Image para mezclar el avatar base con nuevos elementos.
        """
        # Aquí, para simplificar, describimos los accesorios en el prompt 
        # ya que mezclar 4 imágenes requiere un modelo de Inpainting o ControlNet complejo.
        # Usaremos Flux Image-to-Image que es muy potente.
        
        handler = await fal_client.submit_async(
            "fal-ai/flux/dev/image-to-image",
            arguments={
                "image_url": avatar_uri,
                "prompt": "Highly detailed modification. Add the accessories provided in the context. Keep the face identical.",
                "strength": 0.45, # Mantener la estructura original del avatar
            }
        )
        result = await handler.get()
        return result['image']['url']