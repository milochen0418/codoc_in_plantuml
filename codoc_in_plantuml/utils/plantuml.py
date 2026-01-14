import os
import zlib


class PlantUML:
    """Helper class to handle PlantUML encoding."""

    @staticmethod
    def _encode6bit(b: int) -> str:
        if b < 10:
            return chr(48 + b)
        b -= 10
        if b < 26:
            return chr(65 + b)
        b -= 26
        if b < 26:
            return chr(97 + b)
        b -= 26
        if b == 0:
            return "-"
        if b == 1:
            return "_"
        return "?"

    @staticmethod
    def _append3bytes(b1: int, b2: int, b3: int) -> str:
        c1 = b1 >> 2
        c2 = (b1 & 3) << 4 | b2 >> 4
        c3 = (b2 & 15) << 2 | b3 >> 6
        c4 = b3 & 63
        return (
            PlantUML._encode6bit(c1)
            + PlantUML._encode6bit(c2)
            + PlantUML._encode6bit(c3)
            + PlantUML._encode6bit(c4)
        )

    @staticmethod
    def encode(text: str) -> str:
        """Encodes PlantUML text using the correct deflate + custom 6-bit algorithm."""
        if not text:
            return ""
        data = text.encode("utf-8")
        compressed = zlib.compress(data, 9)[2:-4]
        result = ""
        i = 0
        length = len(compressed)
        while i < length:
            if i + 2 < length:
                result += PlantUML._append3bytes(
                    compressed[i], compressed[i + 1], compressed[i + 2]
                )
            elif i + 1 < length:
                result += PlantUML._append3bytes(compressed[i], compressed[i + 1], 0)
            else:
                result += PlantUML._append3bytes(compressed[i], 0, 0)
            i += 3
        return result

    @staticmethod
    def get_url(text: str, format: str = "svg") -> str:
        encoded = PlantUML.encode(text)
        base = os.getenv("CODOC_PLANTUML_SERVER", "https://www.plantuml.com/plantuml")
        base = base.rstrip("/")
        return f"{base}/{format}/{encoded}"