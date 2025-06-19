from ..enums import SLOT_ID, CARD_ID, PON_ID, ONU_ID

def decode_cdata_epon(device_id):
  slot = (device_id >> 24) & 0xFF
  card = (device_id >> 16) & 0xFF
  pon = (device_id >> 8) & 0xFF
  onu = device_id & 0xFF

  return {
    SLOT_ID: slot,
    CARD_ID: card,
    PON_ID: (pon // 16) + 1,
    ONU_ID: onu,
}
    
def decode_cdata_gpon(device_id):
  slot = (device_id >> 24) & 0xFF
  card = (device_id >> 16) & 0xFF
  pon = (device_id >> 8) & 0xFF
  onu = device_id & 0xFF

  return {
    SLOT_ID: slot - 1 if slot > 0 else 0,
    CARD_ID: card,
    PON_ID: pon - 6,
    ONU_ID: onu,
}