from src.tools import get_scheme_info


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