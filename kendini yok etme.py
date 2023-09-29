import os
import sys
import ctypes
import shutil
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QFileDialog, QMessageBox, QWidget


class AppWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Arayüz ayarları
        self.setWindowTitle("Dosya Silme Programı")
        self.setGeometry(100, 100, 400, 200)

        self.window = QLabel("Dosya Silme Programı", self)
        self.window.setGeometry(0, 0, 400, 50)
        self.window.setStyleSheet("font-size: 24px;")

        self.folders_label = QLabel("Silinecek Klasörleri Seçin", self)
        self.folders_label.setGeometry(50, 50, 300, 50)
        self.folders_label.setStyleSheet("font-size: 18px;")

        self.select_button = QPushButton("Klasör Seç", self)
        self.select_button.setGeometry(100, 80, 200, 50)
        self.select_button.setStyleSheet("font-size: 16px;")
        self.select_button.clicked.connect(self.select_folders)

        self.delete_button = QPushButton("Klasörleri Sil", self)
        self.delete_button.setGeometry(100, 140, 200, 50)
        self.delete_button.setStyleSheet("font-size: 16px;")
        self.delete_button.clicked.connect(self.delete_folders)

        # Yönetici izni kontrolü
        if os.name == "nt" and not ctypes.windll.shell32.IsUserAnAdmin():
            QMessageBox.critical(self, "Hata", "Programın yönetici izniyle çalıştırılması gerekiyor.")
            sys.exit()

        # Yeni buton
        self.delete_selected_button = QPushButton("Seçilen Klasörleri Sil", self)
        self.delete_selected_button.setGeometry(100, 200, 200, 50)
        self.delete_selected_button.setStyleSheet("font-size: 16px;")
        self.delete_selected_button.clicked.connect(self.delete_selected_folders)

    def select_folders(self):
        # QFileDialog kullanarak klasörleri seçme
        folders = QFileDialog.getExistingDirectory(
            self, "Klasörleri Seçin", options=QFileDialog.DontUseNativeDialog | QFileDialog.ShowDirsOnly | QFileDialog.ReadOnly)
        if folders:
            with open('klasor_yollari.txt', 'w') as f:
                f.write(folders)
                print("Klasör yolu kaydedildi.")


    def delete_folders(self):
        # Klasörleri okuma
        try:
            with open('klasor_yollari.txt', 'r') as f:
                folders = f.readlines()
        except FileNotFoundError:
            print("Klasör yolu dosyası bulunamadı.")
            return

            # Seçilen klasörleri silme
        for folder in folders:
            folder = folder.strip()
            try:
                shutil.rmtree(folder)
                print(f"{folder} klasörü başarıyla silindi.")
            except OSError as e:
                print(f"{folder} klasörü silinirken hata oluştu: {e}")

        QMessageBox.information(self, "Başarılı", "Klasörler başarıyla silindi.")

    def delete_selected_folders(self):
        # Klasörleri okuma
        try:
            with open('klasor_yollari.txt', 'r') as f:
                folders = f.readlines()
        except FileNotFoundError:
            QMessageBox.critical(self, "Hata", "Kaydedilmiş klasör yolu bulunamadı.")
            return

        # Seçilen klasörleri silme
        selected_folders = []
        for folder in folders:
            if os.path.isdir(folder.strip()):
                reply = QMessageBox.question(self, "Klasörü Sil", f"{folder.strip()} klasörünü silmek istiyor musunuz?",
                                            QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    try:
                        shutil.rmtree(folder.strip())
                        selected_folders.append(folder.strip())
                        print(f"{folder.strip()} klasörü silindi.")
                    except OSError as e:
                        print(f"{folder.strip()} klasörü silinirken bir hata oluştu: {e}")
            else:
                print(f"{folder.strip()} klasörü bulunamadı.")

        # Kullanıcıya silinen klasörleri gösterme
        if selected_folders:
            QMessageBox.information(self, "Klasörler Silindi",
                                    f"Seçilen klasörler başarıyla silindi:\n{','.join(selected_folders)}")
        else:
            QMessageBox.information(self, "Klasörler Silinmedi",
                                    "Seçilen klasörler silinmedi.")

        # Dosyaya kalan klasör yollarını yazma
        with open('klasor_yollari.txt', 'w') as f:
            for folder in folders:
                f.write(folder)

        QMessageBox.information(self, "Başarılı", "Klasörler başarıyla silindi.") 



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AppWindow()
    window.show()
    sys.exit(app.exec_())
