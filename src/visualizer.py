"""Модуль генерации PlantUML и отображения графа в GUI."""

import base64
import tkinter as tk
import urllib.request
import zlib


def generate_plantuml(edges):
    """Формирует текстовое описание графа на языке PlantUML."""
    lines = ["@startuml"]
    if not edges:
        lines.append("node Empty")
    for src, dst in edges:
        safe_src = src.replace("-", "_").replace(".", "_")
        safe_dst = dst.replace("-", "_").replace(".", "_")
        lines.append(f"[{safe_src}] --> [{safe_dst}]")
    lines.append("@enduml")
    return "\n".join(lines)


def encode_plantuml(puml_text):
    """Кодирует текст PlantUML для получения PNG с сервера."""
    compressed = zlib.compress(puml_text.encode("utf-8"))[2:-4]
    alphabet = (
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz-_"
    )
    res = []
    for i in range(0, len(compressed), 3):
        chunk = compressed[i : i + 3]
        res.append(_encode_bytes(chunk, alphabet))
    return "".join(res)


def _encode_bytes(chunk, alphabet):
    """Кодирует 3 байта в 4 символа алфавита PlantUML."""
    b1 = chunk[0]
    b2 = chunk[1] if len(chunk) > 1 else 0
    b3 = chunk[2] if len(chunk) > 2 else 0
    c1 = b1 >> 2
    c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
    c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
    c4 = b3 & 0x3F
    return (
        alphabet[c1] + alphabet[c2] + alphabet[c3] + alphabet[c4]
    )


def show_graph_window(puml_text):
    """Загружает PNG-изображение графа и выводит его в окне tkinter."""
    encoded = encode_plantuml(puml_text)
    url = f"http://plantuml.com{encoded}"
    raw_png = urllib.request.urlopen(url, timeout=15).read()

    root = tk.Tk()
    root.title("Граф зависимостей (PlantUML)")
    img = tk.PhotoImage(data=base64.b64encode(raw_png))
    label = tk.Label(root, image=img)
    label.image = img
    label.pack()
    root.mainloop()
