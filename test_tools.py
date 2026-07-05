from src.tools import (
    get_scheme_info,
    check_svanidhi_eligibility
)


print("=" * 50)
print("TEST 1: Bengali PM SVANidhi")
print("=" * 50)

result_bn = get_scheme_info(
    "PM_SVANidhi",
    "bn"
)

print(result_bn)


print("\n" + "=" * 50)
print("TEST 2: Hindi PM SVANidhi")
print("=" * 50)

result_hi = get_scheme_info(
    "PM_SVANidhi",
    "hi"
)

print(result_hi)


print("\n" + "=" * 50)
print("TEST 3: Fake Scheme")
print("=" * 50)

result_fake = get_scheme_info(
    "FAKE_SCHEME",
    "bn"
)

print(result_fake)

print("\n" + "=" * 50)
print("TEST 4: Vendor Card Available")
print("=" * 50)

result_eligible = check_svanidhi_eligibility(
    has_vending_card=True,
    has_aadhaar=True,
    years_active=3,
    language="bn"
)

print(result_eligible)


print("\n" + "=" * 50)
print("TEST 5: No Card, Has Vending History")
print("=" * 50)

result_more_info = check_svanidhi_eligibility(
    has_vending_card=False,
    has_aadhaar=True,
    years_active=4,
    language="bn"
)

print(result_more_info)


print("\n" + "=" * 50)
print("TEST 6: Insufficient Information")
print("=" * 50)

result_verify = check_svanidhi_eligibility(
    has_vending_card=False,
    has_aadhaar=False,
    years_active=0,
    language="hi"
)

print(result_verify)


print("\n" + "=" * 50)
print("TEST 7: Invalid Years")
print("=" * 50)

result_invalid = check_svanidhi_eligibility(
    has_vending_card=True,
    has_aadhaar=True,
    years_active=-2,
    language="en"
)

print(result_invalid)