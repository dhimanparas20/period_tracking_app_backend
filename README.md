# Period Tracking Application Backend

This project involves developing a backend system for a period tracking application. The application enables users to track their menstrual cycles, including recording period start and end dates, symptoms, and other relevant information.

## Authentication

### Login
- **URL**: `/api/login/`
- **Method**: POST
- **Parameters**: 
  ```json
  {
      "username": "",
      "password": ""
  }
  ```
- **RESPONSE**
  ```json
  {
    "access": "",
    "user": [
        {
            "id": ,
            "user": ,
            "start_date": "",
            "end_date": "",
            "symptoms": ""
        }
    ]
  }
  ```
  
## User Data Management  

### User Details
- **URL**: `/api/user/`
- **Methods**: GET, POST, PUT (partial update) with pk, DELETE with pk

- User can filter their period's history by passing `start_date="YYYY-MM-DD"` & `end_date="YYYY-MM-DD"` parameters in get request.
- **Authorization**: Bearer token required

## Data Analysis
### Calculate Average Cycle Length

- **URL**: `/api/calculate_average_cycle_length/`
- **Method**: GET
- **Authorization**: Bearer token required

### Predict Next Period Date

- **URL**: `/api/predict_next_period/`
- **Method**: GET
- **Authorization**: Bearer token required

### Analyze Symptoms Count

- **URL**: `/api/analyze_symptoms_count/`
- **Method**: GET
- **Authorization**: Bearer token required

## Usage Notes
-    All API requests except login require a Bearer token passed in the authorization header.
-   Users must be authenticated to access user-related endpoints.
-    For data analysis endpoints, ensure the user has sufficient data available for accurate results.    