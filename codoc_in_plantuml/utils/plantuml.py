import base64
import os
import subprocess
import zlib
from pathlib import Path
from urllib.request import urlopen


class PlantUML:
    """Helper class to handle PlantUML encoding."""

    _DEFAULT_JAR_URL = os.getenv(
        "CODOC_PLANTUML_JAR_URL",
        #"https://github.com/plantuml/plantuml/releases/download/v1.2026.1/plantuml-1.2026.1.jar",
        "https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar",
    )

    @staticmethod
    def _default_jar_path() -> Path:
        repo_root = Path(__file__).resolve().parents[2]
        return Path(
            os.getenv(
                "CODOC_PLANTUML_JAR_PATH",
                str(repo_root / ".cache" / "plantuml" / "plantuml.jar"),
            )
        )

    @staticmethod
    def _ensure_jar() -> Path:
        jar_path = PlantUML._default_jar_path()
        if jar_path.exists():
            return jar_path
        jar_path.parent.mkdir(parents=True, exist_ok=True)
        with urlopen(PlantUML._DEFAULT_JAR_URL, timeout=30) as response:
            jar_path.write_bytes(response.read())
        return jar_path

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

    @staticmethod
    def _render_with_jar(text: str, format: str = "svg") -> bytes:
        if not text:
            return b""
        jar_path = PlantUML._ensure_jar()
        result = subprocess.run(
            ["java", "-jar", str(jar_path), f"-t{format}", "-pipe"],
            input=text.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"PlantUML render failed: {result.stderr.decode('utf-8', errors='ignore')}"
            )
        return result.stdout

    @staticmethod
    def _to_data_url(content: bytes, format: str) -> str:
        if not content:
            return ""
        mime = "image/svg+xml" if format == "svg" else f"image/{format}"
        encoded = base64.b64encode(content).decode("ascii")
        return f"data:{mime};base64,{encoded}"

    @staticmethod
    def get_image_source(text: str, format: str = "svg") -> str:
        use_jar = os.getenv("CODOC_PLANTUML_USE_JAR", "").lower() in {"1", "true", "yes"}
        if use_jar:
            return PlantUML._to_data_url(PlantUML._render_with_jar(text, format), format)
        return PlantUML.get_url(text, format)