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
        positions = split_pipe_values(row.get("ORPos", ""))
        professions = split_pipe_values(row.get("ORProf", ""))
        from_dates = split_pipe_values(row.get("ORFromDate", ""))
        to_dates = split_pipe_values(row.get("ORToDate", ""))
        industries = split_pipe_values(row.get("ORIndustry", ""))
        max_count = max(len(positions), len(professions), len(from_dates), len(to_dates), len(industries))
        records = []
        for i in range(max_count):
            if not any([safe_get(positions, i), safe_get(professions, i), safe_get(industries, i)]):
                continue
            records.append(EmploymentRecord(
                position=safe_get(positions, i),
                profession=safe_get(professions, i),
                from_date=safe_get(from_dates, i),
                to_date=safe_get(to_dates, i),
                industry=safe_get(industries, i),
                is_primary=(i == 0),
            ))
        return records
