from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)

def generate_pdf(results: dict, output_file: str = "report.pdf") -> None:
    """Generate a PDF report from the scan results."""
    try:
        c = canvas.Canvas(output_file, pagesize=letter)
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
        logger.info(f"PDF report generated at {output_file}.")
    except Exception as e:
        logger.error(f"Error generating PDF report: {e}")

def generate_visualizations(results: dict) -> None:
    """Generate visualizations (e.g., bar charts) from the scan results."""
    try:
        for target, data in results.items():
            if 'scan' in data:
                ports = [service['port'] for service in data['scan']['services']]
                if ports:
                    plt.bar(range(len(ports)), ports)
                    plt.xlabel('Ports')
                    plt.ylabel('Frequency')
                    plt.title(f'Open Ports for {target}')
                    plt.savefig(f'{target}_ports.png')
                    plt.clf()
        logger.info("Visualizations generated.")
    except Exception as e:
        logger.error(f"Error generating visualizations: {e}")

def generate_report(results: dict, output_file: str = "report.pdf") -> None:
    """Generate a full report including a PDF and visualizations."""
    generate_pdf(results, output_file)
    generate_visualizations(results)
    logger.info("Full report generated.")
