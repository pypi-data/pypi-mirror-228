from libreflow.baseflow.ui.mytasks import (
    MyTasksPageWidget      as BaseMyTasksPageWidget
)


class MyTasksPageWidget(BaseMyTasksPageWidget):

    def build(self):
        super(MyTasksPageWidget, self).build()
        self.header.fdt_button.hide()
