from ..enums import CDATA_EPON, CDATA_GPON, SLOT_ID, CARD_ID, PON_ID, ONU_ID


def _index_decoder(full_index, brand):
    if brand == CDATA_EPON:
        slot = (full_index >> 24) & 0xFF
        card = (full_index >> 16) & 0xFF
        pon = (full_index >> 8) & 0xFF
        onu = full_index & 0xFF

        return {
            SLOT_ID: slot,
            CARD_ID: card,
            PON_ID: (pon // 16) + 1,
            ONU_ID: onu,
        }
    elif brand == CDATA_GPON:
        slot = (full_index >> 24) & 0xFF
        card = (full_index >> 16) & 0xFF
        pon = (full_index >> 8) & 0xFF
        onu = full_index & 0xFF

        return {
            SLOT_ID: slot - 1 if slot > 0 else 0,
            CARD_ID: card,
            PON_ID: pon - 6,
            ONU_ID: onu,
        }


if __name__ == "__main__":
    # Example usage
    device_id = 16780858  # Example device ID
    print(_index_decoder(device_id, "CDATA-GPON"))
    # print("CDATA GPON Decoded:", decode_cdata_gpon(device_id))
