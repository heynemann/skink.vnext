from skink.worker import BoxType


class PythonBoxType(BoxType):
    def __init__(self):
        install = "sudo apt-get install python python-pip -y"
        name = "python"
        super(PythonBoxType, self).__init__(name, install)
