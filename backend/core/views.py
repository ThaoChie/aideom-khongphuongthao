from rest_framework.decorators import api_view
from rest_framework.response import Response
from .lesson_registry import LESSONS, get_lesson, run_all_lessons
from .models import LessonRun
from .lessons.common import to_jsonable

@api_view(['GET'])
def health(request):
    return Response({'status':'ok','version':'elearning-v5','message':'AIDEOM-VN eLearning API is running'})

@api_view(['GET'])
def lessons_list(request):
    return Response({'lessons':[m.metadata() for m in LESSONS]})

@api_view(['GET'])
def lesson_detail(request, lesson_id):
    module = get_lesson(lesson_id)
    return Response(module.metadata())

@api_view(['POST'])
def lesson_run(request, lesson_id):
    module = get_lesson(lesson_id)
    params = request.data.get('params', {}) if isinstance(request.data, dict) else {}
    result = to_jsonable(module.run(params))
    LessonRun.objects.create(lesson_id=lesson_id, params=to_jsonable(params), result=result)
    return Response(result)

@api_view(['POST'])
def pipeline_run(request):
    params = request.data.get('params', {}) if isinstance(request.data, dict) else {}
    return Response(to_jsonable(run_all_lessons(params)))
