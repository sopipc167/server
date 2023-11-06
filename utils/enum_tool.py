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