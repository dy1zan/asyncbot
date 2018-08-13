import re
from discord import Member
from typing import Union, List, Dict, Pattern  # Type hints

"""
Constants split into classes. Admin roles have extra information for rank comparison. Channels are combined into
lists in the Section class.
"""


class RePattern:
    # RP_NAME = re.compile("[A-Z][a-z]+_[A-Z].*")  # Capital, any amount of non cap, underscore, capital, anything
    RP_NAME = re.compile("^[A-Z][a-z]+_[A-Z]{1,2}([a-z][A-Z])?[a-z]+(_[A-Z]{1,2}([a-z][A-Z])?[a-z]+)?$")

    @staticmethod
    def contains_pattern(pattern: Pattern, phrase: Union[str, int]):
        contains = bool(re.search(pattern, phrase))
        return contains


class Role:
    EXECUTIVE = {'name': 'Executive', 'id': 465896094333927424, 'level': 99999}
    HEAD = {'name': 'Head', 'id': 465894668094144512, 'level': 1337}
    SENIOR = {'name': 'Senior', 'id': 465896014130184192, 'level': 4}
    GENERAL = {'name': 'General', 'id': 465887716354031624, 'level': 3}
    JUNIOR = {'name': 'Junior', 'id': 465896256972128266, 'level': 2}
    PROBIE = {'name': 'Probie', 'id': 475211931905556490, 'level': 1}
    ADMINISTRATOR = {'name': 'Administrator', 'id': 465874213324980244, 'level': 0}
    ADMIN_ROLES = [EXECUTIVE, HEAD, SENIOR, GENERAL, JUNIOR, PROBIE, ADMINISTRATOR]

    HELPER = {'name': 'Helper', 'id': 465874370904981514, 'level': -1}
    DEVELOPER = {'name': 'Developer', 'id': 465874671733309440, 'level': -1}
    TESTER = {'name': 'Tester', 'id': 465874643337740290, 'level': -1}

    @staticmethod
    def has_roles(author: Member, role_list: List[Dict[str, Union[str, int]]]) -> bool:
        for role in role_list:
            has_current_role = False
            for author_role in author.roles:
                if author_role.id == role['id']:
                    has_current_role = True
            if not has_current_role:
                return False
        return True

    @staticmethod
    def is_admin(author: Member) -> bool:
        if Role.get_level(author) >= 0:
            return True
        else:
            return False

    @staticmethod
    def get_level(author: Member) -> int:
        """
        Returns the admin level of a Discord member. Returns -1 if not an admin
        """
        level = -1  # Not an admin
        for role in author.roles:
            for admin_role in Role.ADMIN_ROLES:
                if role.id == admin_role['id']:
                    if admin_role['level'] > level:
                        level = admin_role['level']
        return level

    @staticmethod
    def get_rank(author: Member) -> Union[str, None]:
        """
        Returns the admin rank of a Discord member or None if they are not an admin
        """
        level = -1
        rank = None
        for role in author.roles:
            for admin_role in Role.ADMIN_ROLES:
                if role.id == admin_role['id']:
                    if admin_role['level'] > level:
                        rank = admin_role['name']
                        level = admin_role['level']
        if level == -1:
            return None
        return rank


class Channel:
    # IDs for every channel in the server
    # HELP/GENERAL
    GENERAL = 465873343518736397

    # ADMINISTRATORS
    DISCUSSION_ADMIN = 466404751857287178
    CHAT = 465873855672745985
    COMMANDS = 465875438321795074

    # HELPERS
    DISCUSSION_HELPER = 466420981813215232
    NEWBIE = 465874164960460800

    # PUBLIC SERVICES
    GOVERNMENT = 466434019278585869
    NEWS_AGENCY = 466434102661349380

    # DEVELOPMENT
    TESTERS = 465874413267582986
    CONFIRMED_BUGS = 471553508118626315
    BUGS = 465879591656095754
    BOT_TODO = 466949031898382356


class Section:
    # Lists of channel IDs in each section
    HELP_GENERAL = [Channel.GENERAL]
    ADMINISTRATORS = [Channel.DISCUSSION_ADMIN, Channel.CHAT, Channel.COMMANDS]
    HELPERS = [Channel.DISCUSSION_HELPER, Channel.NEWBIE]
    PUBLIC_SERVICES = [Channel.GOVERNMENT, Channel.NEWS_AGENCY]
    DEVELOPMENT = [Channel.TESTERS, Channel.CONFIRMED_BUGS, Channel.BUGS, Channel.BOT_TODO]

    @staticmethod
    def in_sections(channel_id: int, section_list: List[List[int]]) -> bool:
        """
        Verifies a Discord message was posted in the correct section(s) by taking in a list of lists containing
        channel IDs
        """
        for section in section_list:
            for section_channel_id in section:
                if channel_id == section_channel_id:
                    return True
        return False
