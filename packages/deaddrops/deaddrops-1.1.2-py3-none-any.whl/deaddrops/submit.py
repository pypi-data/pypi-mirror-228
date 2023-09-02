from PIL import Image
import requests
import re
import os

TYPE_USB = 1
TYPE_WIRELESS = 2
TYPE_LIVE = 3
TYPE_OTHER = 9

STATUS_BDSG = 0
STATUS_UNCONFIRMED = 1
STATUS_WORKING = 2


class SubmitHelper:
    def __init__(self):
        self.submit_form_dict = {}
        self.submit_data_list = []

        self.is_general_info_set = False
        self.is_location_info_set = False

    def setGeneralInformations(self, name: str, size: int, d_type: int) -> None:
        if d_type not in [TYPE_USB, TYPE_WIRELESS, TYPE_LIVE, TYPE_OTHER]:
            raise ValueError("Invalid value for parameter 'type'")

        self.submit_form_dict.update(
            {
                "name": name,
                "size": str(size) + " GB",
                "droptype": d_type,
            }
        )

        self.is_general_info_set = True

    def setLocationInformations(
        self,
        alpha2_country: str,
        state: str = "",
        city: str = "",
        zipcode: str = "",
        address: str = "",
        latitude: str = "",
        longitude: str = "",
    ) -> None:
        
        # Every alpha2 codes are made with this pattern : https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
        if not re.search(r"^[A-Z]{2}$", alpha2_country):
            raise ValueError("Parameter 'alpha2_country' is not a valid alpha2 format")

        if latitude and not re.search(
            r"^(\+|-)?((\d((\.)|\.\d{1,6})?)|(0*?[0-8]\d((\.)|\.\d{1,6})?)|(0*?90((\.)|\.0{1,6})?))$",
            latitude,
        ):
            raise ValueError("Parameter 'latitude' is not a valid latitude value")

        if longitude and not re.search(
            r"^(\+|-)?((\d((\.)|\.\d{1,6})?)|(0*?\d\d((\.)|\.\d{1,6})?)|(0*?1[0-7]\d((\.)|\.\d{1,6})?)|(0*?180((\.)|\.0{1,6})?))$",
            longitude,
        ):
            raise ValueError("Parameter 'longitude' is not a valid longitude value")

        self.submit_form_dict.update(
            {
                "country": alpha2_country,
                "state": state,
                "city": city,
                "zip": zipcode,
                "address": address,
                "lat": latitude,
                "lon": longitude,
            }
        )

        self.is_location_info_set = True

    def setDescriptionInformations(
        self,
        overview_img_file_path: str = None,
        medium_img_file_path: str = None,
        closeup_img_file_path: str = None,
        about: str = "",
    ) -> None:
        local_ifs = "\\" if os.name == "nt" else "/"
        counter = 0

        for file_path in [
            overview_img_file_path,
            medium_img_file_path,
            closeup_img_file_path,
        ]:
            counter += 1

            if not file_path:
                continue

            # deaddrops.com does not support files larger than 1Mb
            if os.path.getsize(file_path) > 1048576:
                raise RuntimeError(f"{file_path} is greater than 1Mb")

            # deaddrops.com does not support images greater than 300x300px
            image = Image.open(file_path)
            if image.width > 300 or image.height > 300:
                raise ValueError(f"{file_path} dimentions are greater than 300x300px")

            self.submit_data_list.append(
                (
                    f"picture{counter}",
                    (
                        file_path.split(local_ifs)[-1],
                        open(file_path, "rb"),
                        "image/" + os.path.splitext(file_path)[1].replace(".", ""),
                    ),
                )
            )

        self.submit_form_dict.update({"about": about})

    def submitDeadDrop(self, status: int = STATUS_WORKING) -> int | None:
        if not self.is_general_info_set and not self.is_location_info_set:
            raise RuntimeError("Missing general informations or location informations")

        if not status in [STATUS_BDSG, STATUS_UNCONFIRMED, STATUS_WORKING]:
            raise ValueError("Invalid value for parameter 'status'")

        session = requests.Session()

        # First GET request to get and keep the PHPESSID cookie through all the process
        req = session.get("https://deaddrops.com/db/?page=submit")

        # Preview request
        self.submit_form_dict.update({"submit": "Preview"})

        req = session.post(
            "https://deaddrops.com/db/?page=submit",
            files=self.submit_data_list,
            data=self.submit_form_dict,
        )

        if req.status_code >= 300:
            raise RuntimeError(
                f"Status code {req.status_code} for preview POST request"
            )

        # Submit request
        req = session.post(
            "https://deaddrops.com/db/?page=submit",
            data={"submit": "Submit Drop", "dd_status": status},
        )

        if req.status_code >= 300:
            raise RuntimeError(f"Status code {req.status_code} for submit POST request")

        if re.search(r"Id: [0-9]{1,}", test):
            return int(re.search(r"Id: [0-9]{1,}", test).group(0)[4:])
