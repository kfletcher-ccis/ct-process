from models import Constituent, PhoneRecord, EmploymentRecord
from helpers.common import normalize_lookup_id, split_pipe_values, clean_null_value, is_email, safe_get, repeated_values
from helpers.name_normalization import normalize_name


class CoreTransformer:
    def __init__(self, existing_ids_map):
        self.existing_ids_map = existing_ids_map

    def transform_row(self, row):
        lookup_id = normalize_lookup_id(row.get("ConsID", ""))
        existing = self.existing_ids_map.get(lookup_id)
        sky_id = existing.get("sky_id") if existing else None
        cons_import_id = existing.get("cons_import_id") if existing else None
        status = "EXISTING" if existing else "NEW"
        c = Constituent(lookup_id=lookup_id, sky_id=sky_id, cons_import_id=cons_import_id, record_status=status)
        c.core = self._build_core_record(row)
        c.phones = self._build_phone_records(row)
        c.employment = self._build_employment_records(row)
        return c

    def _build_core_record(self, row):
        core = {k: clean_null_value(v) for k, v in row.to_dict().items()}
        core["ConsID"] = normalize_lookup_id(core.get("ConsID", ""))
        core["KeyInd"] = "I"
        for col in ["Deceased", "DecDate", "AddSalText"]:
            core.pop(col, None)

        # ConsCode is derived later; do not pass through source value.
        core["ConsCode"] = ""
        core.pop("ConsCode_2", None)

        core["NickName"] = self._resolve_nickname(row)
        self._normalize_name_fields(core)
        self._clear_duplicate_address_block(core)
        return core

    def _normalize_name_fields(self, core):
        for field in ["FirstName", "MidName", "LastName", "NickName"]:
            if field in core:
                core[field] = normalize_name(core[field])
        for i in range(1, 20):
            field = "AliasName" if i == 1 else f"AliasName_{i}"
            if field in core:
                core[field] = normalize_name(core[field])

    def _clear_duplicate_address_block(self, core):
        primary_type = clean_null_value(core.get("AddrType", "")).upper()
        secondary_type = clean_null_value(core.get("AddrType_2", "")).upper()
        if not primary_type or not secondary_type:
            return
        if primary_type == secondary_type:
            for field in [
                "AddrLines_2", "AddrCity_2", "AddrCountry_2", "AddrCounty_2", "AddrState_2", "AddrZIP_2",
                "AddrSeasFrom_2", "AddrType_2", "AddrValidFrom_2", "AddrValidTo_2", "PrefAddr_2",
            ]:
                if field in core:
                    core[field] = ""

    def _resolve_nickname(self, row):
        candidates = []
        first = clean_null_value(row.get("FirstName", ""))
        nickname = clean_null_value(row.get("NickName", ""))
        if first:
            candidates.append(first)
        if nickname:
            candidates.append(nickname)
        alias_types = repeated_values(row, "AliasType")
        alias_names = repeated_values(row, "AliasName")
        for t, n in zip(alias_types, alias_names):
            if t in {"Preferred Name", "Chosen Name"} and n:
                candidates.append(n.split()[0] if " " in n else n)
        if not candidates:
            return ""
        counts = {}
        for c in candidates:
            key = c.strip().lower()
            counts[key] = counts.get(key, 0) + 1
        max_count = max(counts.values())
        winners = {k for k, v in counts.items() if v == max_count}
        if first and first.lower() in winners:
            return normalize_name(first)
        for c in candidates:
            if c.lower() in winners:
                return normalize_name(c)
        return normalize_name(first or candidates[0])

    def _build_phone_records(self, row):
        records = []
        email_found = False
        phone_types = repeated_values(row, "PhoneType", 20)
        phone_nums = repeated_values(row, "PhoneNumber", 20)
        max_count = max(len(phone_types), len(phone_nums))
        for i in range(max_count):
            phone_type = clean_null_value(
                safe_get(phone_types, i)
            )
            phone_num = clean_null_value(
                safe_get(phone_nums, i)
            )
            if not phone_num:
                continue
            email = is_email(phone_num)
            primary = False
            if phone_type == "Colleague Cell Phone":
                primary = True
            if email and not email_found:
                primary = True
                email_found = True
            if email:
                phone_num = (
                    phone_num
                    .strip()
                    .rstrip(";")
                    .lower()
                )
            records.append(
                PhoneRecord(
                    phone_type=phone_type,
                    phone_value=phone_num,
                    is_primary=primary,
                    is_email=email,
                )
            )

        return records

    def _build_employment_records(self, row):
        """
        Build employment records while preserving positional alignment
        across all pipe-delimited source fields.

        Blank values and N/A placeholders must remain in position until
        the corresponding employment fields have been matched by index.
        """

        def split_preserving_positions(value):
            """
            Split a double-pipe-delimited value without removing empty
            values or N/A placeholders.

            Examples:

            "A||B"      -> ["A", "B"]
            "N/A||Date" -> ["N/A", "Date"]
            "A||||C"    -> ["A", "", "C"]
            """

            if value is None:
                return []

            text = str(value).strip()

            if not text:
                return []

            return [
                item.strip()
                for item in text.split("||")
            ]

        def normalize_optional_date(value):
            """
            Convert source null placeholders to an empty string after
            positional alignment has been preserved.
            """

            cleaned = clean_null_value(value)

            if cleaned.upper() in {
                "N/A",
                "NA",
                "NONE",
                "NULL",
            }:
                return ""

            return cleaned

        positions = split_preserving_positions(
            row.get("ORPos", "")
        )

        professions = split_preserving_positions(
            row.get("ORProf", "")
        )

        from_dates = split_preserving_positions(
            row.get("ORFromDate", "")
        )

        to_dates = split_preserving_positions(
            row.get("ORToDate", "")
        )

        industries = split_preserving_positions(
            row.get("ORIndustry", "")
        )

        organizations = split_preserving_positions(
            row.get("ORFullName", "")
        )

        max_count = max(
            len(positions),
            len(professions),
            len(from_dates),
            len(to_dates),
            len(industries),
            len(organizations),
            0,
        )

        records = []

        for i in range(max_count):

            position = clean_null_value(
                safe_get(positions, i)
            )

            profession = clean_null_value(
                safe_get(professions, i)
            )

            from_date = normalize_optional_date(
                safe_get(from_dates, i)
            )

            to_date = normalize_optional_date(
                safe_get(to_dates, i)
            )

            industry = clean_null_value(
                safe_get(industries, i)
            )

            organization = clean_null_value(
                safe_get(organizations, i)
            )

            if not organization:
                organization = "Columbia College"

            if not any([
                position,
                profession,
                from_date,
                to_date,
                industry,
            ]):
                continue

            records.append(
                EmploymentRecord(
                    organization=organization,
                    position=position,
                    profession=profession,
                    from_date=from_date,
                    to_date=to_date,
                    industry=industry,
                    is_employer=True,
                    is_primary=(i == 0),
                    relationship="Employer",
                    reciprocal="Employee",
                )
            )

        return records