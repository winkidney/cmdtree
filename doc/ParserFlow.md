
## Error Type

+ No such command
+ Argument Required
+ Invalid Argument Type

```
cmd_path = get_cmd_path()
parser = get_parser(cmd_path)
find command (argv, cmd_path)->
    validate argument-length
    find command(child_cmd_path, argv[command_2:])

```
