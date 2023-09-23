from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import openpyxl
import pymongo

database = pymongo.MongoClient("mongodb+srv://sgyaswal1:Y1fs6XlNygTrt6Yy@cluster0.iwy1azb.mongodb.net/?retryWrites=true&w=majority")["assignment"]

Projects = database['projects']

class ExcelDataView(APIView):
    def post(self, request):
        excel_file = request.FILES.get('excel_file')
        
        if not excel_file:
            return Response({'message': 'No Excel file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            workbook = openpyxl.load_workbook(excel_file)
            worksheet = workbook.active
        except Exception as e:
            return Response({'message': 'Error loading the Excel file', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        data_to_insert = []

        for row in worksheet.iter_rows(min_row=2, values_only=True):
            if len(row) >= 6:
                project_data = {
                    'title': row[0],
                    'technologies': row[1],
                    'skillset_frontend': row[2],
                    'skillset_backend': row[3],
                    'skillset_databases': row[4],
                    'skillset_infrastructure': row[5]
                }
                data_to_insert.append(project_data)

        if not data_to_insert:
            return Response({'message': 'No valid data found in the Excel file'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Projects.insert_many(data_to_insert)
            return Response({'message': "Data saved successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': 'Error saving data', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GetProjects(APIView):
    def get(self, request):
        try:
            data = list(Projects.aggregate([{'$project':{"_id":0}}]))
            if data:
                return Response({'data': data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Data not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': 'Error fetching data', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DeleteAllDataView(APIView):
    def post(self, request):
        try:
            result = Projects.delete_many({})
            
            return Response(
                {
                    "message": f"Deleted {result.deleted_count} documents from the collection."
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"message": f"Error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )