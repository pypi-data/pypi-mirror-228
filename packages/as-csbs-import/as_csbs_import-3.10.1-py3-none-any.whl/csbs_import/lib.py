from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import requests

from .models import (
    Assembly,
    AssemblyType,
    Controller,
    ControllerType,
    Device,
    DeviceType,
    Host,
    HostType,
    IOC,
    IOCType,
    OperationalArea,
)

DEFAULT_OPA_URL = "https://ec-csbs-ui-prod.asci.synchrotron.org.au/api/v1/operational_area"
DEFAULT_DATA_URL_FMT = (
    "https://ec-csbs-ui-prod.asci.synchrotron.org.au/api/v1/operational_area"
    + "/{area}/init?path_mode=Final"
)


def get_operational_area_details(
    opa: OperationalArea, session: requests.Session, csbs_data_url: str
) -> None:
    """Fetch and parse data from the csbs_data_url and pouplate the passed opa."""
    r = session.get(csbs_data_url)

    data = r.json()["data"]

    types: dict[str, dict] = {
        "assembly_type": {},
        "controller_type": {},
        "device_type": {},
        "host_type": {},
        "ioc_type": {},
        "operational_area": {},
    }
    nodes: dict[str, dict] = {
        "Assembly": {},
        "Controller": {},
        "Device": {},
        "Host": {},
        "Ioc": {},
        "OperationalArea": {},
    }

    for node in data["operational_area"]:
        csbsid = node["id"]
        nodes["OperationalArea"][csbsid] = OperationalArea(node["short_name"], node["name"], csbsid)

    for node in data["assembly_type"]:
        types["assembly_type"][node["id"]] = AssemblyType(node["name"], node["pv_name"])

    for node in data["controller_type"]:
        types["controller_type"][node["id"]] = ControllerType(node["name"], node["pv_name"])

    for node in data["device_type"]:
        types["device_type"][node["id"]] = DeviceType(node["name"], node["pv_name"])

    for node in data["host_type"]:
        types["host_type"][node["id"]] = HostType(node["name"], node["pv_name"])

    for node in data["ioc_type"]:
        types["ioc_type"][node["id"]] = IOCType(node["name"], node["pv_name"])

    for node in data["instances"]["children"]["Assembly"]:
        nodes["Assembly"][node["id"]] = Assembly(
            node["name"], node["description"], types["assembly_type"][node["assembly_type"]]
        )

    for node in data["instances"]["children"]["Controller"]:
        nodes["Controller"][node["id"]] = Controller(
            node["name"], node["description"], types["controller_type"][node["controller_type"]]
        )

    for node in data["instances"]["children"]["Device"]:
        nodes["Device"][node["id"]] = Device(
            node["name"], node["description"], types["device_type"][node["device_type"]]
        )

    for node in data["instances"]["children"]["Host"]:
        nodes["Host"][node["id"]] = Host(
            node["name"],
            node["description"],
            types["host_type"][node["host_type"]],
            node["comment"],
        )

    for node in data["instances"]["children"]["Ioc"]:
        nodes["Ioc"][node["id"]] = IOC(
            node["name"], node["description"], types["ioc_type"][node["ioc_type"]]
        )

    for path in data["instances"]["children"]["Path"]:

        if path["entity_type"] == "Channel":
            continue

        if path["parent_type"] == "Channel":
            continue

        child = nodes[path["entity_type"]][path["entity_id"]]
        parent = nodes[path["parent_type"]][path["parent_id"]]

        parent.children.append(child)
        child.parent = parent

    opa.children = nodes["OperationalArea"][opa.csbsid].children


def get_operational_areas(session: requests.Session, opa_url: str) -> list[OperationalArea]:
    """Fetch CSBS operational data, return a list of Operational areas."""
    res = []
    r = session.get(opa_url)
    for opa in r.json()["data"]:
        res.append(OperationalArea(opa["short_name"], opa["name"], opa["id"]))

    return res
