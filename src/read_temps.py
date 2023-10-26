from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from time import sleep

import psutil
import PySimpleGUI as sG


def call_temp():
    return psutil.sensors_temperatures()


@dataclass
class GUI:
    bg_color = "#404040"
    acpitz = [
        sG.Text("acpitz:", background_color=bg_color),
        sG.Text("", key="-ACPITZ-", background_color=bg_color),
    ]
    k10temp = [
        sG.Text("k10temp:", background_color=bg_color),
        sG.Text("", key="-K10TEMP-", background_color=bg_color),
    ]
    core = [
        sG.Text("amdgpu:", background_color=bg_color),
        sG.Text("", key="-CORE-", background_color=bg_color),
    ]
    start_stop = [
        sG.Button(
            "Start",
            key="-START-",
            button_color=bg_color,
            highlight_colors=("#FFFFFF", "#4a4949"),
        )
    ]
    layout = [acpitz, k10temp, core, start_stop]


def logic(window):
    window["-START-"].update(disabled=True)
    while True:
        temps = call_temp()

        acpitz = temps.get("acpitz")
        k10temp = temps.get("k10temp")
        amdgpu = temps.get("amdgpu")

        acpi_data = acpitz[0]
        k10temp = k10temp[0]
        core = amdgpu[1]

        window["-ACPITZ-"].update(acpi_data.current)
        window["-K10TEMP-"].update(k10temp.current)
        window["-CORE-"].update(core.current)
        sleep(1)


def main_app():
    sG.theme("Dark")
    print(sG.LOOK_AND_FEEL_TABLE.get("Dark"))
    gui = GUI()
    window = sG.Window(
        "temps",
        layout=gui.layout,
        finalize=True,
        text_justification="left",
        margins=(5, 5),
        element_padding=5,
        size=(165, 130),
        font="UbuntuMono 10 bold",
    )
    while True:
        event, values = window.read()
        if event == sG.WIN_CLOSED:
            break
        if event == "-START-":
            thread = ThreadPoolExecutor()
            thread.submit(logic, window)
    window.close()


if __name__ == "__main__":
    main_app()
