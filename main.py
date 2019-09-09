import click
from prettytable import PrettyTable
from classes.path_class import Path
from classes.database_class import Storage
from classes.report_class import Report
from classes.unitconvertor import UniConv
from classes.markdown_class import MarkDown


@click.group()
def cli():
    pass


@cli.command()
@click.argument('path')
def scan(path):
    """Calculate the total path size"""
    myPath = Path()
    myUni = UniConv()

    if myPath.AddPath(path) is True:
        print("This {0} path had been added to Database".format(path))

    fullsize, lastID = myPath.CalculateSize(path)
    myPath.calculate_files_suffix(path, lastID)

    print("Total size of {0} : {1}".format(path, myUni.beauty_size(fullsize)))


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
    myDB = Storage()

    if myDB.DB_is_new(path) is True:
        print("This {0} \nis wrong, it's not available on the DB".format(path))
    else:
        if yes is True:
            myPath.RemovePath(path)
            print("done")
        else:
            message = "Are you sure you want to remove \"" + path + "\"? [Y/N]"
            answer = input(message)
            if answer.upper() == "Y":
                myPath.RemovePath(path)
                print("Done!!!")
            else:
                print("Ok, nothing had been removed")


@cli.command()
@click.option('--yes', is_flag=True, help="Accept remove without asking")
def remove_all(yes):
    """Remove all data stored in DB"""
    myDB = Storage()
    if yes is True:
        myDB.DB_RemoveAllPaths()
        myDB.DB_RemoveAllQueries()
        myDB.DB_RemoveAllQFE()
        print("done")
    else:
        message = "Are you sure you want to remove everything? [Y/N]"
        answer = input(message)
        if answer.upper() == "Y":
            myDB.DB_RemoveAllPaths()
            myDB.DB_RemoveAllQueries()
            myDB.DB_RemoveAllQFE()
            print("done")
        else:
            print("Ok, nothing had been removed")


@cli.command()
def export_report():
    """This will export a report using Markdown format"""

    myReport = Report()

    myReport.get_pc_information()

    myReport.RP_InsertIndex()
    myReport.RP_InsertSharedPaths()
    myReport.RP_InsertMoreInormation()
    myReport.RP_InsertFileTypes()
    myReport.RP_InsertPieChart_FEC_Size()

    myReport.RP_Commit()


@cli.command()
def add_FEC():
    """Add a new file extension category"""
    FEC_Name = input("Insert file extension category name: ")
    FEC_Info = input("Insert file extension category Info: ")

    myDB = Storage()
    myPath = Path()

    if myPath.is_FEC_Exist(FEC_Name) is False:
        myDB.DB_AddFEC(FEC_Name, FEC_Info)
    else:
        print("This file extension category is already exist!!")


@cli.command()
def add_FE():
    """Add a new file extension"""
    FEC_ID = input("Insert file extension category ID: ")
    FE_name = input("Insert file extension name: ")

    myDB = Storage()
    myPath = Path()

    if myPath.is_FE_Exist(FE_name) is False:
        myDB.DB_AddFEC(FEC_ID, FE_name)
    else:
        print("This file extension is already exist!!")


@cli.command()
def list_FEC():
    """List All Stored extension category"""
    myDB = Storage()
    table = PrettyTable()

    table.field_names = ["#", "Name", "Info"]
    table.align["Info"] = "l"

    for row in myDB.DB_GetAllFEC():
        table.add_row([row['FEC_ID'], row['FEC_Name'], row['FEC_Info']])

    print(table)


@cli.command()
def list_FE():
    """List All Stored extension for a specific category"""
    myDB = Storage()
    table = PrettyTable()

    FEC_ID = input("Insert file extension category ID: ")

    table.field_names = ["#", "Name"]

    for row in myDB.DB_GetAllFE_ByFEC(FEC_ID):
        table.add_row([row['FE_ID'], row['FE_Name']])

    print(table)


@cli.command()
@click.argument('FE_ID')
def remove_FE(FE_ID):
    """Remove a specific File Extension"""
    myPath = Path()
    myPath.remove_FE(FE_ID)


@cli.command()
@click.argument('FEC_ID')
def remove_FEC(FEC_ID):
    """Remove a specific File Extension Category"""
    myPath = Path()
    myPath.remove_FEC(FEC_ID)


if __name__ == "__main__":
    cli()
