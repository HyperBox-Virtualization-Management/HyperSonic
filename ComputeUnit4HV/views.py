from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PrivateSwitchSerializer, InternalSwitchSerializer, ExternalSwitchSerializer


@api_view(['POST'])
def create_private_switch(request):
    if request.method == 'POST':
        serializer = PrivateSwitchSerializer(data=request.data)
        if serializer.is_valid():
            switch = serializer.save()
            return Response({"message": "Private switch created successfully!", "switch_name": switch.switch_name},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_internal_switch(request):
    if request.method == 'POST':
        serializer = InternalSwitchSerializer(data=request.data)
        if serializer.is_valid():
            switch = serializer.save()
            return Response({"message": "Internal switch created successfully!", "switch_name": switch.switch_name},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_external_switch(request):
    if request.method == 'POST':
        serializer = ExternalSwitchSerializer(data=request.data)
        if serializer.is_valid():
            switch = serializer.save()
            return Response({"message": "External switch created successfully!", "switch_name": switch.switch_name},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
