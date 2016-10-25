from configuration import models


def practice_info(request):
    return {
        'practice_info': models.PracticeInfo.get_solo(),
    }
