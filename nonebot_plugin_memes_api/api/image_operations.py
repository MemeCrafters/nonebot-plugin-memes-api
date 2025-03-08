import base64
from typing import Optional

from nonebot.compat import type_validate_python
from pydantic import BaseModel

from . import send_request


def image_data(data: bytes) -> dict:
    return {
        "type": "data",
        "data": base64.b64encode(data).decode(),
    }


class ImageInfo(BaseModel):
    width: int
    height: int
    is_multi_frame: bool
    frame_count: Optional[int]
    average_duration: Optional[float]


async def inspect(image: bytes) -> ImageInfo:
    payload = {"image": image_data(image)}

    return type_validate_python(
        ImageInfo,
        await send_request(
            "/meme/tools/image_operations/inspect", "POST", "JSON", json=payload
        ),
    )


async def flip_horizontal(image: bytes) -> bytes:
    payload = {"image": image_data(image)}

    return await send_request(
        "/meme/tools/image_operations/flip_horizontal", "POST", "BYTES", json=payload
    )


async def flip_vertical(image: bytes) -> bytes:
    payload = {"image": image_data(image)}

    return await send_request(
        "/meme/tools/image_operations/flip_vertical", "POST", "BYTES", json=payload
    )


async def rotate(image: bytes, degrees: Optional[float]) -> bytes:
    payload = {"image": image_data(image), "degrees": degrees}

    return await send_request(
        "/meme/tools/image_operations/rotate", "POST", "BYTES", json=payload
    )


async def resize(image: bytes, width: Optional[int], height: Optional[int]) -> bytes:
    payload = {"image": image_data(image), "width": width, "height": height}

    return await send_request(
        "/meme/tools/image_operations/resize", "POST", "BYTES", json=payload
    )


async def crop(
    image: bytes,
    left: Optional[int],
    top: Optional[int],
    right: Optional[int],
    bottom: Optional[int],
) -> bytes:
    payload = {
        "image": image_data(image),
        "left": left,
        "top": top,
        "right": right,
        "bottom": bottom,
    }

    return await send_request(
        "/meme/tools/image_operations/crop", "POST", "BYTES", json=payload
    )


async def grayscale(image: bytes) -> bytes:
    payload = {"image": image_data(image)}

    return await send_request(
        "/meme/tools/image_operations/grayscale", "POST", "BYTES", json=payload
    )


async def invert(image: bytes) -> bytes:
    payload = {"image": image_data(image)}

    return await send_request(
        "/meme/tools/image_operations/invert", "POST", "BYTES", json=payload
    )


async def merge_horizontal(images: list[bytes]) -> bytes:
    payload = {"images": [image_data(image) for image in images]}

    return await send_request(
        "/meme/tools/image_operations/merge_horizontal", "POST", "BYTES", json=payload
    )


async def merge_vertical(images: list[bytes]) -> bytes:
    payload = {"images": [image_data(image) for image in images]}
    return await send_request(
        "/meme/tools/image_operations/merge_vertical", "POST", "BYTES", json=payload
    )


async def gif_split(image: bytes) -> list[bytes]:
    payload = {"image": image_data(image)}

    return [
        base64.b64decode(data)
        for data in await send_request(
            "/meme/tools/image_operations/gif_split", "POST", "JSON", json=payload
        )
    ]


async def gif_merge(images: list[bytes], duration: Optional[float]) -> bytes:
    payload = {
        "images": [image_data(image) for image in images],
        "duration": duration,
    }

    return await send_request(
        "/meme/tools/image_operations/gif_merge", "POST", "BYTES", json=payload
    )


async def gif_reverse(image: bytes) -> bytes:
    payload = {"image": image_data(image)}

    return await send_request(
        "/meme/tools/image_operations/gif_reverse", "POST", "BYTES", json=payload
    )


async def gif_change_duration(image: bytes, duration: float) -> bytes:
    payload = {"image": image_data(image), "duration": duration}

    return await send_request(
        "/meme/tools/image_operations/gif_change_duration",
        "POST",
        "BYTES",
        json=payload,
    )
