from utils.steam_api import get_top_skins
from rich.console import Console
from rich.table import Table

console = Console()
console.rule("[bold yellow]Top Selling CS2 Skins[/bold yellow]")

skins = get_top_skins(10)

table = Table(title="Steam Market - CS2 Top Items")
table.add_column("Name", style="cyan")
table.add_column("Price", style="green")

for _, row in skins.iterrows():
    table.add_row(row["Name"], row["Price"])

console.print(table)
console.print("[bold blue]Data saved → data/prices.csv[/bold blue]")
