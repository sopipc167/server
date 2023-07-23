
class UserTool:
    @classmethod
    def rank_to_index(self, rank_str):
        ranks = ['탈퇴자', '정회원', '수습회원', '명예회원', '수습회원(휴학)', '졸업생']
        for idx, value in enumerate(ranks):
            if value == rank_str:
                return idx
        return -1

    @classmethod
    def part_to_index(self, part_str):
        parts = ['디자인', '아트', '프로그래밍']
        for idx, value in enumerate(parts):
            if value == part_str:
                return idx
        return -1
    
    @classmethod
    def rest_type_to_index(self, rest_type_str):
        rest_types = ['일반휴학', '군휴학']
        for idx, value in enumerate(rest_types):
            if value == rest_type_str:
                return idx
        return -1
