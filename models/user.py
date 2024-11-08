import string

from datetime import date

from typing import Optional

from pydantic import EmailStr, constr, validator

from models.core import DateTimeModelMixin, IDModelMixin, CoreModel


def validate_username(username: str) -> str:
    allowed = string.ascii_letters + string.digits + "-" + "_"
    assert all(char in allowed for char in username), "Invalid characters in username."
    assert len(username) >= 3, "Username must be 3 characters or more."
    return username

def validate_password(password: str) -> str:
    must_have = string.ascii_letters + string.punctuation
    assert all(char in must_have for char in password), "Invalid characters in username."
    assert len(password) >= 8, "Username must be 8 characters or more."
    return password


class UserBase(CoreModel):
    '''
    Base user model
    '''
    user_email: Optional[EmailStr]
    user_name: Optional[str]
    email_verified: bool = False
    is_active: bool = True
    is_therapist: bool = False
    is_superuser: bool = False


class UserCreate(CoreModel):
    """
    Email and password are required for registering a new user
    Returns user_id, sends data on e-mail
    """
    user_name: str
    user_email: EmailStr
    password: constr(min_length=1, max_length=100)

    # @validator("username", pre=True)
    # def username_is_valid(cls, username: str) -> str:
    #     return validate_username(username)
    #
    # @validator("password", pre=True)
    # def password_is_valid(cls, password: str) -> str:
    #     return validate_password(password)

class UserLogin(CoreModel):
    """
    Email and password are required for registering a new user
    Returns user_id, sends data on e-mail
    """
    user_email: EmailStr
    password: constr(min_length=9, max_length=100)

    # @validator("username", pre=True)
    # def username_is_valid(cls, username: str) -> str:
    #     return validate_username(username)
    #
    # @validator("password", pre=True)
    # def password_is_valid(cls, password: str) -> str:
    #     return validate_password(password)

class UserLoginGen(CoreModel):
    """
    Email and password are required for registering a new user
    Returns user_id, sends data on e-mail
    """
    user_email: EmailStr



class UserClient(CoreModel):
    """
    User data
    """
    session_token: str # генерится на бэке для подтверждения сессии

    user_age: date  #YYYY-MM-DD
    user_experience: bool
    user_type: bool
    user_languages: list[int]
    user_symptoms: list[int]
    user_therapist_gender: int
    user_time: str                               # 0 - любое, 1 - ближайшнн, 2 - конкретное
    user_specific_date_time: Optional[str] = ''  #
    user_price: int                              # 0 - не важно, 1 - 10000, 2 - 25000, 3 - 40000
    user_phone: str
    user_timezone: Optional[int] = 0
    user_photo: Optional[str] = None  #TODO CHANGE

class UserMainData(CoreModel):
    session_token: str
    name: str
    email: str
    user_languages: list
    user_timezone: int


class UserRequestData(CoreModel):
    session_token: str
    user_type: int
    user_symptoms: list[int]
    user_therapist_gender: int
    user_time: int
    user_specific_date_time: str
    user_price: int

class UserTherapistReview(CoreModel):
    session_token: str
    problems: list
    more_problems: Optional[str]
    call_me: int


class AdminReport(CoreModel):
    session_token: Optional[str] = None
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    report_subject: Optional[str] = 'REPORT'
    report_text: str


class DocRegister(CoreModel):
    doc_name: str
    doc_date_of_birth: date # YYYY-MM-DD
    doc_gender: int
    doc_edu: list[dict]
    doc_method: list
    doc_method_other: Optional[str] = '' # TODO REMOVE
    doc_language: list
    doc_edu_additional: list
    doc_comunity: str
    doc_practice_start: str
    doc_online_experience: str
    doc_customers_amount_current: str
    doc_therapy_length: str
    doc_personal_therapy: str
    doc_supervision: str
    doc_another_job: str
    doc_customers_slots_available: str
    doc_socials_links: str
    doc_citizenship: str
    doc_citizenship_other: str
    doc_ref: str
    doc_ref_other: str
    doc_phone: str
    doc_email: str
    doc_additional_info: str
    doc_question_1: str
    doc_question_2: str
    doc_contact: str
    user_photo: Optional[list]


class DocUpdate(CoreModel):
    session_token: str
    doc_date_of_birth: date  # YYYY-MM-DD

    doc_language: list
    doc_additional_info: str
    # doc_method: list
    doc_client_age: int
    doc_lgbtq: int
    doc_therapy_type: int
    symptoms: list



class DocScheldure(CoreModel):
    session_token: Optional[str]
    schedule: Optional[list]
    timezone: Optional[str]


class UserTherapist(CoreModel):
    session_token: str  # генерится на бэке для подтверждения сессии

    user_id: int
    user_therapist_sex: str
    user_therapist_date_of_birth: str
    user_therapist_education: str
    user_therapist_method: int
    user_therapist_education_addictions: bool
    user_therapist_education_food_disorder: bool
    user_therapist_education_sexology: bool
    user_therapist_education_ptsd: bool
    user_therapist_education_other: bool
    '''
    user_therapist_diplomas: list
    '''
    user_therapist_community: str
    user_therapist_online_experience: int
    user_therapist_client_count: int
    user_therapist_longest_client: str
    user_therapist_on_therapy: bool
    user_therapist_on_supervision: bool
    user_therapist_other_work: str
    user_therapist_clients_ready: str
    user_therapist_links: str
    user_therapist_citezenship: int
    user_therapist_phone: str
    user_therapist_essay: str
    user_therapist_unethical: str
    user_therapist_offline_only_cases: str

class UserTherapistFull(UserTherapist):
    session_token: str  # генерится на бэке для подтверждения сессии

    user_therapist_language: str
    user_therapist_experience: str
    user_therapist_about_self: str
    user_therapist_methods: list[int]
    user_therapist_lower18: bool
    user_therapist_lgbtq_experience: bool
    user_therapist_pair_therapy: bool
    user_therapist_symptomatics: list[int]
    user_therapist_relations: list[int]
    user_therapist_events: list[int]
    user_therapist_session_cost: int
    user_therapist_card_number: str


class SingleToken(CoreModel):
    session_token: str

class ApproveTherapistToken(CoreModel):
    session_token: str
    doc_id: int


class SelectTime(CoreModel):
    session_token: str
    doc_id: int
    sh_id: int





class ApproveTime(CoreModel):
    session_token: str
    sh_id: int
    ch_id: Optional[int] = None
    approved: bool


class ReSelectTime(CoreModel):
    session_token: str
    old_sh_id: int
    new_sh_id: int
    ch_id: Optional[int] = None


class CancelTherapy(CoreModel):
    session_token: str
    doc_id: int


class UserUpdate(CoreModel):
    """
    Users are allowed to update their email and/or username
    """
    session_token: str  # генерится на бэке для подтверждения сессии

    user_email: EmailStr
    password: constr(min_length=7, max_length=100)
    user_name: str

    # @validator("username", pre=True)
    # def username_is_valid(cls, username: str) -> str:
    #     return validate_username(username)
    #
    # @validator("password", pre=True)
    # def password_is_valid(cls, password: str) -> str:
    #     return validate_password(password)


class UserClientUpdate(UserUpdate):
    '''
    From front user data update
    '''
    user_dateofbirth: int
    user_experience: bool
    user_isindividual: bool
    user_filters: list[int]
    user_sex_preference: int
    user_time_preference: int
    user_selected_time: int
    user_cash_preference: int


class UserPasswordUpdate(CoreModel):
    """
    Users can change their password
    """
    password: constr(min_length=7, max_length=100)
    salt: str

    # @validator("password", pre=True)
    # def password_is_valid(cls, password: str) -> str:
    #     return validate_password(password)


class UserInDB(IDModelMixin, DateTimeModelMixin, UserBase):
    """
    Add in id, created_at, updated_at, and user's password and salt
    """
    password: constr(min_length=7, max_length=100)
    salt: str

    # @validator("password", pre=True)
    # def password_is_valid(cls, password: str) -> str:
    #     return validate_password(password)
