
class MsgTranslator(object):
    """
        This dict is used for translator message around all program, because Qt linguist can't
        translate those wrote by python, such as status, tooltip, self create widgets.

        rules:
        in language list:
        0 : EN
        1 : CN
    """
    def __init__(self, language):
        self.language = language
        self.msg_trans_dict = dict()
        self.trans_rules_dict = dict()
        # ------------------------------
        self.rules_dict()
        self.translator_dict()

    def rules_dict(self):
        self.trans_rules_dict = {
            'English': 0,
            'Chinese': 1,
        }

    def translator_dict(self):
        self.msg_trans_dict = {
            'warning': ['Warning', '警告'],
            'already_open': ['Program already opened', '程序已在运行，请勿重复打开'],
            'welcome': ['Welcome,', '欢迎用户'],
            'login_unlock': ['Please Login to Unlock More Functions', '未登录，请登陆后解锁更多功能'],
            'delete_warning': ['Delete Warning', '删除警告'],
            'confirm_delete': ['Item cannot be restored once deleted, please confirm', '删除后无法被恢复，请确认'],
            'plan_launch': ['Planed mission will be launched in', '计划任务启动倒计时'],
            'minutes': ['minutes', '分钟'],
            'suspend_next': ['Suspend next：', '暂停队列：'],
            'pwd_error': ['Wrong PWD', '密码错误'],
            'acc_error': ['Wrong ACC', '账号错误'],
            'choose_project': ['Please choose project file', '请选择项目文件'],
            'choose_journal': ['Please choose journal file', '请选择journal文件'],
            'no_case_mesh': ['Case or Mesh do not exist', 'Case或者Mesh不存在'],
            'no_journal': ['Journal do not exist', 'Journal不存在'],
            'no_license': ['Not enough license', '没有足够的license'],
            'drop_reject': ['File type do not accept', '文件类型不支持']

        }

    def make_trans(self, key):
        return self.msg_trans_dict[key][self.trans_rules_dict[self.language]]


if __name__ == '__main__':
    language = 'English'
    translator = MsgTranslator(language)

