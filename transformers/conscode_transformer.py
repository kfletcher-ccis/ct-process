from helpers.common import is_within_last_days

class ConsCodeTransformer:
    def apply(self, constituent):
        constituent.core["ConsCode"] = ""

        constituent.core.pop(
            "ConsCode_2",
            None
        )

        if constituent.record_status == "NEW":

            self._apply_new_logic(
                constituent
            )

        else:

            self._apply_existing_logic(
                constituent
            )

        return constituent


    # -----------------------------------------------------

    def _apply_new_logic(
        self,
        constituent
    ):

        has_employment = (
            len(constituent.employment) > 0
        )

        has_education = (
            len(constituent.education) > 0
        )

        codes = []

        if has_employment:
            codes.append(
                "Employee"
            )

        if has_education:
            codes.append(
                "Alumni"
            )

        self._assign_codes(
            constituent,
            codes
        )

    # -----------------------------------------------------

    def _apply_existing_logic(
        self,
        constituent
    ):

        codes = []

        if self._has_recent_employment(
            constituent
        ):
            codes.append(
                "Employee"
            )

        if self._has_recent_education(
            constituent
        ):
            codes.append(
                "Alumni"
            )

        self._assign_codes(
            constituent,
            codes
        )

    # -----------------------------------------------------

    def _assign_codes(
        self,
        constituent,
        codes
    ):

        if not codes:
            return

        constituent.core[
            "ConsCode"
        ] = codes[0]

        if len(codes) > 1:

            constituent.core[
                "ConsCode_2"
            ] = codes[1]

    # -----------------------------------------------------

    def _has_recent_employment(
        self,
        constituent
    ):

        for employment in constituent.employment:

            if is_within_last_days(
                employment.from_date,
                90
            ):
                return True

            if is_within_last_days(
                employment.to_date,
                90
            ):
                return True

        return False

    # -----------------------------------------------------

    def _has_recent_education(
        self,
        constituent
    ):

        for degree in constituent.education:

            if is_within_last_days(
                degree.graduation_date,
                90
            ):
                return True

        return False