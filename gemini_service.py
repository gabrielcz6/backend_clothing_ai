import os
import google.generativeai as genai
from PIL import Image
import io

# Configura tu API KEY
genai.configure(api_key="TU_API_KEY_AQUI")

class GeminiService:
    def __init__(self):
        # Usamos imagen-3 para generación y edición
        self.model = genai.GenerativeModel('imagen-3')

    async def generate_initial_avatar(self, face_image_bytes: bytes, gender: str):
        """
        Genera un avatar basado en una foto de rostro y género.
        """
        # Convertimos bytes a objeto PIL
        face_img = Image.open(io.BytesIO(face_image_bytes))
        
        prompt = f"Create a high-quality stylized 3D avatar of a {gender} based on the facial features of the provided person. Pixar style, clean background."
        
        # En una implementación real con Gemini/Imagen, se envía la imagen de referencia
        # Nota: La capacidad de Image-to-Image varía según la región y permisos de la cuenta
        response = self.model.generate_content([prompt, face_img])
        
        # Asumiendo que la respuesta contiene la imagen (esto varía según el SDK exacto)
        # Por ahora simulamos el retorno de los bytes de la imagen generada
        return response.images[0].image_bytes

    async def modify_avatar_with_accessories(self, base_avatar_bytes: bytes, accessories_bytes: list[bytes]):
        """
        Toma el avatar base y le añade los accesorios (1 a 3).
        """
        base_img = Image.open(io.BytesIO(base_avatar_bytes))
        acc_images = [Image.open(io.BytesIO(b)) for b in accessories_bytes]
        
        prompt = "Modify the existing avatar by adding the accessories shown in the other images. Keep the facial features identical. Seamless integration."
        
        # Enviamos el avatar original + los accesorios
        inputs = [prompt, base_img] + acc_images
        
        response = self.model.generate_content(inputs)
        
        return response.images[0].image_bytes