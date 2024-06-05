from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from urllib.request import urlopen

from tickethub_back.utils.custom_exceptions import CustomAPIException
from tickethub_back.utils.logic.rekognition import RekognitionLogicClass


class RekognitionViewSet(viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'])
    def compare_faces(self,  request, *args, **kwargs):
        image_source = self.__get_image_request(request.data, 'image_source')
        image_target = self.__get_image_request(request.data, 'image_target')
        try:
            rekognition = RekognitionLogicClass(image_source=image_source)
            data = rekognition.compare_faces(image_target)
            return Response(data, status=status.HTTP_200_OK)
        except CustomAPIException as err:
            return Response(err.default_detail, status=err.status_code)
        
    @action(detail=False, methods=['POST'])
    def detect_faces(self,  request, *args, **kwargs):
        image_source = self.__get_image_request(request.data, 'image_source')
        try:
            rekognition = RekognitionLogicClass(image_source=image_source)
            data = rekognition.detect_faces()
            return Response(data, status=status.HTTP_200_OK)
        except CustomAPIException as err:
            return Response(err.default_detail, status=err.status_code)

    def __get_image_request(self, data, name_file):
        """
        Se recibe una imagen por url o por inputfile
        """
        try:
            image_url = data[name_file]

            'Determina si es una URL (string)'
            if isinstance(image_url, str):
                image = urlopen(image_url)
            else:
                image = data[name_file]

            return image

        except Exception as error:
            print("Error obteniendo imagen " + str(data) + str(error))
            raise Exception('No es posible acceder a los parametros. ' + str(error))
