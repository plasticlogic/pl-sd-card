"""@package docstring
Panel class module.
"""

#from PIL import Image
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
                clear_buffer_path = os.path.join(POST_BUFFER_FOLDER, "clear")
                if (not os.path.exists(clear_buffer_path)):
                        os.mkdir(clear_buffer_path)
                        raw_img_data = bytearray([0xFF] * 1280 * 960)
                        for dsp_idx in range(len(self.__displays)):
                                raw_img_path = os.path.join(clear_buffer_path, f'{dsp_idx:03d}.raw')
                                raw_img_file = open(raw_img_path, "wb")
                                raw_img_file.write(raw_img_data)
                                raw_img_file.close()


                for display in self.__displays:
                        display.enable()
                        display.clear()
                        display.disable()

        def update(self, update_folder: str) -> None:
                """
                Update panel.
                """
                if (not os.path.isdir(update_folder)):
                        return

                saved_image_names = os.listdir(POST_BUFFER_FOLDER)
                new_image_name = os.path.basename(update_folder)
                new_post_image_folder = os.path.join(POST_BUFFER_FOLDER, new_image_name)

                if (not new_image_name in saved_image_names):
                        os.mkdir(new_post_image_folder)
                        self.__prepare_post_buffer(new_post_image_folder, update_folder)
                
                image_list = os.listdir(new_post_image_folder)
                panel_elements = max(self.__displays.count(), image_list.count())

                for display_idx in range(panel_elements):
                        current_display = self.__displays[display_idx]
                        current_display.enable()
                        current_display.update(image_list[display_idx])
                        current_display.disable()

                self.__copy_post_to_pre(new_post_image_folder)


        def __prepare_post_buffer(self, new_post_folder: str, image_folder: str) -> None:
                """
                Create new post image folder and convert related images
                """
                folder_items = os.listdir(image_folder)
                image_idx = 0
                for item in folder_items:
                        if (os.path.isfile(item)):
                                img_path = os.path.join(image_folder, item)
                                self.__copy_convert_image(img_path, new_post_folder, image_idx)
                                image_idx += 1
        
        def __copy_convert_image(self, img_path: str, target_folder_path: str, idx: int) -> None:
                """
                Convert image into raw format and copy it into post buffer
                """
                #img = Image.open(img_path, mode="r")
                #dest_file_path = os.path.join(target_folder_path, str(idx) + ".raw")
                #dest_file = open(dest_file_path, "wb")

                #img.convert("RGB")
                #pixels = list(img.getdata())
                #dest_file.write(pixels)
                return


        def __copy_post_to_pre(self, post_folder_path: str) -> None:
                """
                Copy current post buffer content into pre buffer.
                """
                if (os.path.exists(post_folder_path) and os.path.isdir(post_folder_path)):
                        for folder_item in os.listdir(post_folder_path):
                                src_path = os.path.join(post_folder_path, folder_item)
                                dest_path = os.path.join(PRE_BUFFER_FOLDER, folder_item)

                                if (os.path.isfile(src_path)):
                                        shutil.copyfile(src_path, dest_path)