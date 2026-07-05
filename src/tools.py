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


# Tool 2: PM SVANidhi eligibility pre-screening

def check_svanidhi_eligibility(
    has_vending_card: bool,
    has_aadhaar: bool,
    years_active: int = 0,
    language: str = "bn"
) -> Dict[str, Any]:
    """
    Perform a cautious pre-screening for PM SVANidhi.

    IMPORTANT:
    This function does NOT provide official eligibility
    or loan approval.

    It only gives a preliminary guidance status based on
    the limited information supplied by the user.
    """

    # Normalize language
    if language not in {"bn", "hi", "en"}:
        language = "bn"

    # Basic input validation
    if years_active < 0:
        return {
            "success": False,
            "error": "invalid_years_active",
            "message": {
                "bn": "ব্যবসার বছরের সংখ্যা ঋণাত্মক হতে পারে না।",
                "hi": "व्यवसाय के वर्षों की संख्या नकारात्मक नहीं हो सकती।",
                "en": "Years active cannot be negative."
            }[language]
        }

    # Case 1:
    # Vendor card available
    if has_vending_card:
        return {
            "success": True,
            "status": "potentially_eligible",
            "official_approval": False,
            "scheme_id": "PM_SVANidhi",
            "first_tranche_up_to_inr": 15000,

            "message": {
                "bn": (
                    "আপনার দেওয়া তথ্য অনুযায়ী আপনি "
                    "সম্ভাব্যভাবে PM SVANidhi সহায়তার জন্য "
                    "প্রাথমিক যাচাই করতে পারেন। এটি চূড়ান্ত "
                    "যোগ্যতা বা ঋণ অনুমোদন নয়।"
                ),
                "hi": (
                    "आपके द्वारा दी गई जानकारी के अनुसार "
                    "आप PM SVANidhi सहायता के लिए प्रारंभिक "
                    "जांच कर सकते हैं। यह अंतिम पात्रता या "
                    "ऋण स्वीकृति नहीं है।"
                ),
                "en": (
                    "Based on the information provided, "
                    "you may proceed to preliminary verification "
                    "for PM SVANidhi support. This is not final "
                    "eligibility or loan approval."
                )
            }[language],

            "next_action": {
                "bn": (
                    "সরকারি উৎস বা অনুমোদিত সহায়তা কেন্দ্রের "
                    "মাধ্যমে বর্তমান যোগ্যতার নিয়ম যাচাই করুন।"
                ),
                "hi": (
                    "सरकारी स्रोत या अधिकृत सहायता केंद्र के "
                    "माध्यम से वर्तमान पात्रता नियम सत्यापित करें।"
                ),
                "en": (
                    "Verify current eligibility rules through "
                    "an official source or authorized assistance centre."
                )
            }[language],

            "verification_required": True
        }

    # Case 2:
    # No vending card but some vending history
    if not has_vending_card and years_active > 0:
        return {
            "success": True,
            "status": "needs_more_information",
            "official_approval": False,
            "scheme_id": "PM_SVANidhi",

            "message": {
                "bn": (
                    "আপনার ভেন্ডিং কার্ড নেই, তবে আপনি ব্যবসা "
                    "করার ইতিহাস জানিয়েছেন। শুধুমাত্র এই তথ্যের "
                    "ভিত্তিতে যোগ্যতা নিশ্চিত করা যায় না।"
                ),
                "hi": (
                    "आपके पास वेंडिंग कार्ड नहीं है, लेकिन आपने "
                    "व्यवसाय का इतिहास बताया है। केवल इस जानकारी "
                    "के आधार पर पात्रता तय नहीं की जा सकती।"
                ),
                "en": (
                    "You do not have a vending card but reported "
                    "a vending history. Eligibility cannot be "
                    "determined from this information alone."
                )
            }[language],

            "next_action": {
                "bn": (
                    "স্থানীয় কর্তৃপক্ষ বা সরকারি সহায়তা ব্যবস্থার "
                    "মাধ্যমে গ্রহণযোগ্য বিকল্প প্রমাণ ও বর্তমান "
                    "নিয়ম যাচাই করুন।"
                ),
                "hi": (
                    "स्थानीय प्राधिकरण या सरकारी सहायता व्यवस्था "
                    "से स्वीकार्य वैकल्पिक प्रमाण और वर्तमान "
                    "नियम सत्यापित करें।"
                ),
                "en": (
                    "Verify acceptable alternative evidence and "
                    "current rules through the relevant local authority "
                    "or official assistance channel."
                )
            }[language],

            "verification_required": True
        }

    # Case 3:
    # Insufficient information
    return {
        "success": True,
        "status": "official_verification_required",
        "official_approval": False,
        "scheme_id": "PM_SVANidhi",

        "message": {
            "bn": (
                "বর্তমান তথ্যের ভিত্তিতে সম্ভাব্য যোগ্যতা "
                "মূল্যায়ন করা যাচ্ছে না।"
            ),
            "hi": (
                "वर्तमान जानकारी के आधार पर संभावित पात्रता "
                "का आकलन नहीं किया जा सकता।"
            ),
            "en": (
                "Potential eligibility cannot be assessed "
                "from the current information."
            )
        }[language],

        "next_action": {
            "bn": (
                "বর্তমান সরকারি যোগ্যতার নিয়ম যাচাই করুন এবং "
                "প্রয়োজনীয় বিক্রেতা-সংক্রান্ত তথ্য সংগ্রহ করুন।"
            ),
            "hi": (
                "वर्तमान सरकारी पात्रता नियम सत्यापित करें और "
                "आवश्यक विक्रेता-संबंधी जानकारी एकत्र करें।"
            ),
            "en": (
                "Verify current official eligibility rules and "
                "collect the necessary vendor-related information."
            )
        }[language],

        "verification_required": True
    }


# Tool definitions for Gemma

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_scheme_info",
            "description": (
                "Retrieve grounded information about a supported "
                "government scheme from the curated HawkerSathi database."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "scheme_name": {
                        "type": "string",
                        "enum": [
                            "PM_SVANidhi",
                            "PMEGP",
                            "Jan_Dhan"
                        ],
                        "description": (
                            "Canonical identifier of the scheme."
                        )
                    },
                    "language": {
                        "type": "string",
                        "enum": ["bn", "hi", "en"],
                        "description": (
                            "Language for the returned information."
                        )
                    }
                },
                "required": [
                    "scheme_name",
                    "language"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "check_svanidhi_eligibility",
            "description": (
                "Perform a cautious preliminary pre-screening "
                "for possible PM SVANidhi support. "
                "This does not provide official eligibility "
                "or loan approval."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "has_vending_card": {
                        "type": "boolean",
                        "description": (
                            "Whether the user reports having "
                            "a vending card."
                        )
                    },
                    "has_aadhaar": {
                        "type": "boolean",
                        "description": (
                            "Whether the user reports having Aadhaar. "
                            "Collected as context only; it must not by "
                            "itself determine official eligibility."
                        )
                    },
                    "years_active": {
                        "type": "integer",
                        "minimum": 0,
                        "description": (
                            "Number of years the user reports "
                            "being active as a vendor."
                        )
                    },
                    "language": {
                        "type": "string",
                        "enum": ["bn", "hi", "en"]
                    }
                },
                "required": [
                    "has_vending_card",
                    "has_aadhaar",
                    "language"
                ]
            }
        }
    }
]    


# Tool dispatcher

def execute_tool(
    tool_name: str,
    arguments: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Execute a supported HawkerSathi tool by name.
    """

    try:
        if tool_name == "get_scheme_info":
            return get_scheme_info(**arguments)

        if tool_name == "check_svanidhi_eligibility":
            return check_svanidhi_eligibility(**arguments)

        return {
            "success": False,
            "error": "unknown_tool",
            "tool_name": tool_name
        }

    except TypeError as error:
        return {
            "success": False,
            "error": "invalid_tool_arguments",
            "tool_name": tool_name,
            "details": str(error)
        }

    except Exception as error:
        return {
            "success": False,
            "error": "tool_execution_failed",
            "tool_name": tool_name,
            "details": str(error)
        }


# Tool dispatcher

def execute_tool(
    tool_name: str,
    arguments: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Execute a supported HawkerSathi tool by name.
    """

    try:
        if tool_name == "get_scheme_info":
            return get_scheme_info(**arguments)

        if tool_name == "check_svanidhi_eligibility":
            return check_svanidhi_eligibility(**arguments)

        return {
            "success": False,
            "error": "unknown_tool",
            "tool_name": tool_name
        }

    except TypeError as error:
        return {
            "success": False,
            "error": "invalid_tool_arguments",
            "tool_name": tool_name,
            "details": str(error)
        }

    except Exception as error:
        return {
            "success": False,
            "error": "tool_execution_failed",
            "tool_name": tool_name,
            "details": str(error)
        }