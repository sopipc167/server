class EnumTool:
    # index 데이터를 문자열로 변경
    @staticmethod
    def convert_to_string(dictionary, index):
        return dictionary.get(index, None)

    # 문자열 데이터를 index로 변경
    @staticmethod
    def convert_to_index(dictionary, string):
        for key, value in dictionary.items():
            if value == string:
                return key
        return None
    
class UserEnum(EnumTool):
    RANK = {0: '탈퇴자', 1: '정회원', 2: '수습회원', 3: '명예회원', 4: '수습회원(휴학)', 5: '졸업생'}
    PART = {0: '디자인', 2: '아트', 3: '프로그래밍'}
    REST_TYPE = {-1: '활동', 0: '일반휴학', 1:'군휴학'}

class AttendanceEnum(EnumTool):
    CATEGORY = {0: '디자인', 1: '아트', 2: '프로그래밍', 3: '정기', 4: '기타'}
    USER_ATTENDANCE_STATE = {0: '출석', 1: '지각', 2: '불참'}