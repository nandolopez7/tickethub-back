import boto3
from django.conf import settings
try:
    from django.utils.translation import gettext as _
except ImportError:
    from django.utils.translation import ugettext as _
    
from tickethub_back.utils.custom_exceptions import CustomAPIException

"""
Documentación:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#rekognition
"""


class RekognitionLogicClass:
    """
    Clase que encapsula la lógica para interactuar con Amazon Rekognition.
    """

    def __init__(self, image_source) -> None:
        self.image_source = image_source.read()
        
    def compare_faces(self, image_target):
        """
        Compara dos imágenes en busca de similitudes faciales utilizando Amazon Rekognition.

        Args:
            image_source: Imagen de origen.
            image_target: Imagen objetivo.

        Returns:
            dict: Un diccionario con los resultados de la comparación.
        """

        try:
            client = boto3.client(
                'rekognition',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_DEFAULT_REGION
            )
            response = client.compare_faces(
                SimilarityThreshold=90,  # nivel de confianza mínimo para las coincidencias que se incluirán en la respuesta
                SourceImage={
                    'Bytes': self.image_source,
                },
                TargetImage={
                    'Bytes': image_target.read(),
                },
            )

            if not len(response['FaceMatches']):
                raise CustomAPIException({
                    "ok": False,
                    "message": _("No existe similitud entre las imagenes"),
                    "data": None
                })

            similarity = int(round(response['FaceMatches'][0]['Similarity'], 2))  # La similitud entre las caras en las imágenes 

            if similarity < 60:
                raise CustomAPIException({
                    "ok": False,
                    "message": _("La calidad de las imagenes no permite validar su similitud"),
                    "data": None
                })

            return {
                "ok": True,
                "message": _("Validación exitosa"),
                "data": {"similarity": similarity}
            }
        except CustomAPIException as err:
            raise err
        except Exception as err:
            raise CustomAPIException({
                "ok": False,
                "message": _("Error validando las imágenes"),
                "data": str(err)
            })

    def detect_faces(self):
        """
        Detecta rostros en una imagen utilizando Amazon Rekognition.

        Args:
            image_source: Imagen de origen (formato de bytes).

        Returns:
            dict: Un diccionario con los resultados de la detección.
        """
        print("**** type: ", type(self.image_source))
        try:
       
            client = boto3.client(
                'rekognition',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )

            response = client.detect_faces(
                Image={
                    'Bytes': self.image_source,
                },
                Attributes=['DEFAULT']
            )

            if len(response['FaceDetails']) == 0:
                raise CustomAPIException({
                    "ok": False,
                    "message": _("No se detectó ningún rostro en la imagen"),
                    "data": None
                })

            if len(response['FaceDetails']) > 1:
                raise CustomAPIException({
                    "ok": False,
                    "message": _("Se detectó más de un rostro en la imagen"),
                    "data": None
                })
            confidence = response["FaceDetails"][0]["Confidence"]  # La confianza en la detección del rostro 
            return {
                "ok": True,
                "message": _("Validación exitosa"),
                "data": {"confidence": confidence}
            }
        except CustomAPIException as err:
            raise err
        except Exception as err:
            raise CustomAPIException({
                "ok": False,
                "message": _("Error validando las imágenes"),
                "data": str(err)
            })
        