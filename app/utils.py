from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def format_mac(hex_mac):
    clean_mac = hex_mac.replace(" ", "")
    formatted_mac = ":".join(
        [clean_mac[i : i + 2] for i in range(0, len(clean_mac), 2)]
    )
    return formatted_mac


def resolve_oid(oid, mib_view):
    try:
        oid_obj = ObjectIdentity(oid)
        oid_obj.resolve_with_mib(mib_view)
        return oid_obj.prettyPrint()
    except Exception:
        try:
            mib_node = mib_view.get_node_name(oid)
            module_name = mib_node[0]
            obj_name = mib_node[1]
            indices = list(oid[len(mib_view.get_node_oid(mib_node)) :])
            index_str = "." + ".".join(map(str, indices)) if indices else ""
            return f"{module_name}::{obj_name}{index_str}"
        except Exception:
            return oid.prettyPrint()
