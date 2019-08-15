import click
from prettytable import PrettyTable
from classes.path_class import Path
from classes.database_class import Storage
from classes.markdown_class import MarkDown
from classes.report_class import Report
from classes.unitconvertor import UniConv


@click.group()
def cli():
    pass


@cli.command()
@click.argument('path')
def check_size(path):
    """Calculate the total path size"""
    myPath = Path(path)
    click.echo("Total size = {0:8s}".format(myPath.sizeUnit))
    if myPath.Commit() is True:
        print("Added to Database!!")
    else:
        print("Error: Can't be added to the Database!!")


@cli.command()
@click.argument('path')
@click.option('--count', default=1, help='Enter 0 or less for all results')
def get_report(path, count):
    """Show a saved information about specific path"""
    myPath = Path(path)
    table = PrettyTable()
    myUnit = UniConv()

    table.field_names = ["#", "Time", "Size", "Path"]

    for count, result in enumerate(myPath.GetSizes(count), start=1):
        table.add_row([count, result['time_stamp'],
                       myUnit.beauty_size(result['size']),
                       path])

    print(table)


@cli.command()
def list_all_paths():
    """Print a list for all saved paths in DB"""
    myDB = Storage()
    results = myDB.DB_GetAllPaths()

    table = PrettyTable()
    table.field_names = ["#", "Path"]

    table.align["Path"] = "l"

    for row in results:
        myPath = Path(row)
        table.add_row([myPath.pathID, myPath.path])

    print(table)


@cli.command()
@click.argument('path')
@click.option('--yes', is_flag=True, help="Accept remove without asking")
def remove_path(path, yes):
    """Remove specific Path form DB"""
    myPath = Path(path)
    if yes is True:
        myPath.RemovePath()
        print("done")
    else:
        message = "Are you sure you want to remove \"" + path + "\"? [Y/N]"
        answer = input(message)
        if answer.upper() == "Y":
            myPath.RemovePath()
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
    md = MarkDown()
    myDB = Storage()
    myReport = Report()

    md.MD_header(1, 'Index')
    md.MD_text('[toc]', True)
    md.MD_horizontal_rule()

    md.MD_header(1, 'Shared Paths')

    allPaths = myDB.DB_GetAllPaths()
    table = []

    for path in allPaths:
        table.append(myReport.RP_MainTable(path))

    md.MD_table(table)

    md.MD_horizontal_rule()

    md.MD_header(1, "More Information for each Path")

    for path in allPaths:
        filename = myReport.RP_DrawFig(path, md.MD_getFoldername(), md.MD_getReportpath())
        md.MD_header(2, path)
        md.MD_image('',filename, newline=True)




    md.MD_commit()


if __name__ == "__main__":
    cli()
