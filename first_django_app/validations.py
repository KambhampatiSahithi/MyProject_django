import json
import re
from datetime import date, datetime


from .models import UserForm, ResponseInfo


class UserValidate:
    reason = ""
    response = ""
    '''pass arguments as keyword arguments'''
    def __init__(self, **kwargs):
        data = {}
        l = []
        for k, v in kwargs.items():
            l.append(k)
            data[k] = v
        self.first_name = data[l[0]]
        self.middle_name = data[l[1]]
        self.last_name = data[l[2]]
        self.dob = data[l[3]]
        self.gen = data[l[4]]
        self.nationality = data[l[5]]
        self.st = data[l[6]]
        self.ct = data[l[7]]
        self.pin = data[l[8]]
        self.qfy = data[l[9]]
        self.salary = data[l[10]]
        self.pan = data[l[11]]

    def validate_name(self):
        """validating first and lastname"""
        if self.first_name == "":
            self.reason += " First name is empty "
        if not bool(re.match('[a-zA-Z\s]+$', self.first_name)):
            self.reason += " FirstName should have Alphabets and Spaces "
        if self.last_name == "":
            self.reason += " Last name is empty "
        if not bool(re.match('[a-zA-Z\s]+$', self.last_name)):
            self.reason += " LastName should have Alphabets and Spaces "

    def validate_primary(self):
        """validating gender nationality state city"""
        state_list = ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar",
                      "Chhattisgarh", "Karnataka", "Madhya Pradesh",
                      "Odisha", "Tamil Nadu", "Telangana", "West Bengal"]

        if self.gen not in ["F", "M"]:
            self.reason += " Gender is invalid "
        if self.nationality not in ("Indian", "American"):
            self.reason += " Nationality should be Indian or American. "
        if self.st not in state_list:
            self.reason += " State should be from given list "
        if self.ct == "":
            self.reason += " City is Empty "

    def validate_dob(self):
        """validate entered dat of birth format"""
        try:
            form = "%Y-%m-%d"
            t = datetime.strptime(self.dob, form)
        except ValueError:
            self.reason += "Invalid date of birth format"

    def validate_pin(self):
        """validate pin should have 6 digits"""
        reg = "^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$"
        p = re.compile(reg)
        if self.pin == '':
            self.reason += "pin is empty"
        m = re.match(p, self.pin)
        if m is None:
            self.reason += " Pincode should have 6 digits" \
                           " only with single whitespace "

    def validate_qfy_salary(self):
        """validate salary between 10000 and 90000
        validate qualification(should be string) """
        if int(self.salary) <= 10000 or int(self.salary) >= 90000:
            self.reason += "salary is not in given range"
        if not (self.qfy.replace(" ", "").isalpha()):
            self.reason += " qualification is empty "

    def validate_pan(self):
        """validate pan should have 10 digits
            first 5 capital letters and 4 digits
            and last character should be capital"""
        reg = "[A-Z]{5}[0-9]{4}[A-Z]{1}"
        p = re.compile(reg)
        if self.pan == "":
            self.reason += " Pan is empty "
        if not (re.search(p, self.pan) and len(self.pan) == 10):
            self.reason += " pan should be 10 digits or in specified format. "

    def validate_age_gender(self):
        """validate age with gender
            female age should be greater than 18
            male age should be greater than 18"""
        l = list(map(int, self.dob.split("-")))
        u_dob = date(l[0], l[1], l[2])
        today = date.today()
        age_user = today.year - u_dob.year - ((today.month, today.day) < (u_dob.month, u_dob.day))
        if age_user < 18 and self.gen == "F":
            self.reason += " Age should be 18 or above for female. "
        if age_user < 21 and self.gen == "M":
            self.reason += " Age should be 21 or above for male. "

    def validate_recent_received_request(self):
        """validate with pin
            recently received request in last 5 days"""
        pan_tab = UserForm.objects.only('pan', 'request_receive_time')
        for i in pan_tab:
            t = i.request_receive_time.replace(tzinfo=None)
            diffdays = (t - datetime.now()).days
            if i.pan == self.pan and int(diffdays) <= 5:
                self.reason += " Recently request received in last 5 days "
                return False


class User(UserValidate):
    request_id = ""

    def validate_details(self):
        """call all validation functions in base class"""
        self.validate_name()
        self.validate_primary()
        self.validate_dob()
        self.validate_pin()
        self.validate_qfy_salary()
        self.validate_pan()
        self.validate_age_gender()
        self.validate_recent_received_request()

        """success or failure based on reason """
        if self.reason == "":
            self.reason += "-"
            self.response += "Success"
        else:
            self.response += "Failure"
            return False
        return True

    def push_to_UserForm(self):
        """pushing userdata to UserForm table"""
        my = UserForm(first_name=self.first_name, middle_name=self.middle_name,
                      last_name=self.last_name, dob=self.dob, gender=self.gen,
                      nationality=self.nationality, state=self.st, city=self.ct,
                      pin=self.pin, qualification=self.qfy, salary=self.salary, pan=self.pan)
        my.save()

    def push_to_Response_info(self):
        """pushing response to Response_info table"""
        self.request_id = UserForm.objects.latest('id').id
        my = ResponseInfo(response=self.response, reason=self.reason, request_id_id=self.request_id)
        my.save()

    def json_result(self):
        """convert response information into json format"""
        response_dict = {"Request_id": self.request_id, "Response": self.response, "Reason": self.reason}

        json_obj = json.dumps(response_dict)
        #json_obj = json.loads(json_dump)
        return json_obj
