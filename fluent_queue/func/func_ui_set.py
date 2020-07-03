from PyQt5.QtGui import QIcon, QPixmap


class UiSet(object):
    def __init__(self, ui):
        """
        help main ui to set UI
        1. set icon
        2. set action button default status, some disabled
        :param ui:
        """
        self.ui = ui
        self.ui.action_delete.setDisabled(True)
        # self.ui.progressBar.hide()

    def set_all_icon(self):
        self._set_icon('login.png', self.ui.action_login)
        self._set_icon('logout.png', self.ui.action_logout)
        self._set_icon('add.png', self.ui.action_add)
        self._set_icon('journal.png', self.ui.action_journal)
        self._set_icon('delete.png', self.ui.action_delete)
        self._set_icon('setting.png', self.ui.action_setting)

    def _set_icon(self, pict, action):
        """
        set icon function
        :param pict:
        :param action:
        :return:
        """
        icon = QIcon()
        icon.addPixmap(QPixmap("./icon/%s" % (pict)), QIcon.Normal, QIcon.Off)
        action.setIcon(icon)

    def ui_user_logoff(self, logoff=True):
        """
        two status decide by account log status
        when login:
        1. enable add, delete, logout action button
        2. enable queue list widget, which can be manipulate
        when logoff: do the opposite
        :param logoff:
        :return:
        """
        self.ui.action_add.setDisabled(logoff)
        self.ui.action_delete.setDisabled(logoff)
        self.ui.action_logout.setDisabled(logoff)
        self.ui.action_login.setEnabled(logoff)
        self.ui.action_setting.setDisabled(logoff)
        # self.ui.action_add.setStatusTip('请先登陆后使用添加功能')
        # self.ui.action_delete.setStatusTip('请先登陆后使用删除功能')
        self.ui.listWidget_queue.setDisabled(logoff)


