from typing import TYPE_CHECKING, List

from systemrdl.rdltypes import OnReadType

from .bases import NextStateConditional

if TYPE_CHECKING:
    from systemrdl.node import FieldNode

class _OnRead(NextStateConditional):
    onreadtype = None
    def is_match(self, field: 'FieldNode') -> bool:
        return field.get_property("onread") == self.onreadtype

    def get_predicate(self, field: 'FieldNode') -> str:
        strb = self.exp.dereferencer.get_access_strobe(field)
        return f"{strb} && !decoded_req_is_wr"


class ClearOnRead(_OnRead):
    comment = "SW clear on read"
    onreadtype = OnReadType.rclr

    def get_assignments(self, field: 'FieldNode') -> List[str]:
        field_path = self.get_field_path(field)
        return [
            f"field_combo.{field_path}.next = '0;",
            f"field_combo.{field_path}.load_next = '1;",
        ]


class SetOnRead(_OnRead):
    comment = "SW set on read"
    onreadtype = OnReadType.rset

    def get_assignments(self, field: 'FieldNode') -> List[str]:
        field_path = self.get_field_path(field)
        return [
            f"field_combo.{field_path}.next = '1;",
            f"field_combo.{field_path}.load_next = '1;",
        ]