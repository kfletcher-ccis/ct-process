"""
Marks EXISTING constituents with actionable update metadata.

This transformer must run after RecentFilterTransformer.

At that point:

- constituent.employment contains only employment records that
  passed the configured recent-date window.

- constituent.education contains only education records that
  passed the configured recent-date window for EXISTING records.
"""

class ExistingUpdateTransformer:

    def apply(self, constituent):
        """
        Add update flags and action names to the constituent.

        NEW constituents are not marked for update because they
        will use create operations instead.
        """

        constituent.update_flags = {
            "needs_employment_update": False,
            "needs_education_update": False,
            "needs_update": False,
        }

        constituent.update_actions = []

        if constituent.record_status != "EXISTING":
            return constituent

        needs_employment_update = (
            len(constituent.employment or []) > 0
        )

        needs_education_update = (
            len(constituent.education or []) > 0
        )

        constituent.update_flags = {
            "needs_employment_update": (
                needs_employment_update
            ),
            "needs_education_update": (
                needs_education_update
            ),
            "needs_update": (
                needs_employment_update
                or needs_education_update
            ),
        }

        if needs_employment_update:
            constituent.update_actions.append(
                "EMPLOYMENT"
            )

        if needs_education_update:
            constituent.update_actions.append(
                "EDUCATION"
            )

        return constituent