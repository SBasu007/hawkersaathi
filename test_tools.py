from src.tools import (
    get_scheme_info,
    check_svanidhi_eligibility,
    execute_tool,
    TOOLS
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


print("\n" + "=" * 50)
print("TEST 8: Dispatcher - Scheme Lookup")
print("=" * 50)

result_dispatch_scheme = execute_tool(
    "get_scheme_info",
    {
        "scheme_name": "PM_SVANidhi",
        "language": "bn"
    }
)

print(result_dispatch_scheme)


print("\n" + "=" * 50)
print("TEST 9: Dispatcher - Eligibility")
print("=" * 50)

result_dispatch_eligibility = execute_tool(
    "check_svanidhi_eligibility",
    {
        "has_vending_card": True,
        "has_aadhaar": True,
        "years_active": 3,
        "language": "hi"
    }
)

print(result_dispatch_eligibility)


print("\n" + "=" * 50)
print("TEST 10: Unknown Tool")
print("=" * 50)

result_unknown_tool = execute_tool(
    "fake_tool",
    {}
)

print(result_unknown_tool)


print("\n" + "=" * 50)
print("TEST 11: Invalid Tool Arguments")
print("=" * 50)

result_invalid_args = execute_tool(
    "get_scheme_info",
    {
        "wrong_argument": "hello"
    }
)

print(result_invalid_args)


print("\n" + "=" * 50)
print("TEST 12: Tool Definitions")
print("=" * 50)

for tool in TOOLS:
    print(
        "Tool:",
        tool["function"]["name"]
    )