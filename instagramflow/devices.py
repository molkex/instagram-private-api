"""
Hardware preset database and device profile catalog for authentic mobile emulation.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class DevicePreset:
    name: str
    platform: str
    manufacturer: str
    model: str
    device_code: str
    os_version: str
    os_release: str
    dpi: str
    resolution: str
    scale: float
    chipset: str
    capabilities: str
    app_version: str = "446.0.0.32.78"

DEVICE_CATALOG: Dict[str, DevicePreset] = {
    "iphone_15_pro": DevicePreset(
        name="iPhone 15 Pro",
        platform="iOS",
        manufacturer="Apple",
        model="iPhone 15 Pro",
        device_code="iPhone16,1",
        os_version="17_6_1",
        os_release="iOS 17.6.1",
        dpi="460dpi",
        resolution="1179x2556",
        scale=3.0,
        chipset="Apple A17 Pro",
        capabilities="3brTv10=",
    ),
    "iphone_15_pro_max": DevicePreset(
        name="iPhone 15 Pro Max",
        platform="iOS",
        manufacturer="Apple",
        model="iPhone 15 Pro Max",
        device_code="iPhone16,2",
        os_version="17_6_1",
        os_release="iOS 17.6.1",
        dpi="460dpi",
        resolution="1290x2796",
        scale=3.0,
        chipset="Apple A17 Pro",
        capabilities="3brTv10=",
    ),
    "iphone_14_pro": DevicePreset(
        name="iPhone 14 Pro",
        platform="iOS",
        manufacturer="Apple",
        model="iPhone 14 Pro",
        device_code="iPhone15,2",
        os_version="17_5_1",
        os_release="iOS 17.5.1",
        dpi="460dpi",
        resolution="1179x2556",
        scale=3.0,
        chipset="Apple A16 Bionic",
        capabilities="3brTv10=",
    ),
    "pixel_8_pro": DevicePreset(
        name="Google Pixel 8 Pro",
        platform="Android",
        manufacturer="Google",
        model="Pixel 8 Pro",
        device_code="husky",
        os_version="34",
        os_release="14",
        dpi="480dpi",
        resolution="1344x2992",
        scale=2.8,
        chipset="Google Tensor G3",
        capabilities="3brTv10=",
    ),
    "galaxy_s24_ultra": DevicePreset(
        name="Samsung Galaxy S24 Ultra",
        platform="Android",
        manufacturer="samsung",
        model="SM-S928B",
        device_code="e3q",
        os_version="34",
        os_release="14",
        dpi="500dpi",
        resolution="1440x3120",
        scale=3.0,
        chipset="qcom;Snapdragon 8 Gen 3",
        capabilities="3brTv10=",
    ),
    "galaxy_a34_5g": DevicePreset(
        name="Samsung Galaxy A34 5G",
        platform="Android",
        manufacturer="samsung",
        model="SM-A346B",
        device_code="a34x",
        os_version="34",
        os_release="14",
        dpi="450dpi",
        resolution="1080x2400",
        scale=2.6,
        chipset="mt6877;MediaTek Dimensity 1080",
        capabilities="3brTv10=",
    ),
}

def get_device(preset_key: str = "iphone_15_pro") -> DevicePreset:
    """Retrieve hardware profile by preset identifier."""
    key = preset_key.lower().replace("-", "_")
    return DEVICE_CATALOG.get(key, DEVICE_CATALOG["iphone_15_pro"])

def list_presets() -> list[str]:
    """Return available device preset identifiers."""
    return list(DEVICE_CATALOG.keys())
