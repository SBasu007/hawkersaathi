import json
from pathlib import Path
from typing import Any, Dict


# Paths

BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMES_PATH = BASE_DIR / "data" / "schemes.json"


# Load scheme database

def load_schemes() -> Dict[str, Any]:
    """
    Load the curated multilingual scheme database.
    """

    try:
        with open(
            SCHEMES_PATH,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except FileNotFoundError:
        return {}

    except json.JSONDecodeError as error:
        print(
            f"Invalid JSON in schemes.json: {error}"
        )
        return {}


SCHEMES = load_schemes()


# Tool 1: Get scheme information

def get_scheme_info(
    scheme_name: str,
    language: str = "bn"
) -> Dict[str, Any]:
    """
    Retrieve grounded information about a supported
    government scheme.

    Supported languages:
    - bn: Bengali
    - hi: Hindi
    - en: English
    """

    # Normalize language
    if language not in {"bn", "hi", "en"}:
        language = "bn"

    # Find scheme
    scheme = SCHEMES.get(scheme_name)

    if not scheme:
        return {
            "success": False,
            "error": "scheme_not_found",
            "scheme_name": scheme_name,
            "message": {
                "bn": "এই প্রকল্পের তথ্য আমাদের ডেটাবেসে পাওয়া যায়নি।",
                "hi": "इस योजना की जानकारी हमारे डेटाबेस में नहीं मिली।",
                "en": "Scheme information was not found in the database."
            }[language]
        }

    # Select translated fields
    name_key = f"name_{language}"

    result = {
        "success": True,
        "scheme_id": scheme["scheme_id"],
        "name": scheme.get(
            name_key,
            scheme.get("name_en")
        ),
        "summary": scheme["summary"].get(
            language,
            scheme["summary"].get("en")
        ),
        "target_group": scheme["target_group"].get(
            language,
            scheme["target_group"].get("en")
        ),
        "verification_required": scheme.get(
            "verification_required",
            True
        ),
        "last_verified": scheme.get(
            "last_verified"
        )
    }

    # Add loan information only if present
    if "loan_tranches" in scheme:
        result["loan_tranches"] = scheme[
            "loan_tranches"
        ]

    # Add interest subsidy only if present
    if "interest_subsidy" in scheme:
        subsidy = scheme["interest_subsidy"]

        result["interest_subsidy"] = {
            "value": subsidy.get("value"),
            "note": subsidy.get(
                f"note_{language}",
                subsidy.get("note_en")
            )
        }

    return result