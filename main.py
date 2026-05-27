
import plotly.graph_objects as go
import urllib.request, json
import csv
from models.application_snapshot import ApplicationSnapshot
from collections import Counter

def get_job_applications(filename: str = 'applications.csv') -> list[ApplicationSnapshot]:
    job_applications = []
    with open(filename, newline='') as file:
        reader = csv.reader(file)
        for job_application in reader:
            company, date_applied, status = job_application[0], job_application[1], job_application[2]
            job_applications.append(ApplicationSnapshot(company, date_applied, status))
    
    return job_applications

def get_link_color(source: str, target: str) -> str:
    if target == "Rejected":
        return "rgba(255,80,80,0.35)"
    if target == "Offer":
        return "rgba(80,200,120,0.35)"
    if target.startswith("Interview"):
        return "rgba(80,140,255,0.35)"
    return "rgba(160,160,160,0.25)"

def create_sankey_diagram(applications: list[ApplicationSnapshot]) -> None:
    edge_counts = Counter()
    for application in applications:
        path = application.status_path

        if len(path) < 2:
            continue

        for src, dst in zip(path, path[1:]):
            edge_counts[(src, dst)] += 1

    node_value_lookup = {
                        "Applied":0,
                        "Interview 1":1,
                        "Interview 2":2,
                        "Interview 3":3,
                        "Interview 4":4,
                        "Interview 5":5,
                        "Interview 6":6,
                        "Rejected":7,
                        "Ghosted":8,
                        "Offer":9
    }

    source = []
    target = []
    value = []
    color = []

    for (src, dst), val in edge_counts.items():
        source.append(node_value_lookup[src])
        target.append(node_value_lookup[dst])
        value.append(val)
        color.append(get_link_color(src, dst))

    fig = go.Figure(
        data=[
            go.Sankey(
                valueformat=".0f",

                node=dict(
                    pad=15,
                    thickness=15,
                    line=dict(color="black", width=0.5),
                    label=[
                        "Applied",
                        "Interview 1",
                        "Interview 2",
                        "Interview 3",
                        "Interview 4",
                        "Interview 5",
                        "Interview 6",
                        "Rejected",
                        "Ghosted",
                        "Offer"
                    ],
                    color="black"
                ),

                link=dict(
                    source=source,
                    target=target,
                    value=value,
                    color=color
                )
            )
        ]
    )

    fig.update_layout(title_text="Job Applications", font_size=10)
    fig.show()

if __name__ == "__main__":
    applications = get_job_applications('applications.csv')

    create_sankey_diagram(applications)


