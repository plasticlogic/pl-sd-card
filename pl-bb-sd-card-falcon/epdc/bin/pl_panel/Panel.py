"""@package docstring
Panel class module.
"""

#from PIL import Image
import subprocess
import os
import shutil
import logging

from PanelDisplay import PanelDisplay
import OneWireSwitch

PRE_BUFFER_FOLDER = "/tmp/pre"
POST_BUFFER_FOLDER = "/tmp/post"
CONFIG_PANEL_FOLDER = "/boot/uboot/panel"
CONFIG_IMAGES_FOLDER = os.path.join(CONFIG_PANEL_FOLDER, "numbers")
CONFIG_ORIENTATION_FILE = os.path.join(CONFIG_PANEL_FOLDER, "display_arrangement.txt")

class Panel:
        """
        Panel class.
        """

        def __init__(self):
                self.logger = logging.getLogger("Panel")
                self.__displays = []
                if (not os.path.exists(PRE_BUFFER_FOLDER)):
                        os.mkdir(PRE_BUFFER_FOLDER)
                if (not os.path.exists(POST_BUFFER_FOLDER)):
                        os.mkdir(POST_BUFFER_FOLDER)

        def get_displays_by_switches(self) -> None:
                """
                Search for display one wire switches and create panel objects for them.
                """
                path = OneWireSwitch.ONE_WIRE_DEVICES_FOLDER
                device_ids = os.listdir(path)

                display_idx = 0
                for dev_id in device_ids:
                        if dev_id.find(OneWireSwitch.FamilyCodes.DS2413) != -1:
                                self.__displays.append(PanelDisplay(dev_id, display_idx))
                                display_idx += 1

        def clear(self, num_of_displays: int = 3) -> None:
                """
                Clear the whole panel.
                """
                if self.__is_reorientable():
                        self.__reorientate_panels()

                raw_img_data = bytearray([0xFF] * 1280 * 960)
                for dsp_idx in range(len(self.__displays)):
                        self.logger.debug("Clear Display {}".format(dsp_idx))
                        raw_img_path = os.path.join(POST_BUFFER_FOLDER, f'{dsp_idx:03d}.raw')
                        with open(raw_img_path, "wb") as raw_img_file:
                                raw_img_file.write(raw_img_data)

                for display in self.__displays:
                        display.enable()
                        display.clear()
                        display.disable()

                self.__copy_post_to_pre()

        def update(self, update_folder: str) -> None:
                """
                Update panel.
                """
                if self.__is_reorientable():
                        self.logger.debug("Start normal update")
                        self.__reorientate_panels()
                        self.__update(update_folder)
                else:
                        self.logger.debug("start number update")
                        self.config_panel_update()

        def config_panel_update(self) -> None:
                self.__update(CONFIG_IMAGES_FOLDER)

        def __update(self, folder_path: str) -> None:
                #print("Path: ", folder_path)
                if (not os.path.isdir(folder_path)):
                        return
                
                image_list = os.listdir(folder_path)
                image_list.sort()
                panel_elements = min(len(self.__displays), len(image_list))

                img_idx = 0
                for image in image_list:
                        #print("Image idx ", img_idx)
                        image_path = os.path.join(folder_path, image)
                        self.__copy_convert_image(image_path, img_idx)
                        img_idx += 1

                #print("Image idx: ", img_idx)
                #print("Panel count: ", panel_elements)

                post_buffer_files = os.listdir(POST_BUFFER_FOLDER)
                post_buffer_files.sort()
                pre_buffer_files = os.listdir(PRE_BUFFER_FOLDER)
                pre_buffer_files.sort()
                for display_idx in range(panel_elements):
                        self.logger.debug("Update display {}".format(display_idx))
                        for dsp in self.__displays:
                                dsp.disable() # Disable all displays

                        pre_file = os.path.join(PRE_BUFFER_FOLDER, pre_buffer_files[display_idx])
                        post_file = os.path.join(POST_BUFFER_FOLDER, post_buffer_files[display_idx])
                        current_display = self.__displays[display_idx]

                        current_display.enable()
                        current_display.write_pre_buffer(pre_file)
                        current_display.update(post_file)
                        current_display.disable()

                self.__copy_post_to_pre()

        def __get_orientation_arr(self):
                orientation_arr = []
                
                if not os.path.isfile(CONFIG_ORIENTATION_FILE):
                        return orientation_arr

                with open(CONFIG_ORIENTATION_FILE) as f:
                        for line in f:
                                for num in line.split():
                                        orientation_arr.append(int(num))
                
                return orientation_arr

        def __is_reorientable(self) -> bool:
                
                orientation_arr = self.__get_orientation_arr()

                num_dsp = len(self.__displays)
                if not len(orientation_arr) == num_dsp:
                        return False
                
                if max(orientation_arr) > num_dsp:
                        return False

                for dsp_idx in orientation_arr:
                        if orientation_arr.count(dsp_idx) > 1:
                                return False
                
                return True

        def __reorientate_panels(self) -> None:
                orientation_arr = self.__get_orientation_arr()
                new_dsp_list = []

                for dsp_idx in orientation_arr:
                        new_dsp_list.append(self.__displays[dsp_idx - 1])
                
                self.__displays = new_dsp_list
        
        def __copy_convert_image(self, img_path: str, idx: int) -> None:
                """
                Convert image into raw format and copy it into post buffer
                """
                target_path = os.path.join(POST_BUFFER_FOLDER, f'{idx:03d}.raw')

                self.logger.debug("Convert Image")
                p = subprocess.run(["png2cfa", "--cfa=rgwb", "-i", img_path, "-o", target_path])
                
                if p.returncode != 0:
                        self.logger.error("Failed to convert {}.\nError Code {}.\n".format(
                                img_path, p.returncode, p.stdout))
                else:
                        self.logger.debug("Convertion done.")


        def __copy_post_to_pre(self) -> None:
                """
                Copy current post buffer content into pre buffer.
                """
                for folder_item in os.listdir(POST_BUFFER_FOLDER):
                        src_path = os.path.join(POST_BUFFER_FOLDER, folder_item)
                        dest_path = os.path.join(PRE_BUFFER_FOLDER, folder_item)

                        if (os.path.isfile(src_path)):
                                shutil.copyfile(src_path, dest_path)
