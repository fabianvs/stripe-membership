from django.shortcuts import redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist


class RollSelectionMiddleware:
    """ roll slection verification"""

    def __init__(self, get_response):
        """Middleware initialization."""
        self.get_response = get_response

    def __call__(self, request):
        """Code to be executed for each request before the view is called."""
        
        if not request.user.is_anonymous:
            if not request.user.is_staff:

                user = request.user
                stu_valid = False
                pro_valid = False

                try:
                    user.student
                except ObjectDoesNotExist:
                    pass
                else:
                    stu_valid = True

                try:
                    user.profesor
                except ObjectDoesNotExist:
                    pass
                else:
                    pro_valid = True

                #import pdb; pdb.set_trace()

                if pro_valid != True and stu_valid != True:
                    if request.path not in [reverse('roll'), reverse('logout'), reverse('add_student'), reverse('add_profesor')]:
                        return redirect('roll')

        response = self.get_response(request)
        return response