import os
import re
import json
from typing import List, Optional
from modules import (
    nmap_scan,
    info_gathering,
    vulnerability_scan,
    exploit_module,
    report,
    phishing,
    social_engineering
)
from utils import logger, scheduler, database, api, workflow
from rich.console import Console
from textual.app import App
from textual.widgets import Header, Footer, Button, TextInput
from textual.layouts import GridLayout
import asyncio

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

class HackingAssistantApp(App):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine

    async def on_load(self):
        await self.bind("q", "quit", "Quit")
        await self.bind("h", "show_help", "Help")

    async def on_mount(self):
        header = Header()
        footer = Footer()
        self.grid = GridLayout()
        await self.view.dock(header, edge="top")
        await self.view.dock(footer, edge="bottom")
        await self.view.dock(self.grid, edge="top")

        self.grid.add_column("col", repeat=2)
        self.grid.add_row("row", repeat=5)
        self.grid.add_areas(
            target_input="col1,row1",
            add_target_btn="col2,row1",
            scan_btn="col1,row2",
            info_btn="col2,row2",
            vuln_btn="col1,row3",
            exploit_btn="col2,row3",
            report_btn="col1,row4",
            schedule_btn="col2,row4",
            phish_btn="col1,row5",
            social_btn="col2,row5"
        )

        # User input for target (IP/URL)
        self.target_input = TextInput(placeholder="Enter target IP/URL")
        self.grid.place(target_input=self.target_input)

        # Buttons for various tasks
        self.add_target_btn = Button(label="Add Target", name="add_target_btn")
        self.scan_btn = Button(label="Run Scan", name="scan_btn")
        self.info_btn = Button(label="Run Info Gathering", name="info_btn")
        self.vuln_btn = Button(label="Run Vulnerability Scan", name="vuln_btn")
        self.exploit_btn = Button(label="Run Exploit", name="exploit_btn")
        self.report_btn = Button(label="Generate Report", name="report_btn")
        self.schedule_btn = Button(label="Schedule Scan", name="schedule_btn")
        self.phish_btn = Button(label="Run Phishing Attack", name="phish_btn")
        self.social_btn = Button(label="Run Social Engineering Attack", name="social_btn")

        self.grid.place(
            add_target_btn=self.add_target_btn,
            scan_btn=self.scan_btn,
            info_btn=self.info_btn,
            vuln_btn=self.vuln_btn,
            exploit_btn=self.exploit_btn,
            report_btn=self.report_btn,
            schedule_btn=self.schedule_btn,
            phish_btn=self.phish_btn,
            social_btn=self.social_btn
        )

        # Binding buttons to their respective actions
        self.add_target_btn.on_click = self.add_target
        self.scan_btn.on_click = lambda: self.run_task(self.engine.run_scan, "scan")
        self.info_btn.on_click = lambda: self.run_task(self.engine.run_info_gathering, "info gathering")
        self.vuln_btn.on_click = lambda: self.run_task(self.engine.run_vulnerability_scan, "vulnerability scan")
        self.exploit_btn.on_click = self.run_exploit
        self.report_btn.on_click = lambda: self.run_task(self.engine.generate_report, "report generation")
        self.schedule_btn.on_click = self.schedule_scan
        self.phish_btn.on_click = self.run_phishing_attack
        self.social_btn.on_click = self.run_social_engineering_attack

    async def add_target(self):
        target = self.target_input.value.strip()
        if self.engine.is_valid_target(target):
            self.engine.add_target(target)
        else:
            await self.console.print("[bold red]Invalid target format.[/bold red]")

    async def run_task(self, task_func, task_name):
        try:
            await task_func()
            await self.console.print(f"[bold green]{task_name.capitalize()} completed successfully.[/bold green]")
        except Exception as e:
            await self.console.print(f"[bold red]{task_name.capitalize()} error: {e}[/bold red]")

    async def run_exploit(self):
        try:
            await self.console.print("Enter exploit details:")
            exploit = await self.console.input("Exploit: ")
            payload = await self.console.input("Payload: ")
            target = self.engine.targets[0]  # For simplicity, using the first target
            await self.engine.run_exploit(target, exploit, payload)
            await self.console.print(self.engine.responses["exploit_completed"])
        except Exception as e:
            await self.console.print(f"[bold red]Exploit error: {e}[/bold red]")

    async def schedule_scan(self):
        try:
            target = await self.console.input("Enter target: ")
            if target not in self.engine.targets:
                await self.console.print("[bold red]Target not in the list. Please add the target first.[/bold red]")
                return
            interval = int(await self.console.input("Enter interval in minutes: "))
            scheduler.add_scan_job(self.engine.run_scan, target, interval)
            await self.console.print(self.engine.responses["schedule_scan_success"].format(target=target, interval=interval))
        except ValueError:
            await self.console.print("[bold red]Invalid interval. Please enter a valid number.[/bold red]")
        except Exception as e:
            await self.console.print(f"[bold red]Scheduling scan error: {e}[/bold red]")

    async def run_phishing_attack(self):
        try:
            target = await self.console.input("Enter target email: ")
            await self.engine.run_phishing_attack(target)
            await self.console.print(self.engine.responses["phishing_attack_executed"].format(target=target))
        except Exception as e:
            await self.console.print(f"[bold red]Phishing attack error: {e}[/bold red]")

    async def run_social_engineering_attack(self):
        try:
            target = await self.console.input("Enter target email: ")
            await self.engine.run_social_engineering_attack(target)
            await self.console.print(self.engine.responses["social_engineering_attack_executed"].format(target=target))
        except Exception as e:
            await self.console.print(f"[bold red]Social engineering attack error: {e}[/bold red]")

    async def show_help(self):
        await self.console.print("[bold blue]Hacking Assistant Commands:[/bold blue]")
        await self.console.print("[green]q[/green] - Quit the application")
        await self.console.print("[green]h[/green] - Show this help message")

class HackingAssistantEngine:
    def __init__(self, console: Console, db: Optional[database.Database] = None, log: Optional[logger.Logger] = None):
        self.targets: List[str] = []
        self.results = {}
        self.console = console
        self.log = log or logger.setup_logger('hacking_assistant', 'logs/hacking_assistant.log')
        self.db = db or database.Database()
        with open('responses.json') as f:
            self.responses = json.load(f)

    def is_valid_target(self, target: str) -> bool:
        # Basic validation for targets (IP/URL)
        return re.match(r'^[a-zA-Z0-9.\-]+$', target) is not None

    def add_target(self, target: str) -> None:
        if target not in self.targets:
            self.targets.append(target)
            self.db.add_target(target)
            self.log.info(f"Added target: {target}")
            self.console.print(self.responses["add_target_success"].format(target=target))
        else:
            self.console.print(self.responses["target_already_exists"].format(target=target))

    async def run_scan(self, target: Optional[str] = None) -> None:
        targets = self.targets if target is None else [target]
        self.console.print("Starting network scan...")
        tasks = [self._scan_target(target) for target in targets]
        await asyncio.gather(*tasks)

    async def _scan_target(self, target: str) -> None:
        try:
            scan_results = nmap_scan.scan_network(target)
            self.results.setdefault(target, {})['scan'] = scan_results
            self.db.update_results(target, 'scan', scan_results)
            self.log.info(f"Scan results for {target}: {scan_results}")
            self.console.print(self.responses["scan_completed"])
            await self.run_info_gathering(target)
        except Exception as e:
            self.log.error(f"Error during scan of {target}: {e}")
            self.console.print(self.responses["error_during_scan"].format(target=target, error=e))

    async def run_info_gathering(self, target: Optional[str] = None) -> None:
        targets = self.targets if target is None else [target]
        self.console.print("Starting information gathering...")
        tasks = [self._gather_info(target) for target in targets]
        await asyncio.gather(*tasks)

    async def _gather_info(self, target: str) -> None:
        try:
            info_results = info_gathering.gather_info(target)
            self.results.setdefault(target, {})['info'] = info_results
            self.db.update_results(target, 'info', info_results)
            self.log.info(f"Info gathering results for {target}: {info_results}")
            self.console.print(self.responses["info_gathering_completed"])
            await self.run_vulnerability_scan(target)
        except Exception as e:
            self.log.error(f"Error during info gathering for {target}: {e}")
            self.console.print(self.responses["error_during_info_gathering"].format(target=target, error=e))

    async def run_vulnerability_scan(self, target: Optional[str] = None) -> None:
        targets = self.targets if target is None else [target]
        self.console.print("Starting vulnerability scan...")
        tasks = [self._scan_vulnerabilities(target) for target in targets]
        await asyncio.gather(*tasks)

    async def _scan_vulnerabilities(self, target: str) -> None:
        try:
            vuln_results = vulnerability_scan.scan_target(target)
            self.results.setdefault(target, {})['vulnerabilities'] = vuln_results
            self.db.update_results(target, 'vulnerabilities', vuln_results)
            self.log.info(f"Vulnerability scan results for {target}: {vuln_results}")
            self.console.print(self.responses["vulnerability_scan_completed"])
        except Exception as e:
            self.log.error(f"Error during vulnerability scan of {target}: {e}")
            self.console.print(self.responses["error_during_vulnerability_scan"].format(target=target, error=e))

    async def run_exploit(self, target: str, exploit: str, payload: str) -> None:
        if not self.is_valid_target(target):
            self.console.print("[bold red]Invalid target format.[/bold red]")
            return

        self.console.print(f"Starting exploit {exploit} on target {target}...")
        try:
            result = exploit_module.run_exploit(target, exploit, payload)
            self.results.setdefault(target, {})['exploit'] = result
            self.db.update_results(target, 'exploit', result)
            self.log.info(f"Exploit {exploit} with payload {payload} run on {target}")
            self.console.print(self.responses["exploit_completed"])
        except Exception as e:
            self.log.error(f"Error during exploitation of {target} using {exploit}: {e}")
            self.console.print(self.responses["error_during_exploit"].format(target=target, exploit=exploit, error=e))

    async def generate_report(self) -> None:
        self.console.print("Generating report...")
        try:
            report.generate_report(self.results)
            self.log.info("Report generated")
            self.console.print(self.responses["report_generated"])
        except Exception as e:
            self.log.error(f"Error generating report: {e}")
            self.console.print(self.responses["error_generating_report"].format(error=e))

    async def run_phishing_attack(self, target: str) -> None:
        try:
            phishing.run_phishing_attack(target)
            self.console.print(self.responses["phishing_attack_executed"].format(target=target))
        except Exception as e:
            self.log.error(f"Error during phishing attack on {target}: {e}")
            self.console.print(self.responses["error_during_phishing_attack"].format(target=target, error=e))

    async def run_social_engineering_attack(self, target: str) -> None:
        try:
            social_engineering.run_social_engineering_attack(target)
            self.console.print(self.responses["social_engineering_attack_executed"].format(target=target))
        except Exception as e:
            self.log.error(f"Error during social engineering attack on {target}: {e}")
            self.console.print(self.responses["error_during_social_engineering_attack"].format(target=target, error=e))

    def run(self) -> None:
        app = HackingAssistantApp(self)
        app.run()
