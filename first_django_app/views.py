from django.shortcuts import render
from django.views import View

from . import validations
import logging

# Create your views here.
logging.basicConfig(filename="logger.txt",
                    filemode="a",
                    format='%(asctime)s %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.info("Started execution")


class HomeView(View):
    def get(self, request):
        logging.info("renders request that for form to get data")
        return render(request, 'form.html', {'name': 'welcome to request form'})


class AddDataView(View):
    """main class that does all operations needed"""

    def post(self, request):
        logging.info("Started getting data from form")
        if request.method == "POST":
            fn = request.POST['fn']
            mn = request.POST['mn']
            ln = request.POST['ln']
            dob = request.POST['dob']
            gen = request.POST['gen']
            nat = request.POST['natn']
            st = request.POST['st']
            ct = request.POST['cty']
            pin = request.POST['pin']
            qfy = request.POST['qfy']
            sal = request.POST['sal']
            pan = request.POST['pan']

            user = validations.User(first_name=fn, middle_name=mn,
                                    last_name=ln, dob=dob, gender=gen,
                                    nationality=nat, state=st, city=ct,
                                    pin=pin, qualification=qfy, salary=sal, pan=pan)
            user.validate_details()
            logging.info("Validated required validations")
            user.push_to_UserForm()
            logging.info("pushed data to userform table")
            user.push_to_Response_info()
            logging.info("pushed response to response info table")
            json_obj = user.json_result()
            logging.info("json formatted data is sent to result.html ")

            return render(request, 'result.html', {'json_result': json_obj})
        else:
            return render(request, "form.html")



