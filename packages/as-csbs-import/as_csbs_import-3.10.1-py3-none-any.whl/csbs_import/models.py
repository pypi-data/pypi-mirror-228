from as_acquisition_library import devices

from dataclasses import dataclass, field
import re
import string
from typing import Iterator, Optional

def _varname(name: str):
    name = name.strip()
    name = name.lower()
    name = name.replace("+", "_plus_")
    name = re.sub(r"[^a-z0-9_]", "_", name)
    name = re.sub(r"_+", "_", name)
    return name


@dataclass
class Node(object):
    def isAssembly(self) -> bool:
        return False

    def isLeaf(self) -> bool:
        """Returns true if this node is a full PV, i.e. an actual device with a full PV that is readable/writable."""
        return False

    def topologicalSort(self) -> Iterator["Node"]:
        for child in self.children:
            yield from child.topologicalSort()

        yield self

    def fqn(self, opa=True) -> str:
        """Returns a fully qualified name of the node."""
        parent_name = self.parent.fqn(opa)

        if parent_name:
            return parent_name + "_" + self.description
        else:
            return self.description

    def fqn_dotted_var(self) -> str:
        """Returns a fully qualified dotted name."""
        parts = []
        node = self
        while node:
            part = _varname(getattr(node, "shortname", node.description))

            assert part, "_varname should not allow an empty name"
            assert not part[0].isdigit(), f"_varname '{part}' should not allow a part to start with a digit"
            for char in part:
                assert char in string.ascii_lowercase + string.digits + "_", f"_varname '{part}' should not include: '{char}'"
            assert "__" not in part, f"_varname {part} should not allow double underscores"

            parts = [part] + parts
            node = getattr(node, "parent", None)

        for i in range(1, len(parts)):
            parts[i] = parts[i].removeprefix(parts[i - 1] + "_")

        return ".".join(parts)

@dataclass
class AssemblyType(Node):
    name: str
    pv_name: str


@dataclass
class Assembly(Node):
    name: str
    description: str
    assembly_type: AssemblyType
    parent: Node = None
    children: list = field(default_factory=list)

    def isAssembly(self) -> bool:
        return True


@dataclass
class ControllerType(Node):
    name: str
    pv_name: str


@dataclass
class Controller(Node):
    name: str
    description: str
    controller_type: ControllerType
    children: list = field(default_factory=list)

    def typeName(self) -> str:
        return self.controller_type.name

    def isLeaf(self) -> bool:
        return False


@dataclass
class DeviceType(Node):
    name: str
    pv_name: str


@dataclass
class Device(Node):
    name: str
    description: str
    device_type: DeviceType
    children: list = field(default_factory=list)

    def isLeaf(self) -> bool:
        return True

    def typeName(self) -> str:
        return self.device_type.name


@dataclass
class HostType(Node):
    name: str
    pv_name: str


@dataclass
class Host(Node):
    name: str
    description: str
    host_type: HostType
    comment: str
    children: list = field(default_factory=list)


@dataclass
class IOCType(Node):
    name: str
    pv_name: str


@dataclass
class IOC(Node):
    name: str
    description: str
    ioc_type: IOCType
    children: list = field(default_factory=list)


@dataclass
class OperationalArea(Node):
    shortname: str
    name: str
    csbsid: int
    children: list = field(default_factory=list)

    def isAssembly(self):
        return True

    def fqn(self, opa=True):
        if opa:
            return self.shortname
        else:
            return None

    @property
    def description(self):
        return self.name
