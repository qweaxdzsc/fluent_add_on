from PyQt5.QtGui import QIcon, QPixmap


class UiSet(object):
    def __init__(self, ui):
        self.ui = ui

    def set_all_icon(self):
        self._set_icon('login.png', self.ui.action_login)
        self._set_icon('logout.png', self.ui.action_logout)
        self._set_icon('add.png', self.ui.action_add)
        self._set_icon('journal.png', self.ui.action_journal)
        self._set_icon('delete.png', self.ui.action_delete)
        self._set_icon('help.png', self.ui.action_help)

    def _set_icon(self, pict, action):
        icon = QIcon()
        icon.addPixmap(QPixmap("./icon/%s" % (pict)), QIcon.Normal, QIcon.Off)
        action.setIcon(icon)

    def ui_user_logoff(self, logoff=True):
        self.ui.action_add.setDisabled(logoff)
        self.ui.action_delete.setDisabled(logoff)
        self.ui.action_add.setStatusTip('请先登陆后使用添加功能')
        self.ui.action_delete.setStatusTip('请先登陆后使用删除功能')
