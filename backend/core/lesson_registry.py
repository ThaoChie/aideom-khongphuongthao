from importlib import import_module
from django.http import Http404

LESSON_MODULES = [
    'core.lessons.lesson01_cobb_douglas',
    'core.lessons.lesson02_simple_lp',
    'core.lessons.lesson03_priority_index',
    'core.lessons.lesson04_region_lp',
    'core.lessons.lesson05_mip_projects',
    'core.lessons.lesson06_topsis',
    'core.lessons.lesson07_nsga_pareto',
    'core.lessons.lesson08_dynamic_optimization',
    'core.lessons.lesson09_labor_ai',
    'core.lessons.lesson10_stochastic',
    'core.lessons.lesson11_q_learning',
]
LESSONS = [import_module(name) for name in LESSON_MODULES]

def get_lesson(lesson_id: str):
    for lesson in LESSONS:
        if lesson.LESSON_ID == lesson_id:
            return lesson
    raise Http404(f'Lesson {lesson_id} not found')

def run_all_lessons(params):
    outputs = {}
    for lesson in LESSONS:
        outputs[lesson.LESSON_ID] = lesson.run(params.get(lesson.LESSON_ID, {}))
    return {'mode':'pipeline','lessons': outputs}
