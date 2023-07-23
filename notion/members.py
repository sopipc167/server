from notion.notion import NotionDatabase
import re
import configparser

config = configparser.ConfigParser()
config.read_file(open('config/config.ini'))
MEMBERS_DB = config['NOTION']['MEMBERS_DB']

class Members():
    @classmethod
    def get_targets(self, target_ranks, parts=None):
        filter = self.filter(ranks=target_ranks, parts=parts)

        db = NotionDatabase(MEMBERS_DB, filter)
        
        targets = [
            {
                'id': self.parse_rich_text(member['properties']['PCube+_식별자']['rich_text']),
                'name': member['properties']['이름']['title'][0]['plain_text'],
                'rank': self.parse_select(member['properties']['분류']['select']),
                'grade': member['properties']['학년']['number'],
                'part': self.parse_select(member['properties']['파트']['select']),
                
                'univ': self.parse_select(member['properties']['학교']['select']),
                'last_cleaning': self.parse_date(member['properties']['최근 청소 일자']['date']),
                'rest_type': self.parse_select(member['properties']['휴학종류']['select']),
                
                'etc_message': self.parse_rich_text(member['properties']['비고']['rich_text']),
                'absent_reason': self.parse_rich_text(member['properties']['정기적불참사유']['rich_text']),
                'absent_detail_reason': self.parse_rich_text(member['properties']['정기적불참상세사유']['rich_text']),
                'phone_number': self.parse_rich_text(member['properties']['연락처']['rich_text']),
                'join_date': self.parse_date(member['properties']['가입일']['date']),
                'birth_date': self.parse_date(member['properties']['생년월일']['date']),
                'birth_month': member['properties']['생일(월)']['formula']['number'],
                'birth_day': member['properties']['생일(일)']['formula']['number'],
                'major': self.parse_rich_text(member['properties']['학과']['rich_text']),
                'student_id': member['properties']['학번']['number'],
                'is_next_birth': member['properties']['익월생일여부']['formula']['boolean'],
                'return_plan_date': self.parse_date(member['properties']['복학예정일']['date']),
                'workshop_count': member['properties']['워크샵 참여 횟수']['number'],
                'gogoma': self.parse_multi_select(member['properties']['꼬꼬마 프로젝트 수행시기']['multi_select']),
                
                # 경고에 대한 데이터
                'warnings': member['properties']['경고']['number'],
                'half_warnings': member['properties']['주의']['number'],
                'total_warnings': member['properties']['누계']['formula']['number'],
            }
            for member in db.data
        ]
        targets = sorted(targets, key=lambda x: (x['rank'], x['name']))

        return targets

    def filter(ranks=None, parts=None, seminar=None):
        # 기본값, 모든 항목에 해당하는 조건
        filter_default = { 'property': '이름', 'rich_text': { 'is_not_empty': True } }
        filter_rank = filter_default.copy()
        filter_part = filter_default.copy()
        filter_seminar = filter_default.copy()

        # 분류
        if ranks is not None:
            filter_rank = {
                'or': [
                    {'property': '분류', 'select': {'equals': rank}}
                    for rank in ranks
                ]
            }
        
        # 파트
        if parts is not None:
            filter_part = {
                'or': [
                    {'property': '파트', 'select': { 'equals': part }}
                    for part in parts
                ]
            }

        # 정기적불참사유
        if seminar:
            filter_seminar = {
                'property': '정기적불참사유',
                'rich_text': {
                    'is_empty': True
                }
            }
        
        return {
            'and': [
                filter_rank,
                filter_part,
                filter_seminar,
            ]
        }

    def parse_name(nickname):
        regex = re.compile('[\[|\(|\<](.*?)[\]|\)|\>]')
        search = regex.search(nickname)

        if search is not None:
            name = search.group()[1:-1]
        else:
            name = nickname

        return name
    
    def parse_select(select):
        if not select:
            return None
        elif select['name']:
            return select['name']
        return None
    
    def parse_multi_select(multi_select):
        if not multi_select:
            return None
        elif multi_select:
            return [data['name'] for data in multi_select]
        return None
    
    def parse_date(date):
        if not date:
            return None
        elif date['end']:
            return date['end']
        elif date['start']:
            return date['start']
        return None

    def parse_rich_text(data):
        if len(data) > 0 and 'plain_text' in data[0]:
            return data[0]['plain_text']
        return None
