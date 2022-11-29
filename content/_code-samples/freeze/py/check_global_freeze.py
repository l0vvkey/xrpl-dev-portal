from xrpl.clients import JsonRpcClient
from xrpl.models import AccountInfo

client = JsonRpcClient("https://s.altnet.rippletest.net:51234") # Connect to testnetwork


ACCOUNT_ROOT_LEDGER_FLAGS: dict[str, int] = {
        "lsfNoFreeze": 0x00200000,
        "lsfGlobalFreeze": 0x00400000,
    }

def parse_account_root_flags(flags: int) -> list[str]:
    flags_enabled = []
    for flag in ACCOUNT_ROOT_LEDGER_FLAGS:
        check_flag = ACCOUNT_ROOT_LEDGER_FLAGS[flag]
        if check_flag & flags == check_flag:
            flags_enabled.append(flag)
    return flags_enabled

# Issuer address to query for global freeze status
issuer_addr = "rfDJ98Z8k7ubr6atbZoCqAPdg9MetyBwcg"

# Build account line query
print(f"Checking if global freeze is enabled for the address {issuer_addr}")
acc_info = AccountInfo(account=issuer_addr, ledger_index="validated")

# Submit query
response = client.request(acc_info)

# Parse response for result
result = response.result

# Query result for global freeze status
if "account_data" in result:
    if "Flags" in result["account_data"]:
        if "lsfGlobalFreeze" in parse_account_root_flags(result["account_data"]["Flags"]):
            print("Global Freeze is enabled")
        else:
            print("Global Freeze is disabled")
