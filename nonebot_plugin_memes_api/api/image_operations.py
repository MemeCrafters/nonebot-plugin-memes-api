from typing import Optional

from nonebot.compat import type_validate_python
from pydantic import BaseModel

from . import ImageResponse, ImagesResponse, get_image, send_request, upload_image


class ImageInfo(BaseModel):
    width: int
    height: int
    is_multi_frame: bool
    frame_count: Optional[int]
    average_duration: Optional[float]


async def inspect(image: bytes) -> ImageInfo:
    image_id = await upload_image(image)
    payload = {"image_id": image_id}

    return type_validate_python(
        ImageInfo,
        await send_request(
            "/tools/image_operations/inspect", "POST", "JSON", json=payload
        ),
    )


async def flip_horizontal(image: bytes) -> bytes:
    image_id = await upload_image(image)
    payload = {"image_id": image_id}

    image_id = type_validate_python(
        ImageResponse,
        await send_request(
            "/tools/image_operations/flip_horizontal", "POST", "JSON", json=payload
        ),
    ).image_id
    return await get_image(image_id)


async def flip_vertical(image: bytes) -> bytes:
    image_id = await upload_image(image)
    payload = {"image_id": image_id}

    image_id = type_validate_python(
        ImageResponse,
        await send_request(
            "/tools/image_operations/flip_vertical", "POST", "JSON", json=payload
        ),
    ).image_id
    return await get_image(image_id)


async def rotate(image: bytes, degrees: Optional[float]) -> bytes:
    image_id = await upload_image(image)
    payload = {"image_id": image_id, "degrees": degrees}

    image_id = type_validate_python(
        ImageResponse,
        await send_request(
            "/tools/image_operations/rotate", "POST", "JSON", json=payload
        ),
    ).image_id
    return await get_image(image_id)


async def resize(image: bytes, width: Optional[int], height: Optional[int]) -> bytes:
    image_id = await upload_image(image)
    payload = {"image_id": image_id, "width": width, "height": height}

    image_id = type_validate_python(
        ImageResponse,
        await send_request(
            "/tools/image_operations/resize", "POST", "JSON", json=payload
        ),
    ).image_id
    return await get_image(image_id)


async def crop(
    image: bytes,
    left: Optional[int],
    top: Optional[int],
    right: Optional[int],
    bottom: Optional[int],
) -> bytes:
    image_id = await upload_image(image)
    payload = {
        "image_id": image_id,
        "left": left,
        "top": top,
        "right": right,
        "bottom": bottom,
    }

    image_id = type_validate_python(
        ImageResponse,
        await send_request(
            "/tools/image_operations/crop", "POST", "JSON", json=payload
        ),
    ).image_id
    return await get_image(image_id)


async def grayscale(image: bytes) -> bytes:
    image_id = await upload_image(image)
    payload = {"image_id": image_id}

    image_id = type_validate_python(
        ImageResponse,
        await send_request(
            "/tools/image_operations/grayscale", "POST", "JSON", json=payload
        ),
    ).image_id
    return await get_image(image_id)


async def invert(image: bytes) -> bytes:
    image_id = await upload_image(image)
    payload = {"image_id": image_id}

    image_id = type_validate_python(
        ImageResponse,
        await send_request(
            "/tools/image_operations/invert", "POST", "JSON", json=payload
        ),
    ).image_id
    return await get_image(image_id)


async def merge_horizontal(images: list[bytes]) -> bytes:
    payload = {"image_ids": [await upload_image(image) for image in images]}

    image_id = type_validate_python(
        ImageResponse,
        await send_request(
            "/tools/image_operations/merge_horizontal", "POST", "JSON", json=payload
        ),
    ).image_id
    return await get_image(image_id)


async def merge_vertical(images: list[bytes]) -> bytes:
    payload = {"image_ids": [await upload_image(image) for image in images]}

    image_id = type_validate_python(
        ImageResponse,
        await send_request(
            "/tools/image_operations/merge_vertical", "POST", "JSON", json=payload
        ),
    ).image_id
    return await get_image(image_id)


async def gif_split(image: bytes) -> list[bytes]:
    image_id = await upload_image(image)
    payload = {"image_id": image_id}

    return [
        await get_image(image_id)
        for image_id in type_validate_python(
            ImagesResponse,
            await send_request(
                "/tools/image_operations/gif_split", "POST", "JSON", json=payload
            ),
        ).image_ids
    ]


async def gif_merge(images: list[bytes], duration: Optional[float]) -> bytes:
    payload = {
        "image_ids": [await upload_image(image) for image in images],
        "duration": duration,
    }

    image_id = type_validate_python(
        ImageResponse,
        await send_request(
            "/tools/image_operations/gif_merge", "POST", "JSON", json=payload
        ),
    ).image_id
    return await get_image(image_id)


async def gif_reverse(image: bytes) -> bytes:
    image_id = await upload_image(image)
    payload = {"image_id": image_id}

    image_id = type_validate_python(
        ImageResponse,
        await send_request(
            "/tools/image_operations/gif_reverse", "POST", "JSON", json=payload
        ),
    ).image_id
    return await get_image(image_id)


async def gif_change_duration(image: bytes, duration: float) -> bytes:
    image_id = await upload_image(image)
    payload = {"image_id": image_id, "duration": duration}

    image_id = type_validate_python(
        ImageResponse,
        await send_request(
            "/tools/image_operations/gif_change_duration", "POST", "JSON", json=payload
        ),
    ).image_id
    return await get_image(image_id)
