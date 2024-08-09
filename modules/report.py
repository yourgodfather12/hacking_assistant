from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt

def generate_pdf(results):
    c = canvas.Canvas("report.pdf", pagesize=letter)
    width, height = letter
    c.drawString(100, height - 100, "Hacking Assistant Report")
    y = height - 150
    for target, data in results.items():
        c.drawString(100, y, f"Target: {target}")
        y -= 20
        for key, value in data.items():
            c.drawString(120, y, f"{key.capitalize()}: {value}")
            y -= 20
        y -= 10
    c.save()

def generate_visualizations(results):
    for target, data in results.items():
        if 'scan' in data:
            ports = [service['port'] for service in data['scan']['services']]
            plt.bar(range(len(ports)), ports)
            plt.xlabel('Ports')
            plt.ylabel('Frequency')
            plt.title(f'Open Ports for {target}')
            plt.savefig(f'{target}_ports.png')
            plt.clf()

def generate_report(results):
    generate_pdf(results)
    generate_visualizations(results)
