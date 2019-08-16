import click
from prettytable import PrettyTable
from classes.path_class import Path
from classes.database_class import Storage
from classes.report_class import Report
from classes.unitconvertor import UniConv


@click.group()
def cli():
    pass


@cli.command()
@click.argument('path')
def check_size(path):
    """Calculate the total path size"""
    myPath = Path()

    if myPath.CalculateSize(path) is True:
        print("Added to Database!!")
    else:
        print("Error: Can't be added to the Database!!")


@cli.command()
@click.argument('path')
@click.option('--count', default=0, help='Enter 0 or less for all results')
def get_report(path, count):
    """Show a saved information about specific path"""
    myPath = Path()
    myUnit = UniConv()
    myDB = Storage()

    if myDB.DB_is_new(path) is False:
        table = PrettyTable()

        table.field_names = ["#", "Time", "Size", "Path"]

        for count, result in enumerate(myPath.GetSizes(path, count), start=1):
            table.add_row([count,
                           result['time_stamp'],
                           myUnit.beauty_size(result['size']),
                           path])

        print(table)
    else:
        print("Sorry, The path is not exist !!")


@cli.command()
def list_all_paths():
    """Print a list for all saved paths in DB"""
    myDB = Storage()
    myPath = Path()
    results = myDB.DB_GetAllPaths()

    table = PrettyTable()
    table.field_names = ["#", "Path"]

    table.align["Path"] = "l"

    for row in results:
        table.add_row([myPath.GetPathID(row['path']), row['path']])

    print(table)


@cli.command()
@click.argument('path')
@click.option('--yes', is_flag=True, help="Accept remove without asking")
def remove_path(path, yes):
    """Remove specific Path form DB"""
    myPath = Path()
    if yes is True:
        myPath.RemovePath(path)
        print("done")
    else:
        message = "Are you sure you want to remove \"" + path + "\"? [Y/N]"
        answer = input(message)
        if answer.upper() == "Y":
            myPath.RemovePath(path)
        else:
            print("Ok, nothing had been removed")


@cli.command()
@click.option('--yes', is_flag=True, help="Accept remove without asking")
def remove_all(yes):
    """Remove all data stored in DB"""
    myDB = Storage()
    if yes is True:
        myDB.DB_RemoveAllPath()
        print("done")
    else:
        message = "Are you sure you want to remove everything? [Y/N]"
        answer = input(message)
        if answer.upper() == "Y":
            myDB.DB_RemoveAllPath()
            print("done")
        else:
            print("Ok, nothing had been removed")


@cli.command()
def export_report():
    """This will export a report using Markdown format"""

    myReport = Report()

    myReport.RP_InsertIndex()
    myReport.RP_InsertSharedPaths()
    myReport.RP_InsertMoreInormation()
    myReport.RP_Commit()


if __name__ == "__main__":
    cli()
