import os
import sys
from PIL import Image
import numpy as np
import io
from rembg import remove
from PyQt5 import uic, QtWidgets, QtCore


class Create_mask(QtCore.QThread):
    notifyProgress = QtCore.pyqtSignal(int)
    numberFiles = QtCore.pyqtSignal(int)
    status = QtCore.pyqtSignal(str)
    def __init__(self, input_dir, output_dir, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.input_dir = input_dir
        self.output_dir = output_dir

    def run(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        jpg_files = [f for f in os.listdir(self.input_dir) if f.lower().endswith('.jpg')]
        self.numberFiles.emit(np.size(jpg_files))

        for jpg_file in jpg_files:
            input_path = os.path.join(self.input_dir, jpg_file)
            mask_filename = os.path.splitext(jpg_file)[0] + "_mask.png"
            output_path = os.path.join(self.output_dir, mask_filename)

            self.status.emit(f"Generating binary mask for {jpg_file}")

            # Use rembg to remove the background and generate a mask with transparency
            with open(input_path, "rb") as f_in:
                jpg_data = f_in.read()
                mask_data = remove(jpg_data)

            # Convert the mask with transparency to a binary mask
            mask_image = Image.open(io.BytesIO(mask_data))
            binary_mask = self.create_binary_mask(mask_image)

            # Save the binary mask as a PNG
            binary_mask.save(output_path)
            self.notifyProgress.emit(1)


    def create_binary_mask(self, mask_image):
        # Convert the mask to a NumPy array and extract the alpha channel
        mask_np = np.array(mask_image)
        alpha_channel = mask_np[:, :, 3]

        # Threshold the alpha channel to create a binary mask
        threshold = 128  # You can adjust this threshold value if needed
        binary_mask_np = (alpha_channel > threshold).astype(np.uint8) * 255
        return Image.fromarray(binary_mask_np)


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ui/view.ui', self)
        self.input_directory = ''
        self.output_path = ''
        self.mode = 'jpg'

        self.progress_bar_max = 0
        self.progress_bar_count = 0
        
        self.init_Ui()
        self.show()


    def init_Ui(self):
        self.openInputFolder.clicked.connect(lambda: self.open_folder(0))

        self.selectOutputFolder.clicked.connect(lambda: self.open_folder(1))

        self.create_mask_task = Create_mask(self.input_directory, self.output_path)
        self.create_mask_task.notifyProgress.connect(self.handleProgressBar)
        self.create_mask_task.numberFiles.connect(self.set_max_progressbar)
        self.create_mask_task.status.connect(self.handleStatusMessage)

        self.alignButton.clicked.connect(self.process_images)
        self.progressBar.setValue(0)
        self.statusBar().showMessage("Idle")


    def open_folder(self, mode):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Open a folder")
        if path != ('', ''):
            if mode == 0:
                self.input_directory = path + '/'
                self.labelInputFolder.setText(self.input_directory)
            if mode == 1:
                self.output_path = path + '/'
                self.labelOutputFolder.setText(self.output_path)


    @QtCore.pyqtSlot(str)
    def handleStatusMessage(self, message):
       self.statusBar().showMessage(message)


    @QtCore.pyqtSlot(int)
    def handleProgressBar(self, value):
        self.progress_bar_count += 1
        value = int((self.progress_bar_count/self.progress_bar_max)*100)
        self.progressBar.setValue(value)
        if value == 100:
            self.openInputFolder.setEnabled(True)
            self.selectOutputFolder.setEnabled(True)
            self.alignButton.setEnabled(True)
            self.statusBar().showMessage("Done!")
            QtWidgets.QMessageBox.about(self, " ", "Task completed")


    @QtCore.pyqtSlot(int)
    def set_max_progressbar(self, value):
       self.progress_bar_max = value


    def process_images(self):
        self.progressBar.setValue(0)

        self.create_mask_task = Create_mask(self.input_directory, self.output_path)
        self.create_mask_task.notifyProgress.connect(self.handleProgressBar)
        self.create_mask_task.numberFiles.connect(self.set_max_progressbar)
        self.create_mask_task.status.connect(self.handleStatusMessage)

        try:
            self.create_mask_task.start()
            # self.create_mask(self.input_directory, self.output_path)

            self.openInputFolder.setEnabled(False)
            self.selectOutputFolder.setEnabled(False)
            self.alignButton.setEnabled(False)

        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec()