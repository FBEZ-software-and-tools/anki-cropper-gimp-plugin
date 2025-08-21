#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp, GLib


class AnkiCropPlugin(Gimp.PlugIn):
    def do_query_procedures(self):
        return ["anki-cropper"]

    def do_set_i18n(self, name):
        return False

    def do_create_procedure(self, name):
        procedure = Gimp.ImageProcedure.new(
            self, name, Gimp.PDBProcType.PLUGIN, self.run, None)
        procedure.set_image_types("*")
        procedure.set_menu_label("Anki Crop")
        procedure.add_menu_path("<Image>/Filters/Anki/")
        procedure.set_documentation(
            "Anki Crop plugin for GIMP 3",
            "Crop to selection if exists, then resize image to 200 px height",
            name
        )
        procedure.set_attribution("Your Name", "Your Name", "2025")
        return procedure

    def run(self, procedure, run_mode, image, drawables, config, run_data):
        image.undo_group_start()

        try:
            selection = image.get_selection()
            has_selection = not selection.is_empty(image)

            if has_selection:
                # Crop image to selection bounds
                has_sel, not_empty, x1, y1, x2, y2 = selection.bounds(image)
                if has_sel:
                    width = x2 - x1
                    height = y2 - y1
                    image.crop(width, height, x1, y1)

            # Resize image to 200 px height keeping aspect ratio
            original_width = image.get_width()
            original_height = image.get_height()

            target_height = 200
            target_width = int(original_width * (target_height / original_height))

            image.scale(target_width, target_height)

        except Exception as e:
            Gimp.message(f"Error processing image: {e}")

        finally:
            image.undo_group_end()

        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())


Gimp.main(AnkiCropPlugin.__gtype__, sys.argv)



 