"""CSV schema builder for CT Process export with duplicate headers."""


class CsvSchemaBuilder:
    CORE_FIELDS = [
        "NEW?", "ConsID", "ConsCode", "ConsCode",
        "Titl1", "FirstName", "MidName", "LastName", "Suff1", "NickName",
        "AliasType", "AliasName", "AliasType", "AliasName", "AliasType", "AliasName", "AliasType", "AliasName",
        "AliasType", "AliasName", "AliasType", "AliasName", "AliasType", "AliasName", "AliasType", "AliasName",
        "Bplace", "Bday", "SolCode", "KeyInd",
        "AddrLines", "AddrCity", "AddrCountry", "AddrCounty", "AddrState", "AddrZIP", "AddrSeasFrom", "AddrType", "AddrValidFrom", "AddrValidTo", "PrefAddr",
        "AddrLines", "AddrCity", "AddrCountry", "AddrCounty", "AddrState", "AddrZIP", "AddrSeasFrom", "AddrType", "AddrValidFrom", "AddrValidTo", "PrefAddr",
        "Gender", "Religion", "MrtlStat",
    ]

    PHONE_BLOCK = ["PhoneType", "PhoneNum", "PhoneIsPrimary"]

    EMPLOYMENT_BLOCK = [
        "ORFullName", "ORPos", "ORProf", "ORFromDate", "ORToDate", "ORIndustry",
        "ORIsEmp", "ORIsPrimary", "ORRelat", "ORRecip",
    ]

    MILITARY_BLOCK = [
        "ORFullName", "ORProf", "ORIndustry", "ORIsEmp", "ORIsPrimary", "ORRelat", "ORRecip",
    ]

    RELATIONSHIP_BLOCK = ["IRLink", "IRRelat", "IRRecip"]

    @staticmethod
    def education_degree_block(max_major_records, max_minor_records, max_attribute_records):
        """Build one repeated degree block.

        Correct ImpID layout:
        - One ESRMajESRImpID per set of majors, followed by all ESRMajMajor columns.
        - One ESRMinESRImpID per set of minors, followed by all ESRMinMinor columns.
        - One ESRAttrESRImpID per set of attributes, followed by repeated ESRAttrCat/ESRAttrDesc pairs.
        """
        headers = [
            "ESRSchoolName", "ESRDateEnt", "ESRDateLeft", "ESRDegree", "ESRDateGrad", "ESRClassOf", "ESRCampus", "ESRPrimAlum",
            "ESRMajESRImpID",
        ]
        headers.extend(["ESRMajMajor"] * max_major_records)

        headers.append("ESRMinESRImpID")
        headers.extend(["ESRMinMinor"] * max_minor_records)

        headers.append("ESRAttrESRImpID")
        for _ in range(max_attribute_records):
            headers.extend(["ESRAttrCat", "ESRAttrDesc"])

        return headers

    def build_headers(self, schema_analysis):
        headers = []
        headers.extend(self.CORE_FIELDS)

        for _ in range(schema_analysis.get("max_phone_records", 0)):
            headers.extend(self.PHONE_BLOCK)

        for _ in range(schema_analysis.get("max_employment_records", 0)):
            headers.extend(self.EMPLOYMENT_BLOCK)

        for _ in range(schema_analysis.get("max_degree_records", 0)):
            headers.extend(self.education_degree_block(
                schema_analysis.get("max_major_records", 0),
                schema_analysis.get("max_minor_records", 0),
                schema_analysis.get("max_attribute_records", 0),
            ))

        for _ in range(schema_analysis.get("max_military_records", 0)):
            headers.extend(self.MILITARY_BLOCK)

        for _ in range(schema_analysis.get("max_relationship_records", 0)):
            headers.extend(self.RELATIONSHIP_BLOCK)

        return headers
