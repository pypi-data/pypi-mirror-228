import argparse
import brof.command_funcs as cf
import os

parser = argparse.ArgumentParser(description="CLI tool for keeping changes to a file updated in different locations")
parser.add_argument("-add", "-a", dest="add", nargs=2, help="Add a pair of files")
parser.add_argument("-remove", "-rm", dest="remove", nargs=2, help="Remove a pair of files")
parser.add_argument("-refresh", "-r", dest="refresh", action="store_true", help="Refresh current pairs to update changes")
parser.add_argument("-dir", "-d", dest="dir", nargs=2, help="Add a pair of directories")
parser.add_argument("-show", "-s", dest="show", action="store_true", help="Show the pairs of the current workspace")
parser.add_argument("-clear", "-c", dest="clear", action="store_true", help="Clear all the pairs from the current workspace")

def main():
    cf.setup_file(cf.file_path)
    args = parser.parse_args()

    if args.add:
        src = args.add[0]
        dst = args.add[1]

        if not os.path.exists(src) or not os.path.exists(dst):
            print("Both files must exisit")
            return
        if cf.has_pair(src, dst):
            print("The pair already exisits in the workspace")
            return
        if os.path.isdir(src) or os.path.isdir(dst):
            print("Both must be files, trying to add file and folder")
            return

        cf.add_pair_to_store(args.add[0], args.add[1])   
    elif args.remove:
        src = args.remove[0]
        dst = args.remove[1]
        
        if not cf.has_pair(src, dst):
            print("The pair must exisit in the workspace")
            return
        if not os.path.exists(src) or not os.path.exists(dst):
            print("Both files must exisit")
            return

        cf.remove_pair(src, dst)   
    elif args.refresh:
        to_refresh = cf.find_changed()
        print("Pairs to be updated:")
        print(to_refresh)

        for pair in to_refresh:
            io = input(f"Do you want to refresh pair: {pair}? y/n or a for refreshing all pairs ")
            if io == "y":
                cf.refresh_pair(pair)
            elif io == "a":
                cf.refresh_pairs(to_refresh)
                break
    elif args.dir:
        src = args.dir[0]
        dst = args.dir[1]

        if not os.path.exists(src) or not os.path.exists(dst):
            print("Both directories must exisit")
            return
        if not os.path.isdir(src) or not os.path.isdir(dst):
            print("Both must be directories, trying to add folder and file")
            return

        cf.add_folders(src, dst)   
    elif args.show:
        cf.show_pairs()
    elif args.clear:
        cf.clear_file_pairs_file()

if __name__ == "__main__":
    main()
