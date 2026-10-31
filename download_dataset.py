from roboflow import Roboflow

rf = Roboflow(api_key="jfa6LsrceAB0PStpBIdt")

project = rf.workspace("anges-workspace-q0s1m").project("helmet-detection-ligfk")

dataset = project.version(4).download("yolov8")

print("Téléchargement terminé :", dataset.location)
