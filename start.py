import os
import json
import argparse
import hyperdiv as hd

parser = argparse.ArgumentParser()
parser.add_argument("--predictions", help="Path to predictions JSON file", default="predictions.json")
parser.add_argument("--output", help="Path to output JSON file", default="output.json")
args = parser.parse_args()

predictions_json = args.predictions
output_json = args.output

with open(predictions_json, "r") as f:
    predictions = json.load(f)
try:
    with open(output_json, "r") as f:
        output = json.load(f)
except FileNotFoundError:
    output = {}

# Rest of the code...

with open(predictions_json, "r") as f:
    predictions = json.load(f)

try:
    with open(output_json, "r") as f:
        output = json.load(f)
except FileNotFoundError:
    output = {}

# Find all possible labels from predictions json and output json
labels = set()
for predictions_for_file in predictions.values():
    for prediction in predictions_for_file:
        labels.add(prediction["label"])

for label in output.keys():
    labels.add(label)

labels = list(sorted(labels))

# Find all files that have not been reviewed yet
files = set()
for file in predictions.keys():
    files.add(file)

reviewed_in_past = 0
for files_in_label in output.values():
    for file in files_in_label:
        reviewed_in_past += 1
        files.remove(file)

files = list(sorted(files))


class useKeyboard(hd.Plugin):
    _assets_root = os.path.join(os.path.dirname(__file__), "plugins")
    _assets = ["useKeyboard.js"]

    keyName = hd.Prop(hd.String, "")


def main():
    state = hd.state(index=0, selection=-1)

    def next_image():
        label = labels[state.selection]
        if label not in output:
            output[label] = []
        output[label].append(files[state.index])
        with open(output_json, "w") as f:
            json.dump(output, f, indent=4)

        state.selection = -1
        state.index = min(state.index + 1, len(files) - 1)

    def doKeyboardAction(keyName):
        if keyName == "ArrowRight":
            next_image()
        elif keyName == "ArrowUp":
            state.selection = (state.selection - 1) % len(labels)
        elif keyName == "ArrowDown":
            state.selection = (state.selection + 1) % len(labels)
        else:
            return
        keyboard.keyName = ""

    keyboard = useKeyboard()
    if keyboard.keyName:
        doKeyboardAction(keyboard.keyName)

    template = hd.template(title="Classification Review Tool", sidebar=False)
    with template.body:
        with hd.hbox():
            with hd.vbox():
                hd.text(files[state.index])
                with open(files[state.index], "rb") as im:
                    hd.image(im.read(), max_height="80vh")
            with hd.hbox(justify="end", grow=True):
                with hd.vbox(gap=2):
                    if state.selection == -1:
                        state.selection = labels.index(
                            predictions[files[state.index]][0]["label"]
                        )
                    with hd.radio_group(value=state.selection):
                        for i in range(len(labels)):
                            with hd.scope(i):
                                with hd.hbox(gap=1):
                                    hd.radio(f"{i}", value=i, min_width="50px")
                                    with hd.box(min_width="200px", text_align="end"):
                                        hd.text(labels[i])
                                    score = 0.001
                                    for prediction in predictions[files[state.index]]:
                                        if prediction["label"] == labels[i]:
                                            score = prediction["score"]
                                    hd.text(f"{score:.2f}")
                                    BAR_WIDTH = 20
                                    hd.box(
                                        width=score * BAR_WIDTH,
                                        height="1em",
                                        background_color="blue",
                                    )
                                    hd.box(width=(1 - score) * BAR_WIDTH, height="1em")

                    with hd.hbox(gap=1):
                        with hd.vbox():
                            hd.text(f"Reviewed in Current Session:")
                            hd.text(f"Reviewed Earlier:")
                            hd.text(f"Unreviewed:")
                        with hd.vbox():
                            hd.text(f"{state.index}")
                            hd.text(f"{reviewed_in_past}")
                            hd.text(f"{len(files) - state.index}")
                            
                    if hd.button("Next Image", suffix_icon="chevron-right").clicked:
                        next_image()

hd.run(main)
