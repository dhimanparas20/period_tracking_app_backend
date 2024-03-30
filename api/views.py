from .models import User
from .serializers import *
from django.contrib.auth import authenticate
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view,action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,GenericViewSet,ReadOnlyModelViewSet
from rest_framework.generics import get_object_or_404
from statistics import mean
from django.utils import timezone

#when sending token in header we nedd to specify Toekn or Bearer
# use [BearerTokenAuthentication] insted of [TokenAuthentication]
class BearerTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'

# API login for User. Returns a token
class Login(APIView):
    def post(self, request, format=None):
        try:
            username = request.data['username']
            password = request.data['password']
        except KeyError:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        token, _ = Token.objects.get_or_create(user=user)
        # Serialize user data
        periods = Period.objects.filter(user=user)  # Retrieve periods associated with the user
        serializer = PeriodSerializer(periods, many=True)  # Serialize multiple periods
        return Response({"access": str(token.key),"user": serializer.data})

#CRUD Operations on Data
class PeriodViewSet(ModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = self.queryset.filter(user=request.user)
        
        # Check if 'start_date' and 'end_date' query parameters are present
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        # Filter queryset by date range if query parameters are provided
        if start_date and end_date:
            queryset = queryset.filter(start_date__gte=start_date, end_date__lte=end_date)
        
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = Period.objects.all()
        period = get_object_or_404(queryset, pk=pk, user=request.user)
        serializer = self.serializer_class(period, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = Period.objects.all()
        period = get_object_or_404(queryset, pk=pk, user=request.user)
        period.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)   
    
    def calculate_average_cycle_length(self, request):
        periods = Period.objects.filter(user=request.user)  # Filter periods for the authenticated user
        cycle_lengths = [period.duration for period in periods if period.duration is not None]
        
        # Calculate the average cycle length
        average_cycle_length = sum(cycle_lengths) / len(cycle_lengths) if cycle_lengths else None
        
        return Response({"average_cycle_length": int(average_cycle_length)})
    
    def predict_next_period(self, request):
            periods = Period.objects.filter(user=request.user)
            if periods.count() >= 2:
                # Sort periods by start date to ensure they are ordered properly
                sorted_periods = periods.order_by('start_date')

                # Calculate the gap between consecutive periods
                period_gaps = [(sorted_periods[i + 1].start_date - sorted_periods[i].end_date).days
                            for i in range(len(sorted_periods) - 1)]
                # Calculate the average gap
                average_gap = sum(period_gaps) / len(period_gaps)

                # Predict the next period date by adding the average gap to the end date of the most recent period
                last_period = sorted_periods.last()
                predicted_next_period_date = last_period.end_date + timezone.timedelta(days=average_gap)
                return Response({"predicted_next_period_date": predicted_next_period_date}, status=200)
            else:
                return Response({"message": "Insufficient data to predict the next period date"}, status=400)
    
    def analyze_symptoms_count(self, request):
        user = request.user
        periods = Period.objects.filter(user=user)
        symptoms_count = {}

        # Count occurrences of each symptom
        for period in periods:
            symptoms = period.symptoms.split(',')  # Assuming symptoms are separated by commas
            for symptom in symptoms:
                symptom = symptom.strip()  # Remove leading/trailing whitespace
                if symptom:
                    if symptom in symptoms_count:
                        symptoms_count[symptom] += 1
                    else:
                        symptoms_count[symptom] = 1

        return Response({"symptoms_count": symptoms_count}, status=200)        

