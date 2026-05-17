from core.lesson_registry import LESSONS

def test_all_lessons_have_four_tabs():
    assert len(LESSONS) == 11
    for lesson in LESSONS:
        result = lesson.run({})
        assert set(['overview','allocation','scenarios','risks']).issubset(result['tabs'].keys())
        assert result['lesson']['params']
