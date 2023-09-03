import sniper.snapshot as snapshot
import sniper.ami as ami
import sniper.instance as instance

# @todo: maybe this shouild return something rather than printing things

def process(rows, args):
    dry_run = not args.delete
    for row in rows:
        print("★","\t",row['type'],row['id'],row['region'])
        match row['type']:
            case "Snapshot":
                try:
                    info = snapshot.describe(row['id'], row['region'])
                    if snapshot.has_deleteme_tag(info):
                        snapshot.delete(row['id'], dry_run, row['region'])
                    else:
                        print(row['type'],row['id'],"did not have delete tag")
                except Exception as e:
                    print(e, " -- skipping")
            case "Image":
                try:
                    info = ami.describe(row['id'], row['region'])
                    if ami.has_deleteme_tag(info):
                        ami.deregister(row['id'], dry_run, row['region'])
                    else:
                        print(row['type'],row['id'],"did not have delete tag")
                except Exception as e:
                    print(e, " -- skipping")
            case "Instance":
                try:
                    info = instance.describe(row['id'], row['region'])
                    if instance.has_deleteme_tag(info):
                        instance.terminate(row['id'], dry_run, row['region'])
                    else:
                        print(row['type'],row['id'],"did not have delete tag")
                except Exception as e:
                    print(e, " -- skipping")
            case _:
                print("method not implemented for type",row['type'])
        print()
