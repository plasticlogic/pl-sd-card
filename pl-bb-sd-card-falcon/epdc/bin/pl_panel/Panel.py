"""@package docstring
Panel class module.
"""

#from PIL import Image
import subprocess
import os
import shutil

from PanelDisplay import PanelDisplay
import OneWireSwitch

PRE_BUFFER_FOLDER = "/tmp/pre"
POST_BUFFER_FOLDER = "/tmp/post"

class Panel:
        """
        Panel class.
        """

        def __init__(self):
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
                raw_img_data = bytearray([0xFF] * 1280 * 960)
                for dsp_idx in range(len(self.__displays)):
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
                if (not os.path.isdir(update_folder)):
                        return
                
                image_list = os.listdir(update_folder)
                panel_elements = max(len(self.__displays), len(image_list))

                img_idx = 0
                for image in image_list:
                        image_path = os.path.join(update_folder, image)
                        self.__copy_convert_image(image_path, img_idx)
                        img_idx += 1

                post_buffer_files = os.listdir(POST_BUFFER_FOLDER)
                pre_buffer_files = os.listdir(PRE_BUFFER_FOLDER)
                for display_idx in range(panel_elements):
                        pre_file = os.path.join(PRE_BUFFER_FOLDER, pre_buffer_files[display_idx])
                        post_file = os.path.join(POST_BUFFER_FOLDER, post_buffer_files[display_idx])
                        current_display = self.__displays[display_idx]
                        current_display.enable()
                        current_display.write_pre_buffer(pre_file)
                        current_display.update(post_file)
                        current_display.disable()

                self.__copy_post_to_pre()
        
        def __copy_convert_image(self, img_path: str, idx: int) -> None:
                """
                Convert image into raw format and copy it into post buffer
                """
                target_path = os.path.join(POST_BUFFER_FOLDER, f'{idx:03d}.raw')
                subprocess.call(["png2cfa", "-i", img_path, "-o", target_path])


        def __copy_post_to_pre(self) -> None:
                """
                Copy current post buffer content into pre buffer.
                """
                for folder_item in os.listdir(POST_BUFFER_FOLDER):
                        src_path = os.path.join(POST_BUFFER_FOLDER, folder_item)
                        dest_path = os.path.join(PRE_BUFFER_FOLDER, folder_item)

                        if (os.path.isfile(src_path)):
                                shutil.copyfile(src_path, dest_path)